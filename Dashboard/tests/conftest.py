from os.path import abspath, dirname, join, exists
import os

import pytest

from Dashboard.app import create_app
from database_utils.setup import seed

ROOT_FOLDER = abspath(join(dirname(__file__), '..'))
TEST_DB_PATH = join(ROOT_FOLDER, 'app_data', 'data.db')
TEST_DB_URI = "sqlite:///" + TEST_DB_PATH


@pytest.yield_fixture(scope='session')
def app():
    params = {
        'DEBUG': False,
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DB_URI
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
    :param app: PyTest fixture
    :return: Flask app client
    """
    yield app.test_client()


# @pytest.fixture(scope='session')
# def db(app, request):
#     if not exists(TEST_DB_PATH):
#         seed(create_app({'SQLALCHEMY_DATABASE_URI': TEST_DB_URI}))

