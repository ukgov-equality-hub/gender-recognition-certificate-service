from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms.validators import DataRequired


class MarriageCivilPartnershipForm(FlaskForm):
    currently_married = RadioField(
        choices=[
            ('Married', 'Married'),
            ('Civil partnership', 'Civil partnership'),
            ('Neither', 'Neither')
        ],
        validators=[DataRequired(message='Select if you are currently married or in a civil partnership')]
    )


class StayTogetherForm(FlaskForm):
    stay_together = RadioField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        validators=[DataRequired(message='Select if you plan to remain married after receiving your Gender Recognition Certificate')]
    )


class PartnerAgreesForm(FlaskForm):
    partner_agrees = RadioField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        validators=[DataRequired(message='Select if you can provide a declaration of consent from your spouse')]
    )


class PartnerDiedForm(FlaskForm):
    partner_died = RadioField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        validators=[DataRequired(message='Select if you were previously married or in a civil partnership, and your spouse or partner died')]
    )


class PreviousPartnershipEndedForm(FlaskForm):
    previous_partnership_ended = RadioField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        validators=[DataRequired(message='Select if you have ever been married or in a civil partnership that has ended')]
    )


class InterimCheckForm(FlaskForm):
    # There are no fields on the CheckYourAnswers form
    # But, to avoid a compiler error, we need to write 'pass' here
    pass


class CheckYourAnswers(FlaskForm):
    # There are no fields on the CheckYourAnswers form
    # But, to avoid a compiler error, we need to write 'pass' here
    pass
