from flask_wtf import FlaskForm
from wtforms import EmailField, RadioField
from wtforms.validators import DataRequired, Email
from grc.document_checker.doc_checker_state import CurrentlyInAPartnershipEnum


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
        validators=[DataRequired(message='Select if you have ever been married or in a civil partnership that has ended')]
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
    email_address = EmailField(
        validators=[
            DataRequired(message='Enter your email address'),
            Email(message='Enter a valid email address')
        ]
    )
