import json

from Dashboard.blueprints.api.models import Drivers
from Dashboard.blueprints.api.views import api, FlightsCtrl, TasksCtrl, DriversCtrl
from Dashboard.tests.data_for_test import D_drivers, F_flights, T_tasks
from utils.tests_helpers import TestMixin, AssertsMixin


class TestViews(TestMixin, AssertsMixin):
    def test_flights_get(self):
        url = api.url_for(FlightsCtrl)

        response = self.client.get(url)
        data = dict(json.loads(response.data.decode('utf-8')))

        assert "schedule" in data.keys()

        rows = data['schedule']

        assert len(rows) == len(F_flights)

        row_keys = {'type', 'terminal', 'actual_time', 'scheduled_time', 'containers', 'flight_num'}
        for row in rows:
            assert len(row_keys - set(row.keys())) == 0

    def test_tasks_get(self):
        url = api.url_for(TasksCtrl)

        response = self.client.get(url)
        data = dict(json.loads(response.data.decode('utf-8')))

        assert "tasks" in data.keys()

        rows = data['tasks']

        assert len(rows) == len(T_tasks)

        row_keys = {'task_id', 'status', 'containers', 'ready_time', 'source', 'destination', 'driver'}
        for row in rows:
            assert len(row_keys - set(row.keys())) == 0

    def test_drivers_get_all(self):
        url = api.url_for(DriversCtrl, type='all')

        response = self.client.get(url)
        data = dict(json.loads(response.data.decode('utf-8')))

        assert 'drivers' in data.keys()

        rows = data['drivers']

        assert len(rows) == len(D_drivers)

        row_keys = {'name', 'status', 'task_id'}
        for row in rows:
            assert len(row_keys - set(row.keys())) == 0

    def test_drivers_get_working(self):
        url = api.url_for(DriversCtrl)

        d1 = Drivers.get_by_identity('Stan Mohan')
        d2 = Drivers.get_by_identity('John Smith')
        d1.ready()
        d2.ready()

        response = self.client.get(url)
        data = dict(json.loads(response.data.decode('utf-8')))

        assert 'drivers' in data.keys()
        assert len(data['drivers']) == 2

    def test_drivers_post(self):
        url = api.url_for(DriversCtrl)

        payload = {
            'name': 'John Smith',
            'activity': 'start'
        }

        response = self.client.post(url,
                                    data=json.dumps(payload),
                                    content_type="application/json")

        data = json.loads(response.data.decode('utf-8'))

        assert len({'task', 'driver'} - set(data.keys())) == 0
        assert type(data['task']) == dict
        assert type(data['driver']) == dict

        assert data['driver']['name'] == payload['name']
        assert data['driver']['status'] == 'On Task'

        payload['activity'] = 'complete'
        response = self.client.post(url,
                                    data=json.dumps(payload),
                                    content_type="application/json")

        data = json.loads(response.data.decode('utf-8'))

        assert len({'task', 'driver'} - set(data.keys())) == 0
        assert type(data['task']) == dict
        assert type(data['driver']) == dict

        assert data['driver']['name'] == payload['name']
        assert data['driver']['status'] == 'On Task'

        payload['activity'] = 'break'
        response = self.client.post(url,
                                    data=json.dumps(payload),
                                    content_type="application/json")

        data = json.loads(response.data.decode('utf-8'))

        assert len({'task', 'driver'} - set(data.keys())) == 0
        assert data['task'] is None
        assert type(data['driver']) == dict

        assert data['driver']['name'] == payload['name']
        assert data['driver']['status'] == 'Break'

        payload['activity'] = 'stop'

        response = self.client.post(url,
                                    data=json.dumps(payload),
                                    content_type="application/json")

        data = json.loads(response.data.decode('utf-8'))

        assert len({'task', 'driver'} - set(data.keys())) == 0
        assert data['task'] is None
        assert type(data['driver']) == dict

        assert data['driver']['name'] == payload['name']
        assert data['driver']['status'] == 'Off Work'
