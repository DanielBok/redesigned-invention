from os.path import abspath, dirname, join

import pandas as pd
from flask import Blueprint, request, redirect, jsonify
from flask_restful import Api, Resource
from Dashboard.extensions import csrf

from utils import now
from .models import Drivers, Flights, Tasks
from .optimizer import fcfs

api_bp = Blueprint('api', __name__)
api = Api(api_bp, decorators=[csrf.exempt])


@api_bp.before_request
def before_request():
    # Flights.update_arrival_time()  # TODO find some way to add noise to mimic actual arriving time
    url = request.path
    if url.endswith('/') and url != '/':
        return redirect(url[:-1])


class FlightsCtrl(Resource):
    def get(self):
        forecast = request.args.get('forecast', 4)

        results = Flights.get_flight_from_time(now(), forecast)
        return jsonify({
            'schedule': results
        })


class Schedule(Resource):
    def get(self):
        start = now()
        forecast = request.args.get('forecast', 4)
        root_dir = abspath(join(dirname(__file__), '..', '..', '..', 'app_data'))
        df = pd.read_pickle(join(root_dir, 'flights.p'))
        results = fcfs(df, start, forecast)

        return jsonify({
            'data': results
        })


class TasksCtrl(Resource):
    def get(self):
        tasks = Tasks.get_all_undone_tasks()
        return jsonify({
            'tasks': tasks
        })


class DriversCtrl(Resource):
    def get(self):
        type_ = request.args.get('type', 'working')  # valid type_ = ['working', 'all']
        if type_ == 'all':
            records = Drivers.get_all_drivers()
        else:
            records = Drivers.get_working_drivers()

        return jsonify({
            'drivers': records
        })

    def post(self):
        data = request.get_json()
        identity = data['name']
        activity = data['activity'].lower()
        d = Drivers.get_by_identity(identity)

        if activity in {'stop', 'break'}:
            task_id = None
            if activity == 'stop':
                task_id = d.stop_work()
            if activity == 'break':
                task_id = d.pause()

            if task_id is not None:
                Tasks.get_task_by_id(task_id).unset_task()

        task_dict = None
        if activity in {'start', 'complete'}:
            d.ready()
            task = Tasks.get_first_task()
            if task is not None:
                task.set_driver(d.name_)
                d.update_task(task.id)

            task_dict = task.to_dict()

        result = {
            'driver': {
                'name': d.name_,
                'status': d.status.value
            },
            'task': task_dict
        }

        return jsonify({
            'driver': result
        })


api.add_resource(Schedule, '/schedule')
api.add_resource(FlightsCtrl, '/flights')
api.add_resource(TasksCtrl, '/tasks')
api.add_resource(DriversCtrl, '/drivers')
