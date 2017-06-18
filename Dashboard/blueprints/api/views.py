from datetime import timedelta as td

from flask import Blueprint, request, redirect, jsonify
from flask_restful import Api, Resource

from Dashboard.extensions import csrf
from utils.datetime import now
from .models import Drivers, Flights, Tasks

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


class TasksCtrl(Resource):
    def get(self):
        type_ = request.args.get('type')  # request was too huge
        if type_ == 'all':
            tasks = Tasks.get_all_tasks_since(now() - td(hours=1), (now() + td(hours=2)))
        else:
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
            d.stop_work(activity)

        elif activity in {'start', 'complete'}:
            d.ready(activity)

        elif activity in {'update'}:
            new_task_id = data['target']
            d.update_task(new_task_id)
        else:
            return jsonify({
                'driver': {
                    'name': d.name_,
                    'status': d.status.value,
                    'task_id': d.task_id
                },
                'task': None,
                'error': 'Activity not recognized'
            })

        return jsonify({
            'driver': {
                'name': d.name_,
                'status': d.status.value,
                'task_id': d.task_id
            },
            'task': d.get_task()
        })


api.add_resource(FlightsCtrl, '/flights')
api.add_resource(TasksCtrl, '/tasks')
api.add_resource(DriversCtrl, '/drivers')
