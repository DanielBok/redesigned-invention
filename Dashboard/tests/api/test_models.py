from Dashboard.blueprints.api.models import Drivers
from utils.tests_helpers import TestMixin, AssertsMixin


class TestModels(TestMixin, AssertsMixin):
    def test_drivers_update(self):

        d = Drivers.get_by_identity('Stan Mohan')
        d.ready()

        assert d.status.code == 'on'

        d.stop_work('break')
        assert d.status.code == 'break'

        d.stop_work('stop')
        assert d.status.code == 'off'
