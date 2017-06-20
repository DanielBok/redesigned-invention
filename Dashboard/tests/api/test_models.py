from datetime import timedelta as td

from Dashboard.blueprints.api.models import Tasks, Drivers
from Dashboard.tests.data_for_test import T_tasks, D_drivers
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

    def test_get_all_drivers_names(self):
        drivers = Drivers.get_all_drivers_names()
        assert len(drivers) == len(D_drivers)

    def test_task_to_string(self):
        task = Tasks.get_first_task()
        assert str(task).startswith("TASK DATA")

    def test_task_to_dict_stats(self):
        task = Tasks.get_first_task()
        d = task.to_dict('stats')
        assert 'time_taken' in d.keys()
        assert 'status' not in d.keys()

    def test_get_all_tasks(self):
        tasks = Tasks.get_all_tasks()
        assert len(tasks) == len(T_tasks)

        tasks = Tasks.get_all_done_tasks()
        assert len(tasks) == 0
        task = Tasks.get_first_task()

        task.do_task(Drivers.get_by_identity("John Smith"))
        task.complete_task()

        tasks = Tasks.get_all_done_tasks()
        assert len(tasks) == 1

