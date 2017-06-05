import json

from flask import Blueprint, render_template, redirect, url_for, request, make_response
from flask_login import login_required

from Dashboard.blueprints.user.decorators import role_required

managers = Blueprint('manager', __name__, template_folder='templates')


@managers.before_request
@login_required
@role_required('manager')
def before_request():
    pass


@managers.route('/')
def index():
    return redirect(url_for('.flight_schedules'))


@managers.route('/manpower')
def manpower():
    payload = {
        'title': 'Pronto Dashboard',
        'page_title': 'Manpower',
        'page_color': 'indigo darken-2'
    }
    return render_template('page/manpower.html', **payload)


@managers.route('/allocation')
def allocation():
    payload = {
        'title': 'Pronto Dashboard',
        'page_title': 'Allocation',
        'page_color': 'indigo darken-2'
    }
    return render_template('page/allocation.html', **payload)


@managers.route('/flight-schedules')
def flight_schedules():
    payload = {
        'title': 'Pronto Dashboard',
        'page_title': 'Flight Schedules',
        'page_color': 'indigo darken-2'
    }
    return render_template('page/flight-schedules.html', **payload)


@managers.route('/taskboard')
def taskboard():
    payload = {
        'title': 'Pronto Dashboard',
        'page_title': 'Taskboard',
        'page_color': 'indigo darken-2'
    }
    return render_template('page/taskboard.html', **payload)


@managers.route('/make_csv', methods=['POST'])
def make_csv():
    _data = request.form
    data = json.loads(_data['data'])

    print(data)
    csv = ""

    for d in data:
        if len(csv) == 0:
            csv += ','.join(i.title() for i in d.keys()) + '\n'
        csv += ','.join(str(i) for i in d.values()) + '\n'

    resp = make_response(csv)
    resp.headers["Content-Disposition"] = "attachment; filename={name}.csv".format(name=_data['name'])
    resp.headers["Content-type"] = "text/csv"

    return resp


@managers.errorhandler(404)
def page_not_found(e):
    return None
