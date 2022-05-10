from flask_wtf import FlaskForm
from wtforms import EmailField
from wtforms.validators import DataRequired, Email


class ForgotPasswordForm(FlaskForm):
    email_address = EmailField(
        validators=[
            DataRequired(message='Enter your email address'),
            Email(message='Enter a valid email address')
        ]
    )
