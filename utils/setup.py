import sys
from datetime import timedelta as td
from os import getenv
from os.path import join, dirname, abspath, exists

import pandas as pd
from numpy import random as rng
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import database_exists, create_database

from Dashboard.blueprints.api.models import Drivers, Flights, Tasks
from Dashboard.blueprints.user.models import User
from Dashboard.extensions import db
from configs.settings import SQLALCHEMY_DATABASE_URI
from utils.extra import ProgressEnumerate
from .datetime import now

APP_DATA = abspath(join(dirname(__file__), '..', 'app_data'))


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
    return exists(join(APP_DATA, 'data.db'))


def insert_data(_db):
    """
    Inserts data into empty database
    :param _db: SQLAlchemy db context
    :return: None
    """
    is_heroku = getenv('IS_HEROKU', 'NO') == 'YES'

    print('Seeding employees and driver tables.')
    # insert employees
    employees = [{
        'role': 'manager',
        'username': 'manager',
        'password': 'airport',
        'name': 'Roger Federer'
    }]

    names = []
    with open(join(APP_DATA, 'people.txt')) as f:
        for c, line in enumerate(f):
            name = line.strip().split('\t')[0]
            employees.append({
                'role': 'driver',
                'username': 'driver{0:d}'.format(c),
                'password': 'airport',
                'name': name
            })
            names.append(name)

            if is_heroku and c >= 20:
                break

    for e in ProgressEnumerate(employees):
        if not User.find_by_identity(e['username']):
            _db.session.add(User(**e))

        if e['role'] == 'driver' and not Drivers.get_by_identity(e['name']):
            _db.session.add(Drivers(name_=e['name']))

    print('Seeding Flights and Tasks table')
    df = pd.DataFrame(pd.read_pickle(join(APP_DATA, 'flights.p')))

    if is_heroku:
        df = df.loc[(df.TIME >= now()) & (df.TIME <= now() + td(days=7))].reset_index(drop=True)

    df.rename(columns={
        'FL': 'flight_num',
        'TER': 'terminal',
        'TIME': 'scheduled_time',
        'TYPE': 'type_',
        'PAX': 'pax',
        'CONTAINERS': 'num_containers',
    }, inplace=True)

    df['actual_time'] = df.scheduled_time

    otime = now()
    time = otime + td(minutes=5)
    ddf = df.to_dict('records')
    for e in ProgressEnumerate(ddf):
        _db.session.add(Flights(**e))

        nc = e['num_containers']
        if nc > 0:

            _containers = [4 for _ in range(nc // 4)]
            if nc % 4 != 0:
                _containers.append(nc % 4)

            st = e['scheduled_time']
            rt = st if e['type_'] == 'A' else st - td(minutes=30)
            ct = st + td(minutes=rng.triangular(16, 17, 18))

            for c in _containers:

                if e['type_'] == 'A':
                    source = e['flight_num']
                    dest = 'HOTA'
                else:
                    source = 'HOTA'
                    dest = e['flight_num']

                task_data = {
                    'status': 'done' if st <= time else 'ready',
                    'ready_time': rt,
                    'completed_time': ct,
                    'flight_time': st,
                    'driver': rng.choice(names) if st <= otime else None,
                    'containers': c,
                    'source': source,
                    'destination': dest
                }
                _db.session.add(Tasks(**task_data))

    try:
        print("Committing data. This may take a while..")
        _db.session.commit()
    except SQLAlchemyError as e:
        _db.session.rollback()
        print("ERROR: Mass commit failed!!!! ", e, sep='\n', end='\n', file=sys.stderr)
