from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField
from wtforms.validators import DataRequired, Email


class ForgotPasswordForm(FlaskForm):
    email = EmailField(
        'email',
        validators=[
            DataRequired(message='Email address is required'),
            Email(message='A valid email address is required')
        ]
    )

    submit = SubmitField('Submit')
