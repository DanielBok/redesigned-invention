def _hidden_env_data():
    import os
    from os.path import dirname, join, abspath

    root_folder = abspath(join(dirname(__file__), '..'))

    data = {
        'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL',
                                                  "sqlite:///{path}".format(
                                                      path=join(root_folder, 'app_data', 'data.db'))),
    }

    return data


_data = _hidden_env_data()

DEBUG = True
SECRET_KEY = "SECRETKEY!@#$"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = _data['SQLALCHEMY_DATABASE_URI']
TIMEZONE = 'Asia/Singapore'
