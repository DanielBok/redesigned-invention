from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    next_page = HiddenField()
    identity = StringField('Username', validators=[DataRequired(), Length(4, 256)])
    password = PasswordField('Password', validators=[DataRequired(), Length(4, 256)])
