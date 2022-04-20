from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from grc.utils.form_custom_validators import StrictRequiredIf, validateDOB


class NameForm(FlaskForm):
    first_name = StringField(
        validators=[DataRequired(message='Enter your first name, as originally registered on your birth or adoption certificate')]
    )

    last_name = StringField(
        validators=[DataRequired(message='Enter your last name, as originally registered on your birth or adoption certificate')]
    )


class DobForm(FlaskForm):
    day = IntegerField(
        validators=[
            DataRequired(message='Enter a day'),
            NumberRange(min=1, max=31, message='Enter a valid day'),
            validateDOB
        ]
    )

    month = IntegerField(
        validators=[
            DataRequired(message='Enter a month'),
            NumberRange(min=1, max=12, message='Enter a valid month'),
            validateDOB
        ]
    )

    # THe user must be 18 years old or older to apply
    year = IntegerField(
        validators=[
            DataRequired(message='Enter a year'),
            validateDOB
        ]
    )


class UkCheckForm(FlaskForm):
    birth_registered_in_uk = RadioField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        validators=[DataRequired(message='Select if your birth was registered in the UK')]
    )


class CountryForm(FlaskForm):
    country = StringField(
        'country',
        validators=[DataRequired(message='Country is required')]
    )

    submit = SubmitField('Save and continue')


class PlaceOfBirthForm(FlaskForm):
    place_of_birth = StringField(
        validators=[DataRequired(message='Enter your town or city of birth')]
    )


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

    #adopted_uk = StringField(
    #    'adopted_uk',
    #    # choices=[('Yes'), ('No'), (None)],
    #    validators=[StrictRequiredIf('check', 'Yes', message='Select if your were you adopted in the United Kingdom')]  # validateAdopted
    #)

    submit = SubmitField('Save and continue')


class AdoptedUKForm(FlaskForm):
    check = RadioField(
        'check',
        choices=[('Yes'), ('No')],
        validators=[DataRequired(message='Select if your were you adopted in the United Kingdom')]
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
