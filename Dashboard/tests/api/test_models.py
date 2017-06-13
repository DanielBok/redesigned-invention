from datetime import timedelta as td

from Dashboard.blueprints.api.models import Tasks
from Dashboard.tests.data_for_test import T_tasks
from utils.datetime import now
from utils.tests_helpers import TestMixin, AssertsMixin


class TestModels(TestMixin, AssertsMixin):
    def test_get_all_tasks_since(self):
        start = now() + td(minutes=20)
        end = now() + td(minutes=40)

        counts = 0
        for t in T_tasks:
            if start <= t['ready_time'] <= end:
                counts += 1

        tasks_ = Tasks.get_all_tasks_since(start, end)

        assert len(tasks_) == counts

