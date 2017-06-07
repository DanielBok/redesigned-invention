from flask import url_for


class TestUsers(object):
    def test_login_page(self, client):
        response = client.get(url_for('user.login'))
        assert response.status_code == 200
