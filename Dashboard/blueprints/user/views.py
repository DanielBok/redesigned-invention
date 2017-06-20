from os import getenv
from urllib.parse import urljoin

import numpy.random as rng
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy_utils.types import Choice

from Dashboard.blueprints.api.models import Drivers, Tasks
from Dashboard.extensions import db
from utils.datetime import now
from utils.setup import secret_seed
from .decorators import anonymous_required
from .forms import LoginForm
from .models import User

user = Blueprint('user', __name__, template_folder='templates')


def _redirect(role, *url):
    red_url = (role + '/' + '/'.join(url)).lower()
    return redirect(urljoin(request.host_url, red_url))


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
                role = u.role.value

                if next_url:
                    return _redirect(role, next_url)

                if role == 'Manager':
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
        Drivers.get_by_identity(current_user.name).stop_work('stop')

    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('user.login'))


@user.route('/secret-route')
def secret_route():
    if request.args.get('key', 'None') != getenv('SECRET_RESET', None):
        return redirect(url_for('.login'))

    secret_seed()

    flash("Seeding is successful", "success")

    return redirect(url_for('.login'))


@user.route('/clear-route')
def clear_route():
    tasks = (Tasks.query
             .filter((Tasks.flight_time <= now()) &
                     (Tasks.status != Choice('done', 'Done')))
             .all())

    drivers = Drivers.get_all_drivers_names()
    for task in tasks:
        if task.driver is None:
            task.driver = rng.choice(drivers)
        if task.task_start_time is None:
            task.task_start_time = now()
        task.completed_time = now()
        task.status = Choice('done', 'Done')
        task.task_time_taken = -1
        db.session.add(task)

    tasks = (Tasks.query
             .filter(
        (
            (Tasks.ready_time >= now()) &
            (Tasks.status != Choice('ready', 'Ready'))
        ) |
        (
            (Tasks.flight_time >= now()) &
            (Tasks.ready_time <= now())
        )
    )
             .all())

    for task in tasks:
        task.status = Choice('ready', 'Ready')
        task.driver = None
        task.task_start_time = None
        db.session.add(task)

    db.session.commit()

    flash("Clearing is successful", "success")

    return redirect(url_for('.login'))
