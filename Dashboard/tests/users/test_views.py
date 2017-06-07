from flask import url_for
from utils.tests_helpers import TestMixin, AssertsMixin


class TestUsers(TestMixin, AssertsMixin):
    def test_login_page(self):
        response = self.client.get(url_for('user.login'))
        assert response.status_code == 200

    def test_login(self):
        response = self.login()
        print(response.data)
        assert response.status_code == 200

    def test_logout(self):
        self.login()
        response = self.logout()
        self.assert_with_message(200, response, '')
