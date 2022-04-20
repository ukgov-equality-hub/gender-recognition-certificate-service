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
        validators=[DataRequired(message='Enter the security code that we emailed you'), validateSecurityCode]
    )

    attempt = IntegerField('attempt', default=0)


class IsFirstVisitForm(FlaskForm):
    isFirstVisit = RadioField(
        choices=[
            ('FIRST_VISIT', "No"),
            ('HAS_REFERENCE', "Yes, and I have my reference number"),
            ('LOST_REFERENCE', "Yes, but I have lost my reference number")
        ],
        validators=[DataRequired(message='Select if you have already started an application')]
    )

    reference = StringField(
        validators=[StrictRequiredIf('isFirstVisit', 'HAS_REFERENCE', message='Enter a reference number', validators=[validateReferenceNumber])],
    )


class OverseasCheckForm(FlaskForm):
    overseasCheck = RadioField(
        choices=[('Yes', 'Yes'), ('No', 'No')],
        validators=[DataRequired(message='Select if you ever been issued a Gender Recognition Certificate')]
    )


class OverseasApprovedCheckForm(FlaskForm):
    overseasApprovedCheck = RadioField(
        choices=[('Yes', 'Yes'), ('No', 'No')],
        validators=[DataRequired(message='Select if you have official documentation')]
    )


class DeclerationForm(FlaskForm):
    consent = BooleanField(
        validators=[DataRequired(message='You must consent to the General Register Office contacting you')]
    )
