from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, BooleanField
from wtforms.validators import DataRequired
from grc.business_logic.data_structures.submit_and_pay_data import HelpWithFeesType
from grc.utils.form_custom_validators import StrictRequiredIf, validateHWFReferenceNumber


class MethodCheckForm(FlaskForm):
    applying_for_help_with_fee = RadioField(
        choices=[
            (True, 'Yes'),
            (False, 'No, I will pay now')
        ],
        validators=[DataRequired(message='Select if you are applying for help paying the fee')]
    )


class HelpTypeForm(FlaskForm):
    how_applying_for_fees = RadioField(
        choices=[
            (HelpWithFeesType.USING_ONLINE_SERVICE.name, 'Using the online service'),
            (HelpWithFeesType.USING_EX160_FORM.name, 'Using the EX160 form')
        ],
        validators=[DataRequired(message='Select how are you applying for help paying the fee')]
    )

    help_with_fees_reference_number = StringField(
        validators=[
            StrictRequiredIf(
                'how_applying_for_fees',
                HelpWithFeesType.USING_ONLINE_SERVICE.name,
                message='Enter your Help with Fees reference number'
            ),
            validateHWFReferenceNumber
        ]
    )


class CheckYourAnswers(FlaskForm):
    certify = BooleanField(
        validators=[DataRequired(message='You must certify that all information given in this application is correct and that you understand making a false application is an offence.')]
    )
