import pickle
from json import dumps
from os.path import exists
from time import time

from flask import Blueprint, render_template
from werkzeug.contrib.cache import SimpleCache

from Dashboard.blueprints.api.models import Tasks

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


@stats.route('/dpdata', methods=['GET', 'POST'])
def driver_performance_data():
    t = time()
    if exists('s.p'):
        with open('s.p', 'rb') as f:
            data = pickle.load(f)
        print('pickles', time() - t)
        return data

    data = cache.get('dp-data')
    if data is None:
        data = {}
        drivers = Tasks.get_all_drivers()
        for d in drivers:
            data.update(Tasks.get_driver_stats(d))

        data['drivers'] = drivers
        data = dumps(data)
        cache.set('dp-data', data)
        with open('s.p', 'wb') as f:
            pickle.dump(data, f)
    print(time() - t)
    return data
