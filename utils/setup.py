import sys
from datetime import timedelta as td
from os.path import exists

import pandas as pd
from numpy import random as rng
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import database_exists, create_database

from Dashboard.blueprints.api.models import Drivers, Flights, Tasks
from Dashboard.blueprints.user.models import User
from Dashboard.extensions import db
from configs.settings import SQLALCHEMY_DATABASE_URI
from utils.extra import ProgressEnumerate
from .datetime import now, localize
from .extra import get_app_data_path


def seed(app):
    print("Initializing and seeding utils.", end='\t')

    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', SQLALCHEMY_DATABASE_URI)

    if not database_exists(db_uri):
        if db_uri.startswith('sqlite'):
            create_database(db_uri)
        else:
            message = "Failed to connect to database. Please check if it is provisioned.\n" \
                      "Database URI = " + db_uri
            raise Exception(message)
    else:
        print("Database exists. OKAY")

    db.app = app
    tables = [
        User.__table__,
        Drivers.__table__,
        Flights.__table__,
        Tasks.__table__
    ]

    print('Dropping and recreating tables in database. ', end='\t')
    db.metadata.drop_all(db.engine, tables=tables)
    db.metadata.create_all(db.engine, tables=tables)
    print('Complete')

    insert_data(db)

    print('Seeding Complete')


def local_db_exists():
    return exists(get_app_data_path('data.db'))


def insert_data(_db):
    """
    Inserts data into empty database
    :param _db: SQLAlchemy db context
    :return: None
    """

    print('Seeding employees and driver tables.')
    # insert employees
    employees = [{
        'role': 'manager',
        'username': 'manager',
        'password': 'airport',
        'name': 'Roger Federer'
    }]

    file = get_app_data_path('people.txt')

    names = []
    with open(file) as f:
        for c, line in enumerate(f):
            name = line.strip().split('\t')[0]
            employees.append({
                'role': 'driver',
                'username': 'driver{0:d}'.format(c),
                'password': 'airport',
                'name': name
            })
            names.append(name)

    _seed_users_and_workers(_db, employees)

    _seed_flights_and_task(_db, names)


def secret_seed():
    print("Initializing secret seeding", end='\t')

    db.drop_all()
    db.create_all()

    print('Seeding employees and driver tables.')
    # insert employees
    employees = [{
        'role': 'manager',
        'username': 'manager',
        'password': 'airport',
        'name': 'Roger Federer'
    }]

    names = []
    with open(get_app_data_path('people.txt')) as f:
        for c, line in enumerate(f):
            name = line.strip().split('\t')[0]
            employees.append({
                'role': 'driver',
                'username': 'driver{0:d}'.format(c),
                'password': 'airport',
                'name': name
            })
            names.append(name)

            if c >= 20:
                break

    _seed_users_and_workers(db, employees)

    _seed_flights_and_task(db, names, 3, 3)


def _seed_users_and_workers(_db, employees: list):
    count = 0
    for e in ProgressEnumerate(employees):
        if not User.find_by_identity(e['username']):
            _db.session.add(User(**e))

        if e['role'] == 'driver' and not Drivers.get_by_identity(e['name']):
            _db.session.add(Drivers(name_=e['name']))

        if count % 250 == 0:
            _db.session.commit()
        count += 1

    try:
        print("Committing data. This may take a while..")
        _db.session.commit()
    except SQLAlchemyError as e:
        _db.session.rollback()
        print("ERROR: Mass commit failed!!!! ", e, sep='\n', end='\n', file=sys.stderr)


def _seed_flights_and_task(_db, names: list, days_before: int = None, days_after: int = None, limiter=250):
    print('Seeding Flights and Tasks table')
    count = 0
    df = pd.DataFrame(pd.read_pickle(get_app_data_path('flights.p')))

    if days_after is not None and days_after is not None:
        df = df.loc[(df.TIME >= now() - td(days=days_before)) &
                    (df.TIME <= now() + td(days=days_after))].reset_index(drop=True)

    df.rename(columns={
        'FL': 'flight_num',
        'TER': 'terminal',
        'TIME': 'scheduled_time',
        'TYPE': 'type_',
        'PAX': 'pax',
        'CONTAINERS': 'num_containers',
        "BAY": 'bay'
    }, inplace=True)

    mixture = rng.normal(-2.5, 3, len(df)) + rng.normal(2.5, 3, len(df))
    df['actual_time'] = [t + td(minutes=m) for t, m in zip(df.scheduled_time, mixture)]

    otime = now()
    time = otime + td(minutes=1)
    ddf = df.to_dict('records')
    for e in ProgressEnumerate(ddf):
        _db.session.add(Flights(**e))

        nc = e['num_containers']
        if nc > 0:

            _containers = [4 for _ in range(nc // 4)]
            if nc % 4 != 0:
                _containers.append(nc % 4)

            at = e['actual_time']

            if e['type_'] == 'A':
                source = e['flight_num']
                dest = e['terminal'] + 'HOT'
                rt = at + td(minutes=rng.triangular(1, 1.8, 3))
            else:
                source = e['terminal'] + 'HOT'
                dest = e['flight_num']
                rt = at - td(minutes=35)

            ts = rt + td(minutes=rng.uniform(0, 1.5))
            ct = ts + td(minutes=rng.triangular(16, 17, 18))

            ttt = None
            if at <= time:
                status = 'done'
                driver = rng.choice(names)
                ttt = (ct - ts).total_seconds()
            elif ct > now():
                status = 'er'
                driver = rng.choice(names)
                ct = None
            else:
                status = 'ready'
                ct = None
                if at <= otime:
                    driver = rng.choice(names)
                else:
                    driver = None

            for c in _containers:

                task_data = {
                    'status': status,
                    'ready_time': rt,
                    'completed_time': ct,
                    'flight_time': at,
                    'driver': driver,
                    'containers': c,
                    'source': source,
                    'destination': dest,
                    'bay': e['bay'],
                    'task_start_time': ts,
                    'task_time_taken': ttt
                }
                _db.session.add(Tasks(**task_data))

                if count % limiter == 0:
                    _db.session.commit()
                count += 1

    try:
        print("Committing data. This may take a while..")
        _db.session.commit()
    except SQLAlchemyError as e:
        _db.session.rollback()
        print("ERROR: Mass commit failed!!!! ", e, sep='\n', end='\n', file=sys.stderr)
