from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, Email
from grc.document_checker.doc_checker_state import CurrentlyInAPartnershipEnum
from grc.utils.form_custom_validators import validateSecurityCode


class PreviousNamesCheck(FlaskForm):
    changed_name_to_reflect_gender = RadioField(
        choices=[
            (True, 'Yes'),
            (False, 'No')
        ],
        validators=[DataRequired(message='Select if you have ever changed your name to reflect your gender')]
    )


class MarriageCivilPartnershipForm(FlaskForm):
    currently_in_a_partnership = RadioField(
        choices=[
            (CurrentlyInAPartnershipEnum.MARRIED.name, 'Married'),
            (CurrentlyInAPartnershipEnum.CIVIL_PARTNERSHIP.name, 'Civil partnership'),
            (CurrentlyInAPartnershipEnum.NEITHER.name, 'Neither')
        ],
        validators=[DataRequired(message='Select if you are currently married or in a civil partnership')]
    )


class PlanToRemainInAPartnershipForm(FlaskForm):
    plan_to_remain_in_a_partnership = RadioField(
        choices=[
            (True, 'Yes'),
            (False, 'No')
        ],
        validators=[DataRequired(message='Select if you plan to remain married after receiving your Gender Recognition Certificate')]
    )


class PartnerDiedForm(FlaskForm):
    previous_partnership_partner_died = RadioField(
        choices=[
            (True, 'Yes'),
            (False, 'No')
        ],
        validators=[DataRequired(message='Select if you ever been married or in a civil partnership where your spouse or partner died')]
    )


class PreviousPartnershipEndedForm(FlaskForm):
    previous_partnership_ended = RadioField(
        choices=[
            (True, 'Yes'),
            (False, 'No')
        ],
        validators=[DataRequired(message='Select if you have ever been married or in a civil partnership that has now ended')]
    )


class GenderRecognitionOutsideUKForm(FlaskForm):
    gender_recognition_outside_uk = RadioField(
        choices=[
            (True, 'Yes'),
            (False, 'No')
        ],
        validators=[DataRequired(message='Select if you have received gender recognition in one of these countries or territories')]
    )


class EmailForm(FlaskForm):
    email = EmailField(
        'email',
        validators=[DataRequired(message='Email address is required'), Email(message='A valid email address is required')]
    )

    submit = SubmitField('Continue')


class ValidateEmailForm(FlaskForm):
    code = StringField(
        'code',
        validators=[DataRequired(message='A valid code is required'), validateSecurityCode]
    )

    attempt = IntegerField('attempt', default=0)

    submit = SubmitField('Continue')
