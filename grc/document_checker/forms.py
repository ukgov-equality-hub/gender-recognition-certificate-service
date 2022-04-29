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


class PartnerAgreesForm(FlaskForm):
    check = RadioField(
        'check',
        choices=[('Yes'), ('No')],
        validators=[DataRequired(message='Select if you can provide a declaration of consent from your spouse')]
    )

    submit = SubmitField('Save and continue')


class PartnerDiedForm(FlaskForm):
    check = RadioField(
        'check',
        choices=[('Yes'), ('No')],
        validators=[DataRequired(message='Select if you were previously married or in a civil partnership, but your spouse or partner has died')]
    )

    submit = SubmitField('Save and continue')


class EndedCheckForm(FlaskForm):
    check = RadioField(
        'check',
        choices=[('Yes'), ('No')],
        validators=[DataRequired(message='Select if you have ever been married or in a civil partnership that has now ended')]
    )

    submit = SubmitField('Save and continue')


class InterimCheckForm(FlaskForm):
    submit = SubmitField('Save and continue')


class OverseasApprovedCheckForm(FlaskForm):
    check = RadioField(
        'check',
        choices=[('Yes'), ('No')],
        validators=[DataRequired(message='Select if you have official documentation')]
    )

    submit = SubmitField('Continue')


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
