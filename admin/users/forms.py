from flask_wtf import FlaskForm
from wtforms import EmailField, BooleanField
from wtforms.validators import DataRequired, Email


class UsersForm(FlaskForm):
    email_address = EmailField(
        validators=[
            DataRequired(message="Enter the new user's email address"),
            Email(message='Enter a valid email address')
        ]
    )

    is_admin_user = BooleanField()
