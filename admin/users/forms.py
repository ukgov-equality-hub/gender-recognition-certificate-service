from flask_wtf import FlaskForm
from wtforms import EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


class UsersForm(FlaskForm):
    email = EmailField(
        'email',
        validators=[
            DataRequired(message='Email address is required'),
            Email(message='A valid email address is required')
        ]
    )

    userType = BooleanField('check')

    submit = SubmitField('Submit')
