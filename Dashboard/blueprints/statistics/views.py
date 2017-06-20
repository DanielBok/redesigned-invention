from os.path import exists
from time import time

import pandas as pd
from flask import Blueprint, render_template, jsonify, request, make_response
from werkzeug.contrib.cache import SimpleCache

from Dashboard.blueprints.api.models import Tasks
from Dashboard.extensions import csrf

stats = Blueprint('stats', __name__,
                  template_folder='templates',
                  static_folder='static',
                  static_url_path='/static')

cache = SimpleCache()


@stats.route('/')
def index():
    payload = {
        'title': 'Statistics',
        'page_title': 'Statistics',
        'page_color': 'lime darken-4'
    }
    return render_template('stats/index.html', **payload)


@stats.route('/dpdata')
@csrf.exempt
def driver_performance_data():
    t = time()

    refresh = request.args.get('refresh', 'no').lower() == 'yes'

    if not refresh:
        data = cache.get('dp-data')
        if data is not None:
            return jsonify(data)

    if exists('s.p') and not refresh:
        df = pd.read_pickle('s.p')
    else:
        df = Tasks.get_tasks_data()
        # df.to_pickle('s.p')

    drivers = df.driver.unique().tolist()

    data = {}

    wd = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
    sum_con = df.groupby(df.flight_time.dt.weekday).apply(lambda x: x.containers.sum()).tolist()
    num_weeks = len(df.flight_time.dt.week.unique())

    data['drivers'] = drivers
    data['container_total_by_day'] = {'dow': wd, 'sum': sum_con}
    data['container_mean_by_day'] = {'dow': wd, 'mean': [i / num_weeks for i in sum_con]}

    tdf = df.drop(['task_id'], axis=1)
    tdf.ready_time = tdf.ready_time.map(lambda x: x.isoformat())
    tdf.flight_time = tdf.flight_time.map(lambda x: x.isoformat())

    for driver in drivers:
        data[driver] = (tdf.loc[tdf.driver == driver]
                        .drop(['driver', 'flight_time', 'source'], axis=1)
                        .to_dict('list'))

    cache.set('dp-data', data)
    print(time() - t)

    return jsonify(data)


@stats.route('/as_csv')
def as_csv():
    refresh = request.args.get('refresh', 'no').lower() == 'yes'
    if exists('s.p') and not refresh:
        df = pd.read_pickle('s.p')
    else:
        df = Tasks.get_tasks_data()
        df.to_pickle('s.p')

    csv = df.to_csv(index=False)

    resp = make_response(csv)
    resp.headers["Content-Disposition"] = "attachment; filename={name}.csv".format(name='data')
    resp.headers["Content-type"] = "text/csv"

    return resp
