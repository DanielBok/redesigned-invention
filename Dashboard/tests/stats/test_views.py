import json

from flask import url_for

from utils.tests_helpers import TestMixin, AssertsMixin


class TestViews(TestMixin, AssertsMixin):
    def test_index(self):
        response = self.client.get(url_for('stats.index'))
        assert response.status_code == 200

    def test_dp_api(self):
        response = self.client.get(url_for('stats.driver_performance_data'))
        data = dict(json.loads(response.data.decode('utf-8')))

        assert "container_mean_by_day" in data.keys()
        assert "container_total_by_day" in data.keys()
        assert "drivers" in data.keys()
        drivers = data['drivers']
        for d in drivers:
            assert d in data.keys()

    def test_csv(self):
        response = self.client.get(url_for('stats.as_csv'))
        assert response.status_code == 200
