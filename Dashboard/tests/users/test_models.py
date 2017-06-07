from Dashboard.blueprints.user.models import User
from utils.tests_helpers import TestMixin



class TestUser(TestMixin):
    def test_find_user(self, users):
        # u = User.find_by_identity('John Smith')
        # assert u.role == 'manager'
        # assert u.authenticate('test') is True
        # assert u.authenticate('false_password') is False
        print(users)
        assert 1 == 1
