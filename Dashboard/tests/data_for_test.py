from datetime import timedelta as td

import numpy.random as rng
from sqlalchemy_utils import Choice

from utils.datetime import now

U_manager = {
    'role': 'manager',
    'username': 'manager',
    'password': 'test',
    'name': 'Roger Federer'
}

U_driver = {
    'role': 'driver',
    'username': 'driver',
    'password': 'test',
    'name': 'John Smith'
}

U_all = [U_manager, U_driver]

D_driver = {
    'name_': 'John Smith',
    'task_id': None,
    'status': Choice('off', 'Off Work')
}

T_tasks = [
    {'completed_time': None, 'containers': 2, 'ready_time': now(), 'destination': 'HOTA', 'id': 51984,
     'driver': None, 'status': Choice('ready', 'Ready'), 'source': 'SQ997'},
    {'completed_time': None, 'containers': 2, 'ready_time': now(), 'destination': 'HOTA', 'id': 51988,
     'driver': None, 'status': Choice('ready', 'Ready'), 'source': 'SQ238'},
    {'completed_time': None, 'containers': 2, 'ready_time': now(), 'destination': 'HOTA', 'id': 51989,
     'driver': None, 'status': Choice('ready', 'Ready'), 'source': 'SQ661'},
    {'completed_time': None, 'containers': 2, 'ready_time': now(), 'destination': 'HOTA', 'id': 51991,
     'driver': None, 'status': Choice('ready', 'Ready'), 'source': 'SQ891'},
    {'completed_time': None, 'containers': 3, 'ready_time': now(), 'destination': 'HOTA', 'id': 51992,
     'driver': None, 'status': Choice('ready', 'Ready'), 'source': 'SQ671'},
    {'completed_time': None, 'containers': 4, 'ready_time': now(), 'destination': 'HOTA', 'id': 51993,
     'driver': None, 'status': Choice('ready', 'Ready'), 'source': 'SQ425'},
    {'completed_time': None, 'containers': 2, 'ready_time': now(), 'destination': 'HOTA', 'id': 51994,
     'driver': None, 'status': Choice('ready', 'Ready'), 'source': 'SQ425'},
    {'completed_time': None, 'containers': 4, 'ready_time': now(), 'destination': 'HOTA', 'id': 51995,
     'driver': None, 'status': Choice('ready', 'Ready'), 'source': 'SQ325'},
    {'completed_time': None, 'containers': 2, 'ready_time': now(), 'destination': 'HOTA', 'id': 51996,
     'driver': None, 'status': Choice('ready', 'Ready'), 'source': 'SQ325'},
    {'completed_time': None, 'containers': 3, 'ready_time': now(), 'destination': 'SQ116', 'id': 51997,
     'driver': None, 'status': Choice('ready', 'Ready'), 'source': 'HOTA'},
    {'completed_time': None, 'containers': 4, 'ready_time': now(), 'destination': 'SQ836', 'id': 51998,
     'driver': None, 'status': Choice('ready', 'Ready'), 'source': 'HOTA'},
    {'completed_time': None, 'containers': 2, 'ready_time': now(), 'destination': 'SQ836', 'id': 51999,
     'driver': None, 'status': Choice('ready', 'Ready'), 'source': 'HOTA'},
    {'completed_time': None, 'containers': 4, 'ready_time': now(), 'destination': 'SQ964', 'id': 52003,
     'driver': None, 'status': Choice('ready', 'Ready'), 'source': 'HOTA'},
    {'completed_time': None, 'containers': 1, 'ready_time': now(), 'destination': 'SQ186', 'id': 52005,
     'driver': None, 'status': Choice('ready', 'Ready'), 'source': 'HOTA'},
    {'completed_time': None, 'containers': 3, 'ready_time': now(), 'destination': 'SQ982', 'id': 52008,
     'driver': None, 'status': Choice('ready', 'Ready'), 'source': 'HOTA'}
]

for i, (j, k) in enumerate(rng.uniform(0, 1, (len(T_tasks), 2))):
    T_tasks[i]['ready_time'] += td(minutes=j, seconds=k)

F_flights = [{'actual_time': now(), 'type_': 'D', 'flight_num': 'SQ452', 'pax': 196, 'id': 39840, 'num_containers': 4,
              'terminal': 'T2', 'scheduled_time': now()},
             {'actual_time': now(), 'type_': 'D', 'flight_num': 'SQ211', 'pax': 231, 'id': 57763, 'num_containers': 0,
              'terminal': 'T3', 'scheduled_time': now()},
             {'actual_time': now(), 'type_': 'A', 'flight_num': 'SQ305', 'pax': 217, 'id': 90970, 'num_containers': 2,
              'terminal': 'T3', 'scheduled_time': now()},
             {'actual_time': now(), 'type_': 'D', 'flight_num': 'SQ634', 'pax': 250, 'id': 8006, 'num_containers': 6,
              'terminal': 'T3', 'scheduled_time': now()},
             {'actual_time': now(), 'type_': 'A', 'flight_num': 'SQ447', 'pax': 136, 'id': 54142, 'num_containers': 3,
              'terminal': 'T2', 'scheduled_time': now()},
             {'actual_time': now(), 'type_': 'A', 'flight_num': 'SQ529', 'pax': 212, 'id': 79547, 'num_containers': 4,
              'terminal': 'T2', 'scheduled_time': now()},
             {'actual_time': now(), 'type_': 'D', 'flight_num': 'SQ636', 'pax': 250, 'id': 50788, 'num_containers': 3,
              'terminal': 'T3', 'scheduled_time': now()},
             {'actual_time': now(), 'type_': 'A', 'flight_num': 'SQ615', 'pax': 250, 'id': 16804, 'num_containers': 4,
              'terminal': 'T3', 'scheduled_time': now()},
             {'actual_time': now(), 'type_': 'A', 'flight_num': 'SQ173', 'pax': 218, 'id': 76604, 'num_containers': 2,
              'terminal': 'T2', 'scheduled_time': now()},
             {'actual_time': now(), 'type_': 'A', 'flight_num': 'SQ208', 'pax': 235, 'id': 60450, 'num_containers': 3,
              'terminal': 'T3', 'scheduled_time': now()}]

for i, (j, k) in enumerate(rng.uniform(0, 1, (len(F_flights), 2))):
    F_flights[i]['scheduled_time'] += td(minutes=j, seconds=k)
