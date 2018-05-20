from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Email, ValidationError, IPAddress, DataRequired
from app.database import db


def check_user_unique(form, username):
    if username.data in user_credentials:
        raise ValidationError('User exists')

def check_user_exists(form, username):
    user = db.get_client(username.data)
    if not user:
        raise ValidationError('User doesn\'t exist')

def check_password(form, password):
    if password.data != user_credentials[form.name.data]:
        raise ValidationError('Wrong password')


class SignUpForm(FlaskForm):
    name = TextField('name', validators=[Required()])
    email = TextField('email', validators=[Required(), Email(message='Wrong email format')])
    password = PasswordField('password', validators=[Required()])

    def validate_username(self, name):
        user = db.get_client(name)
        if user is not None:
            raise ValidationError('Please use a different username.')


class LoginForm(FlaskForm):
    name = TextField('name', validators=[Required(), check_user_exists])
    password = PasswordField('password', validators=[Required()])

    def validate_username(self, name):
        user = db.get_client(name)
        if user is not None:
            raise ValidationError('Invalid username or bad password.')

class AddServiceForm(FlaskForm):
    ip = TextField('ip', validators=[Required(), IPAddress(ipv4=True, message='Please input valid IP')])

