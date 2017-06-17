from collections import defaultdict
from datetime import datetime as dt, timedelta as td

import pandas as pd
from numpy import random as rng
from sqlalchemy_utils.types import ChoiceType, Choice

from Dashboard.extensions import db
from utils.datetime import now
from utils.mixins import ResourceMixin, AwareDateTime


class Flights(ResourceMixin, db.Model):
    TYPES = [
        ('A', 'Arrival'),
        ('D', 'Departure')
    ]

    __tablename__ = 'flights'

    id = db.Column(db.Integer(), primary_key=True)
    flight_num = db.Column(db.String(10), nullable=False)
    terminal = db.Column(db.String(5), nullable=False)

    scheduled_time = db.Column(AwareDateTime(), nullable=False)
    actual_time = db.Column(AwareDateTime(), nullable=False)

    type_ = db.Column(ChoiceType(TYPES), nullable=False)
    pax = db.Column(db.Integer, nullable=False, default=0)
    num_containers = db.Column(db.Integer, nullable=False, default=0)
    bay = db.Column(db.String(5), nullable=False)

    def __init__(self, **kwargs):
        super(Flights, self).__init__(**kwargs)

    def to_dict(self):
        return {
            'flight_num': self.flight_num,
            'terminal': self.terminal,
            'scheduled_time': self.scheduled_time,
            'type': self.type_.value,
            'containers': self.num_containers,
            'actual_time': self.actual_time,
            'bay': self.bay
        }

    @classmethod
    def update_arrival_time(cls):
        records = Flights.query.filter(
            ((now() + td(minutes=30) > Flights.scheduled_time) & (now() + td(hours=4) <= Flights.scheduled_time))
        ).all()
        noise = rng.normal(0, 5, len(records))
        for r, n in zip(records, noise):
            r.time += td(minutes=n)
            db.session.add(r)
        db.session.commit()

    @classmethod
    def get_flight_from_time(cls, start: dt, forecast=4):
        results = Flights.query.filter(
            (Flights.scheduled_time >= start) & (Flights.scheduled_time <= start + td(hours=forecast))).all()

        return [i.to_dict() for i in results]


class Drivers(ResourceMixin, db.Model):
    ACTIVITIES = [
        ('ready', 'Ready'),
        ('on', 'On Task'),
        ('off', 'Off Work'),
        ('break', 'Break'),
        ('na', 'Not applicable')
    ]

    __tablename__ = 'driver'
    id = db.Column(db.Integer(), primary_key=True)
    name_ = db.Column(db.String(128), nullable=False, index=True)
    task_id = db.Column(db.Integer(), nullable=True, default=None)

    # Activity tracking
    status = db.Column(ChoiceType(ACTIVITIES), nullable=False, server_default="off")

    def __init__(self, **kwargs):
        super(Drivers, self).__init__(**kwargs)

    def get_task(self):
        if self.task_id is None:
            return None
        return Tasks.get_task_by_id(self.task_id).to_dict()

    def ready(self, activity='start'):
        self.status = Choice('ready', 'Ready')  # put to ready

        if activity == 'complete':
            task = Tasks.get_task_by_id(self.task_id)
            task.complete_task()
            self.task_id = None

        task = Tasks.get_first_task()  # get task
        if task is not None:  # if there is task, give driver task
            self.task_id = task.id
            task.do_task(self)
            self.status = Choice('on', 'On Task')

        return self.save()

    def update_task(self, new_task_id):
        Tasks.get_task_by_id(self.task_id).return_task()  # get old task id

        self.task_id = new_task_id  # set new task
        self.status = Choice('on', 'On Task')

        Tasks.get_task_by_id(new_task_id).do_task(self)

        return self.save()

    def stop_work(self, type_: str):
        """
        Stops work and returns task to Task queue
        :param type_: type of stop. Break or off work
        :return: self
        """

        if type_.lower() == 'break':
            self.status = Choice('break', 'Break')
        elif type_.lower() == 'stop':
            self.status = Choice('off', 'Off Work')
        else:
            raise ValueError('type_ argument is not recognized')

        if self.task_id is not None:
            task = Tasks.get_task_by_id(self.task_id)
            task.driver = None
            task.return_task()
            self.task_id = None

        return self.save()

    @classmethod
    def get_by_identity(cls, identity: str) -> 'Drivers':
        return Drivers.query.filter(Drivers.name_ == identity).first()

    @classmethod
    def get_working_drivers(cls):
        return [{'name': d.name_, 'status': d.status.value, 'task_id': d.task_id}
                for d in Drivers.query.filter(Drivers.status != 'off').all()]

    @classmethod
    def get_all_drivers(cls):
        return [{'name': d.name_, 'status': d.status.value, 'task_id': d.task_id}
                for d in Drivers.query.all()]


