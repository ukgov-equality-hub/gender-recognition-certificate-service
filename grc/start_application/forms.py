from email.policy import default
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, RadioField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email
from grc.utils.form_custom_validators import validateSecurityCode


class SaveYourApplicationForm(FlaskForm):
    email = EmailField(
        'email',
        validators=[
            DataRequired(message='Email address is required'),
            Email(message='A valid email address is required')
        ]
    )

    submit = SubmitField('Continue')


class ValidateEmailForm(FlaskForm):
    code = StringField(
        'code',
        validators=[DataRequired(message='A valid code is required'), validateSecurityCode]
    )

    attempt = IntegerField('attempt', default=0)

    submit = SubmitField('Continue')


class OverseasCheckForm(FlaskForm):
    check = RadioField(
        'check',
        choices=[('Yes'), ('No')],
        validators=[DataRequired(message='Select if you ever been issued a Gender Recognition Certificate')]
    )

    submit = SubmitField('Continue')


class OverseasApprovedCheckForm(FlaskForm):
    check = RadioField(
        'check',
        choices=[('Yes'), ('No')],
        validators=[DataRequired(message='Select if you have official documentation')]
    )

    submit = SubmitField('Continue')


class DeclerationForm(FlaskForm):
    check = BooleanField(
        'check',
        validators=[DataRequired(message='Confirm that you meet requirements')]
    )

    submit = SubmitField('Continue')
