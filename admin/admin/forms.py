from flask_wtf import FlaskForm
from wtforms import HiddenField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    action = HiddenField('action')
    email = EmailField(
        'email',
        validators=[DataRequired(message='Email address is required'), Email(message='A valid email address is required')]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(message='Please enter your password')]
    )
    submit = SubmitField('Login')
