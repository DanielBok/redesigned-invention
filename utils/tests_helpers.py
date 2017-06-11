import pytest
from flask import url_for, Response


class AssertsMixin:
    @staticmethod
    def assert_with_message(status_code: int, response: Response, message: str = None):
        assert response.status_code == status_code
        assert message in str(response.data)


class TestMixin(object):
    """
    Automatically load in a session and client, this is common for a lot of
    tests that work with views.
    """

    @pytest.fixture(autouse=True)
    def set_common_fixtures(self, client, users):
        self.client = client
        self.users = users

    def login(self, identity='manager', password='test') -> Response:
        """
        Login a specific user.
        :return: Flask response
        """
        user = {
            'identity': identity,
            'password': password
        }

        response = self.client.post(url_for('user.login'), data=user, follow_redirects=True)

        return response

    def logout(self) -> Response:
        """
        Logout a specific user.
        :return: Flask response
        """
        response = self.client.get(url_for('user.logout'), follow_redirects=True)
        return response
