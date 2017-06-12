import pytest

from Dashboard.app import create_app
from Dashboard.blueprints.api.models import Drivers, Tasks, Flights
from Dashboard.blueprints.user.models import User
from Dashboard.extensions import db as _db
from configs.settings import SQLALCHEMY_DATABASE_URI
from .data_for_test import U_all, D_driver, T_tasks, F_flights


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
    _db.session.add(Drivers(**D_driver))

    # Add tasks
    for t in T_tasks:
        _db.session.add(Tasks(**t))

    for f in F_flights:
        _db.session.add(Flights(**f))

    _db.session.commit()

    return _db


# @pytest.yield_fixture(scope='function')
# def session(db):
#     """
#     Speeds up tests by using rollbacks and nested sessions. Requires that database support SQL savepoints. Postgres
#     does.
#
#     Read more at:
#     http://stackoverflow.com/a/26624146
#     :param db: Pytest Fixture
#     :return: None
#     """
#     db.session.begin_nested()
#
#     yield db.session
#
#     db.session.rollback()


@pytest.fixture(scope='function')
def users(db):
    """
    Create user fixtures. They reset per test
    :param db: PyTest Fixture
    :return: SQLAlchemy database session
    """
    db.session.query(User).delete()

    for u in U_all:
        db.session.add(User(**u))

    db.session.commit()

    return db
