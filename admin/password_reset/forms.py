from flask_wtf import FlaskForm
from wtforms import HiddenField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from grc.utils.form_custom_validators import validatePasswordStrength


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        'password',
        validators=[DataRequired(message='Please enter a new password'), validatePasswordStrength]
    )

    confirmPassword = PasswordField(
        'confirmPassword',
        validators=[
            DataRequired(message='Please confirm your password'),
            EqualTo('password', message='Passwords must match')
        ]
    )

    submit = SubmitField('Reset')
