def _hidden_env_data():
    import os
    from os.path import dirname, join, abspath

    grab = os.environ.get
    root_folder = abspath(join(dirname(__file__), '..'))

    data = {
        'DEBUG': grab('DEBUG', True),
        'DEBUG_TB_INTERCEPT_REDIRECTS': grab('DEBUG_TB_INTERCEPT_REDIRECTS', False),
        'SECRET_KEY': grab('SECRET_KEY', os.urandom(128).hex()),
        'SERVER_NAME': grab('SERVER_NAME', 'localhost:5000'),
        'SQLALCHEMY_DATABASE_URI': grab('DATABASE_URL',
                                        "sqlite:///{path}".format(path=join(root_folder, 'app_data', 'data.db'))),

    }

    return data


_data = _hidden_env_data()

DEBUG = _data['DEBUG']
DEBUG_TB_INTERCEPT_REDIRECTS = _data['DEBUG_TB_INTERCEPT_REDIRECTS']
SECRET_KEY = _data['SECRET_KEY']
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = _data['SQLALCHEMY_DATABASE_URI']
TIMEZONE = 'Asia/Singapore'
SERVER_NAME = _data['SERVER_NAME']
