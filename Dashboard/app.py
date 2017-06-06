from flask import Flask

from Dashboard.blueprints.api import api
from Dashboard.blueprints.manager import managers
from Dashboard.blueprints.user import user
from Dashboard.blueprints.user.models import User
from Dashboard.extensions import login_manager, db, csrf
from Dashboard.blueprints.driver import driver


def create_app(settings_override=None):
    """
    Create the flask app with required settings
    :param settings_override: (dict) overrides settings file
    :return: Flask app
    """

    app = Flask(__name__, instance_relative_config=True, static_folder="./static")
    app.config.from_object('configs.settings')

    if settings_override:
        app.config.update(settings_override)

    # Register blueprints here
    app.register_blueprint(user)
    app.register_blueprint(managers, url_prefix='/manager')
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(driver, url_prefix='/driver')

    # Extend app to use other 3rd-party flask libraries
    login_manager.init_app(app)
    db.init_app(app)
    csrf.init_app(app)

    # authentication setup
    authentication(app, User)

    return app


def authentication(app, user_model):
    """
    Initialize Flask-Login extension (mutates the app instance passed in). Methods imposed are required "overwrites"
     over the base Flask-Login abstract methods
    :param app: app instance
    :param user_model: SQL User model
    :return: app instance
    """

    login_manager.login_view = 'user.login'  # the login driver

    @login_manager.user_loader
    def load_user(uid):
        return user_model.query.get(uid)

    return app