class Tasks(ResourceMixin, db.Model):
    STATUSES = [
        ('ready', 'Ready'),
        ('er', 'En-route'),
        ('done', 'Done')
    ]

    __tablename = 'tasks'

    # Task info
    id = db.Column(db.Integer(), primary_key=True)
    status = db.Column(ChoiceType(STATUSES), nullable=False, index=True, default='ready')
    ready_time = db.Column(AwareDateTime(), index=True)
    flight_time = db.Column(AwareDateTime(), index=True)

    # Performance Info
    task_start_time = db.Column(AwareDateTime(), index=True)
    completed_time = db.Column(AwareDateTime(), index=True)
    task_time_taken = db.Column(db.Integer(), default=-1)

    # Containers info
    source = db.Column(db.String(10), nullable=False)
    destination = db.Column(db.String(10), nullable=False)
    containers = db.Column(db.Integer, nullable=False, index=True)
    bay = db.Column(db.String(5), nullable=False)

    # Driver details
    driver = db.Column(db.String(50), nullable=True)

    def __init__(self, **kwargs):
        super(Tasks, self).__init__(**kwargs)

    def __str__(self):
        msg = 'TASK DATA\n' + '\n'.join("{0}\t {1}".format(str(k), str(v)) for k, v in self.to_dict().items())
        return msg

    def to_dict(self, purpose: str = None):
        payload = {
            'task_id': self.id,
            'ready_time': self.ready_time,
            'flight_time': self.flight_time,
            'status': self.status.value,
            'source': self.source,
            'destination': self.destination,
            'containers': self.containers,
            'driver': self.driver
        }

        if purpose and purpose.startswith("stats"):
            payload.update({
                "time_taken": self.task_time_taken
            })
            payload.pop('status')
        return payload

    def do_task(self, driver: Drivers):
        self.driver = driver.name_
        self.status = Choice('er', 'En-route')
        self.task_start_time = now()
        return self.save()

    def return_task(self):
        self.status = Choice('ready', 'Ready')
        self.driver = None
        self.task_start_time = None
        return self.save()

    def complete_task(self):
        self.status = Choice('done', 'Done')
        self.completed_time = now()
        self.save()
        self.task_time_taken = (self.completed_time - self.task_start_time).total_seconds()
        return self.save()

    @classmethod
    def get_first_task(cls, forecast=4) -> 'Tasks':
        return (Tasks.query
                .filter((Tasks.ready_time <= now() + td(hours=forecast)) &
                        (Tasks.status == Choice('ready', 'Ready')) &
                        (Tasks.flight_time >= now()))
                .order_by(Tasks.ready_time)
                .first())

    @classmethod
    def get_task_by_id(cls, task_id) -> 'Tasks':
        return (Tasks.query
                .filter(Tasks.id == task_id)
                .first())

    @classmethod
    def get_all_tasks_since(cls, start: dt, stop: dt = None):
        if stop is None:
            stop = now()
        records = (Tasks.query
                   .filter(((Tasks.ready_time >= start) &
                            (Tasks.ready_time <= stop)) |
                           (Tasks.status == Choice('er', 'En-route')))
                   .order_by(Tasks.ready_time)
                   .all())
        return [t.to_dict() for t in records]

    @classmethod
    def get_all_undone_tasks(cls, forecast=4):
        records = (Tasks.query
                   .filter((Tasks.status == Choice('ready', 'Ready')) &
                           (Tasks.ready_time <= now() + td(hours=forecast)))
                   .all())
        return [t.to_dict() for t in records]

    @classmethod
    def get_all_tasks(cls, purpose=None):
        return [t.to_dict(purpose) for t in Tasks.query.all()]

    @classmethod
    def get_all_done_tasks(cls):
        return [t.to_dict('stats') for t in Tasks.query.filter(Tasks.status == Choice('done', 'Done')).all()]

    @classmethod
    def get_all_drivers(cls):
        return [t[0] for t in Tasks.query.with_entities(Tasks.driver).distinct(Tasks.driver).all()]

    @classmethod
    def get_driver_stats(cls, driver, jsonify=True):
        data = defaultdict(list)
        for t in Tasks.query.filter((Tasks.status == Choice('done', 'Done')) &
                                            (Tasks.driver == driver)).all():
            for k, v in t.to_dict('stats').items():
                if k in {'status', 'task_id', 'driver'}:
                    continue
                if jsonify and type(v) == dt:
                    v = v.isoformat()
                data[k].append(v)
        return {driver: data}

    @classmethod
    def get_tasks_data(cls):
        data = [t.to_dict('stats') for t in Tasks.query.filter(Tasks.status == Choice('done', 'Done')).all()]
        columns = data[0].keys()
        return pd.DataFrame(data, columns=columns)
