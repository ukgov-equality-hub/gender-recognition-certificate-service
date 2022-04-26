from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, RadioField, BooleanField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from grc.utils.form_custom_validators import StrictRequiredIf, validatePostcode
from datetime import datetime
from dateutil.relativedelta import relativedelta


class MethodCheckForm(FlaskForm):
    applying_for_help_with_fee = RadioField(
        choices=[
            ('Help', 'Yes'),
            ('Online', 'No, I will pay now')
        ],
        validators=[DataRequired(message='Select if you are applying for help paying the fee')]
    )


class HelpTypeForm(FlaskForm):
    how_applying_for_fees = RadioField(
        choices=[
            ('Using the online service', 'Using the online service'),
            ('Using the EX160 form', 'Using the EX160 form')
        ],
        validators=[DataRequired(message='Select how are you applying for help paying the fee')]
    )

    help_with_fees_reference_number = StringField(
        validators=[StrictRequiredIf('how_applying_for_fees', 'Using the online service', message='Enter your Help with Fees reference number')]
    )


class CheckYourAnswers(FlaskForm):
    certify = BooleanField(
        validators=[DataRequired(message='You must certify that all information given in this application is correct and that you understand making a false application is an offence.')]
    )


class PaymentDetailsForm(FlaskForm):
    card_number = IntegerField(
        'card_number',
        validators=[
            DataRequired(message='A valid card number is required'),
            NumberRange(min=0000000000000000, max=9999999999999999, message='A valid card number is required')
        ]
    )

    month = IntegerField(
        'month',
        validators=[
            DataRequired(message='Expiry date must include a month'),
            NumberRange(min=1, max=12, message='Please enter a valid month')
        ]
    )

    year = IntegerField(
        'year',
        validators=[
            DataRequired(message='Expiry date  must include a year'),
            NumberRange(min=int((datetime.now()).strftime('%y')), max=int((datetime.now() + relativedelta(years=10)).strftime('%y')), message='Please enter a valid year')
        ]
    )

    name = StringField(
        'name',
        validators=[DataRequired(message='Name on card is required')]
    )

    security_code = IntegerField(
        'security_code',
        validators=[
            DataRequired(message='Security code is required'),
            NumberRange(min=000, max=999, message='Please enter a valid security code')
        ]
    )

    building = StringField(
        'building',
        validators=[DataRequired(message='Building is required')]
    )

    street = StringField(
        'street',
        validators=[DataRequired(message='Street is required')]
    )

    town = StringField(
        'town',
        validators=[DataRequired(message='Town or city is required')]
    )

    county = StringField(
        'county',
        validators=[DataRequired(message='County is required')]
    )

    postcode = StringField(
        'postcode',
        validators=[DataRequired(message='A valid postcode is required'), validatePostcode]
    )

    email = EmailField(
        'email',
        validators=[DataRequired(message='Email address is required')]
    )  # Email(message='A valid email address is required')

    submit = SubmitField('Continue')


class PaymentConfirmationForm(FlaskForm):
    submit = SubmitField('Continue')
