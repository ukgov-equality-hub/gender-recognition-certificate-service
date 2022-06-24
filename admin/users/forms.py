from flask_wtf import FlaskForm
from wtforms import EmailField, BooleanField
from wtforms.validators import DataRequired, Email
from grc.utils.form_custom_validators import validateGovUkEmailAddress


class UsersForm(FlaskForm):
    email_address = EmailField(
        validators=[
            DataRequired(message="Enter the new user's email address"),
            Email(message='Enter a valid email address'),
            validateGovUkEmailAddress
        ]
    )

    is_admin_user = BooleanField()
