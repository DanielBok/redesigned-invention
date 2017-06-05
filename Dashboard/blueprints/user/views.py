from urllib.parse import urljoin

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user

from Dashboard.blueprints.api.models import Drivers
from .decorators import anonymous_required
from .forms import LoginForm
from .models import User

user = Blueprint('user', __name__, template_folder='templates')


def _redirect(url):
    return redirect(urljoin(request.host_url, url))


@user.route('/')
def index():
    return redirect(url_for('.login'))


@user.route('/login', methods=['GET', 'POST'])
@anonymous_required()
def login():
    form = LoginForm(next_page=request.args.get('next'))

    if form.validate_on_submit():
        u = User.find_by_identity(request.form.get('identity'))
        if u and u.authenticate(request.form.get('password')):
            if login_user(u, remember=True):
                next_url = request.form.get('next')
                if next_url:
                    return _redirect(next_url)

                if u.role.value == 'Manager':
                    return redirect(url_for('manager.index'))
                else:
                    Drivers.get_by_identity(u.name).ready()
                    return redirect(url_for('driver.index'))
        else:
            flash('Username or password does not match', 'error')

    payload = {
        'title': 'Login',
        'page_title': 'Welcome',
        'form': form,
        'page_color': 'teal darken-2'
    }

    return render_template('user/login.html', **payload)


@user.route('/logout')
@login_required
def logout():
    if current_user.role == 'driver':
        Drivers.get_by_identity(current_user.name).stop_work()
    logout_user()
    return redirect(url_for('user.login'))
