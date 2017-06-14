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

U_drivers = [
    {'username': 'driver', 'role': 'driver', 'name': 'John Smith', 'password': 'test', },
    {'username': 'driver0', 'role': 'driver', 'name': 'Stan Mohan', 'password': 'test'},
    {'username': 'driver1', 'role': 'driver', 'name': 'Ed Hong Weiming', 'password': 'test'},
    {'username': 'driver2', 'role': 'driver', 'name': 'Tony Khoo', 'password': 'test'},
    {'username': 'driver3', 'role': 'driver', 'name': 'Roger Shum Cheng Sean', 'password': 'test'}
]

U_all = [U_manager, *U_drivers]

D_drivers = [
    {'task_id': None, 'name_': 'John Smith', 'status': Choice('off', 'Off Work')},
    {'task_id': None, 'name_': 'Stan Mohan', 'status': Choice('off', 'Off Work')},
    {'task_id': None, 'name_': 'Ed Hong Weiming', 'status': Choice('off', 'Off Work')},
    {'task_id': None, 'name_': 'Tony Khoo', 'status': Choice('off', 'Off Work')},
    {'task_id': None, 'name_': 'Roger Shum Cheng Sean', 'status': Choice('off', 'Off Work')}
]

F_flights = [{'actual_time': now(), 'type_': 'D', 'flight_num': 'SQ452', 'pax': 196, 'id': 39840, 'num_containers': 4,
              'terminal': 'T2', 'scheduled_time': now()},
             {'actual_time': now(), 'type_': 'D', 'flight_num': 'SQ211', 'pax': 231, 'id': 57763, 'num_containers': 3,
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
             {'actual_time': now(), 'type_': 'A', 'flight_num': 'SQ615', 'pax': 250, 'id': 16804, 'num_containers': 7,
              'terminal': 'T3', 'scheduled_time': now()},
             {'actual_time': now(), 'type_': 'A', 'flight_num': 'SQ173', 'pax': 218, 'id': 76604, 'num_containers': 2,
              'terminal': 'T2', 'scheduled_time': now()},
             {'actual_time': now(), 'type_': 'A', 'flight_num': 'SQ208', 'pax': 235, 'id': 60450, 'num_containers': 3,
              'terminal': 'T3', 'scheduled_time': now()}]

T_tasks = []
for i, (j, k) in enumerate(rng.uniform(1, 60, (len(F_flights), 2))):

    F_flights[i]['scheduled_time'] += td(minutes=j, seconds=k)

    _flight = F_flights[i]
    _num_containers = _flight['num_containers']
    _containers = [4 for _ in range(_num_containers // 4)]

    if _num_containers % 4 != 0:
        _containers.append(_num_containers % 4)

    for _c in _containers:
        T_tasks.append({
            'status': Choice('ready', 'Ready'),
            'ready_time': (
                (_flight['scheduled_time'] + td(minutes=rng.triangular(1, 3, 5))) if _flight['type_'] == 'A' else
                (_flight['scheduled_time'] + td(minutes=-30))),
            'completed_time': _flight['scheduled_time'] + td(minutes=rng.triangular(16, 17, 18)),
            'flight_time': _flight['scheduled_time'],
            'driver': None,
            'containers': _c,
            'source': _flight['flight_num'] if _flight['type_'] == 'A' else 'HOTA',
            'destination': 'HOTA' if _flight['type_'] == 'A' else _flight['flight_num']
        })
