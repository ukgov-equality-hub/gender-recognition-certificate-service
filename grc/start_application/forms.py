from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, RadioField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email
from grc.utils.form_custom_validators import validateSecurityCode, validateReferenceNumber, StrictRequiredIf


class SaveYourApplicationForm(FlaskForm):
    email = EmailField(
        validators=[
            DataRequired(message='Email address is required'),
            Email(message='A valid email address is required')
        ],
    )


class ValidateEmailForm(FlaskForm):
    code = StringField(
        'code',
        validators=[DataRequired(message='A valid code is required'), validateSecurityCode]
    )

    attempt = IntegerField('attempt', default=0)

    submit = SubmitField('Continue')


class IsFirstVisitForm(FlaskForm):
    isFirstVisit = RadioField(
        choices=[
            ('FIRST_VISIT', "No, this is my first visit"),
            ('HAS_REFERENCE', "Yes, I have started an application and have my reference number"),
            ('LOST_REFERENCE', "Yes, I have started an application, but I have lost my reference number")
        ],
        validators=[DataRequired(message='Select if you have already started an application')]
    )

    reference = StringField(
        validators=[StrictRequiredIf('isFirstVisit', 'HAS_REFERENCE', message='Enter a reference number', validators=[validateReferenceNumber])],
        default=''
    )


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
