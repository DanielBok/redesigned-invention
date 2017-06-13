import os
from os import getenv
from os.path import abspath, dirname, join

DEBUG = getenv('DEBUG', True)
DEBUG_TB_INTERCEPT_REDIRECTS = getenv('DEBUG_TB_INTERCEPT_REDIRECTS', False)
SECRET_KEY = getenv('SECRET_KEY', os.urandom(128).hex())
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL',
                                 "sqlite:///{0}".format(abspath(join(dirname(__file__), '..', 'app_data', 'data.db'))))
TIMEZONE = 'Asia/Singapore'
SERVER_NAME = getenv('SERVER_NAME', 'localhost:5000')
ROOT_FOLDER = abspath(join(dirname(__file__), '..'))
