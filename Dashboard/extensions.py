from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension

login_manager = LoginManager()
db = SQLAlchemy()
csrf = CSRFProtect()
toolbar = DebugToolbarExtension()