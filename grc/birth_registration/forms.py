from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from datetime import datetime
from dateutil.relativedelta import relativedelta
from grc.utils.form_custom_validators import StrictRequiredIf, validateAdopted, validateDOB


class NameForm(FlaskForm):
    first_name = StringField(
        'first_name',
        validators=[DataRequired(message='First name is required')]
    )

    last_name = StringField(
        'last_name',
        validators=[DataRequired(message='Last name is required')]
    )

    submit = SubmitField('Save and continue')


class SexForm(FlaskForm):
    check = RadioField(
        'check',
        choices=[('Female'), ('Male')],
        validators=[DataRequired(message='Select a sex')]
    )

    submit = SubmitField('Save and continue')


class DobForm(FlaskForm):
    day = IntegerField(
        'day',
        validators=[
            DataRequired(message='The date must include a day'),
            NumberRange(min=1, max=31, message='Please enter a valid day'),
            validateDOB
        ]
    )

    month = IntegerField(
        'month',
        validators=[
            DataRequired(message='The date must include a month'),
            NumberRange(min=1, max=12, message='Please enter a valid month'),
            validateDOB
        ]
    )

    # We are assuming the person applying is 18 years old or older
    year = IntegerField(
        'year',
        validators=[
            DataRequired(message='The date must include a year'),
            #NumberRange(
            #    min=int((datetime.now() - relativedelta(years=120)).strftime('%Y')),
            #    max=int((datetime.now() - relativedelta(years=18)).strftime('%Y')),
            #    message='Year needs to be a valid year in past. You need to be 18 years old to apply.'
            #),
            validateDOB
        ]
    )

    submit = SubmitField('Save and continue')


class UkCheckForm(FlaskForm):
    check = RadioField(
        'check',
        choices=[('Yes'), ('No')],
        validators=[DataRequired(message='Select if your birth was registered in the UK')]
    )

    submit = SubmitField('Save and continue')


class CountryForm(FlaskForm):
    country = StringField(
        'country',
        validators=[DataRequired(message='Country is required')]
    )

    submit = SubmitField('Save and continue')


class PlaceOfBirthForm(FlaskForm):
    place_of_birth = StringField(
        'place_of_birth',
        validators=[DataRequired(message='Place of birth is required')]
    )

    submit = SubmitField('Save and continue')


class MothersNameForm(FlaskForm):
    first_name = StringField(
        'first_name',
        validators=[DataRequired(message='First name is required')]
    )

    last_name = StringField(
        'last_name',
        validators=[DataRequired(message='Last name is required')]
    )

    maiden_name = StringField(
        'maiden_name',
        validators=[DataRequired(message='Mother’s maiden name is required')]
    )

    submit = SubmitField('Save and continue')


class FatherNameCheckForm(FlaskForm):
    check = RadioField(
        'check',
        choices=[('Yes'), ('No')],
        validators=[DataRequired(message='Select if your father’s name is listed on the certificate')]
    )

    submit = SubmitField('Save and continue')


class AdoptedForm(FlaskForm):
    check = RadioField(
        'check',
        choices=[('Yes'), ('No')],
        validators=[DataRequired(message='Select if your were you adopted')]
    )

    adopted_uk = StringField(
        'adopted_uk',
        # choices=[('Yes'), ('No'), (None)],
        validators=[StrictRequiredIf('check', 'Yes', message='Select if your were you adopted in the United Kingdom')]  # validateAdopted
    )

    submit = SubmitField('Save and continue')


class ForcesForm(FlaskForm):
    check = RadioField(
        'check',
        choices=[('Yes'), ('No'), ('I don’t know')],
        validators=[DataRequired(message='Select if your was birth registered by a Forces registering service, or with a British Consul or High Commission, or under Merchant Shipping or Civil Aviation provisions')]
    )

    submit = SubmitField('Save and continue')


class CheckYourAnswers(FlaskForm):
    submit = SubmitField('Save and continue')
