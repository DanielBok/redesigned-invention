import sqlite3
from datetime import timedelta as td
from os.path import join, dirname, abspath, exists

import pandas as pd
from numpy import random as rng
from sqlalchemy_utils import database_exists

from Dashboard.blueprints.api.models import Drivers, Flights, Tasks
from Dashboard.blueprints.user.models import User
from Dashboard.extensions import db
from configs.settings import SQLALCHEMY_DATABASE_URI
from database_utils.extra import ProgressEnumerate
from utils import now

APP_DATA = abspath(join(dirname(__file__), '..',  'app_data'))


def seed(app):
    print("Initializing and seeding database_utils.", end='\t')
    if not database_exists(SQLALCHEMY_DATABASE_URI):
        if SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
            with sqlite3.connect(join(APP_DATA, 'data.db')):
                pass
        else:
            message = "Failed to connect to database. Please check if it is provisioned.\n" \
                      "Database URI = " + SQLALCHEMY_DATABASE_URI
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
        for i, line in enumerate(f):
            name = line.strip().split('\t')[0]
            employees.append({
                'role': 'driver',
                'username': 'driver{0:d}'.format(i),
                'password': 'airport',
                'name': name
            })
            names.append(name)

    for e in ProgressEnumerate(employees):
        if not User.find_by_identity(e['username']):
            db.session.add(User(**e))

        if e['role'] == 'driver' and not Drivers.get_by_identity(e['name']):
            db.session.add(Drivers(name_=e['name']))

    print('Seeding Flights and Tasks table')
    df = pd.DataFrame(
        pd.read_pickle(join(APP_DATA, 'flights.p')))

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
        db.session.add(Flights(**e))

        nc = e['num_containers']
        if nc > 0:
            last_num = 1 + nc // 4
            if nc % 4 == 0:
                last_num -= 1

            st = e['scheduled_time']
            rt = st if e['type_'] == 'A' else st - td(minutes=30)
            ct = st + td(minutes=rng.triangular(16, 17, 18))

            for i in range(last_num):
                task_data = {
                    'status': 'done' if st <= time else 'ready',
                    'ready_time': rt,
                    'completed_time': ct,
                    'driver': rng.choice(names) if st <= otime else None,
                    'containers': 4 if i + 1 < last_num else nc % 4,
                    'source': e['flight_num'] if e['type_'] == 'A' else 'HOTA',
                    'destination': e['flight_num'] if e['type_'] == 'D' else 'HOTA'
                }
                db.session.add(Tasks(**task_data))

    try:
        print("Committing data. This may take a while..")
        db.session.commit()
    except:
        db.session.rollback()
        raise Exception('Mass commit failed')

    print('Seeding Complete')


def local_db_exists():
    return exists(join(APP_DATA, 'data.db'))
