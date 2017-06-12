from Dashboard.blueprints.user.models import User
from utils.tests_helpers import TestMixin


class TestModels(TestMixin):
    def test_authenticate(self, users):
        u = User.find_by_identity('manager')

        message = "<User Username: {0} Role: {1} Name: {2}".format(u.username, u.role, u.name)
        assert str(u) == message
        assert u.authenticate('Fake PASSWORD', use_password=False) is True
        assert u.authenticate('Fake Password') is False
