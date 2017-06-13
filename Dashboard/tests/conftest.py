import pytest

from Dashboard.app import create_app
from Dashboard.blueprints.api.models import Drivers, Tasks, Flights
from Dashboard.blueprints.user.models import User
from Dashboard.extensions import db as _db
from configs.settings import SQLALCHEMY_DATABASE_URI
from .data_for_test import U_all, D_drivers, T_tasks, F_flights


@pytest.yield_fixture(scope='session')
def app():
    db_uri = SQLALCHEMY_DATABASE_URI.replace('data.db', 'data_test.db')
    params = {
        'DEBUG': False,
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': db_uri
    }

    _app = create_app(settings_override=params)
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def client(app):
    """
    Setup an app client which gets passed to each test function
    :param app: PyTest Fixture
    :return: Flask app client
    """
    yield app.test_client()


@pytest.fixture(scope='session')
def db(app):
    """
    Setup database. This only gets executed once per session
    :param app: PyTest Fixture
    :return: SQLAlchemy database session
    """

    _db.drop_all()
    _db.create_all()

    # Add users
    for u in U_all:
        _db.session.add(User(**u))

    # Add driver
    for d in D_drivers:
        _db.session.add(Drivers(**d))

    # Add tasks
    for t in T_tasks:
        _db.session.add(Tasks(**t))

    for f in F_flights:
        _db.session.add(Flights(**f))

    _db.session.commit()

    return _db


@pytest.fixture(scope='function')
def tasks(db):
    yield db

    db.session.query(Tasks).delete()

    for t in T_tasks:
        db.session.add(Tasks(**t))

    db.session.commit()


@pytest.fixture(scope='function')
def drivers(db):
    yield db

    db.session.query(Drivers).delete()

    for d in D_drivers:
        db.session.add(Drivers(**d))

    db.session.commit()
