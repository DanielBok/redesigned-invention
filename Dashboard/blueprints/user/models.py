from flask_login import UserMixin
from sqlalchemy_utils import ChoiceType
from werkzeug.security import generate_password_hash, check_password_hash

from Dashboard.extensions import db
from utils.mixins import ResourceMixin


class User(UserMixin, ResourceMixin, db.Model):
    ROLE = [
        ('driver', 'Driver'),
        ('manager', 'Manager')
    ]

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)

    # Authentication
    role = db.Column(ChoiceType(ROLE), index=True, nullable=False, server_default='driver')
    username = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(256), nullable=False)

    name = db.Column(db.String(128), nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = User.encrypt_password(kwargs.get('password', 'airport'))

    def __str__(self):
        message = "<User Username: {0} Role: {1} Name: {2}".format(self.username, self.role, self.name)
        return message

    def authenticate(self, password='', use_password=True):
        if use_password:
            return check_password_hash(self.password, password)
        return True

    @classmethod
    def encrypt_password(cls, string: str):
        """
        Takes a plain string and hashes it. It's extra for the project
        :param string: plain string
        :return: hashed password
        """
        return generate_password_hash(string)

    @classmethod
    def find_by_identity(cls, identity: str) -> 'User':
        return User.query.filter(User.username == identity).first()
