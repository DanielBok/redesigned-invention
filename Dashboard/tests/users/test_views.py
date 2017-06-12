from flask import url_for

from utils.tests_helpers import TestMixin, AssertsMixin


class TestViews(TestMixin, AssertsMixin):
    def test_index_redirect(self):
        response = self.client.get(url_for('user.index'))
        target = url_for('user.login')
        self.assert_redirect(response, target)

    def test_login_page(self):
        response = self.client.get(url_for('user.login'))
        assert response.status_code == 200

    def test_login(self):
        response = self.login()
        assert response.status_code == 200

    def test_logout(self):
        self.login()
        response = self.logout()
        self.assert_with_message(200, response, '')

    def test_login_with_next_fail(self):
        response = self.login(next='/random_url')
        assert response.status_code == 404

    def test_login_with_next_manager(self):
        response = self.login(next='/flight-schedules', follow_redirects=False)
        target = url_for('manager.flight_schedules')
        self.assert_redirect(response, target)

    def test_login_driver(self):
        response = self.login('driver', follow_redirects=False)
        target = url_for('driver.index')
        self.assert_redirect(response, target)

    def test_fail_login(self):
        response = self.login('driver', 'BAD_PASSWORD')
        self.assert_with_message(200, response, 'Username or password does not match')

    def test_logout_driver(self):
        self.login('driver', follow_redirects=False)
        response = self.logout(follow_redirects=False)
        target = url_for('user.login')
        self.assert_redirect(response, target)

    def test_anon_required_redirect(self):
        self.login('driver', follow_redirects=False)
        response = self.client.get(url_for('user.login'))
        target = url_for('driver.index')
        self.assert_redirect(response, target)

    def test_redirect_due_to_roles(self):
        self.login('driver', follow_redirects=False)
        response = self.client.get(url_for('manager.index'))

        fake_target = url_for('manager.index')
        assert response.location != fake_target
        self.assert_redirect(response, url_for('driver.index'))
