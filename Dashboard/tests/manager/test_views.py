from flask import url_for

from utils.tests_helpers import TestMixin, AssertsMixin


class TestViews(TestMixin, AssertsMixin):
    def test_index_redirect(self):
        self.login()
        response = self.client.get(url_for('manager.index'))
        target = url_for('manager.flight_schedules')
        self.assert_redirect(response, target)

    def test_controller(self):
        self.login()
        response = self.client.get(url_for('manager.driver_controller'))
        assert response.status_code == 200

    def test_allocation(self):
        response = self.login(next='allocation')
        self.assert_with_message(200, response, 'Allocation')

    def test_manpower(self):
        response = self.login(next='manpower')
        self.assert_with_message(200, response, 'Manpower')

    def test_taskboard(self):
        response = self.login(next='taskboard')
        self.assert_with_message(200, response, 'Taskboard')
