from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, BooleanField
from wtforms.validators import DataRequired
from grc.utils.form_custom_validators import StrictRequiredIf


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
