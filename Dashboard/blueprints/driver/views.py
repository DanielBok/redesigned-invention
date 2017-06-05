from flask import Blueprint, render_template
from flask_login import login_required

from Dashboard.blueprints.user.decorators import role_required

driver = Blueprint('driver', __name__,
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/static')


@driver.before_request
@login_required
@role_required('driver')
def before_request():
    pass


@driver.route('/')
def index():
    payload = {
        'title': 'Pronto Dashboard',
        'page_title': 'Taskboard',
        'page_color': 'yellow darken-4'
    }
    return render_template('driver/index.html', **payload)
