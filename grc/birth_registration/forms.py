from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired
from grc.utils.form_custom_validators import validateDOB, Integer


class NameForm(FlaskForm):
    first_name = StringField(
        validators=[DataRequired(message='Enter your first name, as originally registered on your birth or adoption certificate')]
    )

    middle_names = StringField() # Middle names are optional, so no validators are required here

    last_name = StringField(
        validators=[DataRequired(message='Enter your last name, as originally registered on your birth or adoption certificate')]
    )


class DobForm(FlaskForm):
    day = StringField(
        validators=[
            DataRequired(message='Enter a day'),
            Integer(min=1, max=31, message='Enter a day as a number between 1 and 31')
        ]
    )

    month = StringField(
        validators=[
            DataRequired(message='Enter a month'),
            Integer(min=1, max=12, message='Enter a month as a number between 1 and 12')
        ]
    )

    # The user must be 18 years old or older to apply
    year = StringField(
        validators=[
            DataRequired(message='Enter a year'),
            Integer(min=1000, message='Enter a year as a 4-digit number, like 2000', validators=[validateDOB])
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
    country_of_birth = StringField(
        validators=[DataRequired(message='Enter your country of birth')]
    )


class PlaceOfBirthForm(FlaskForm):
    place_of_birth = StringField(
        validators=[DataRequired(message='Enter your town or city of birth')]
    )


class MothersNameForm(FlaskForm):
    first_name = StringField(
        validators=[DataRequired(message="Enter your mother's first name")]
    )

    last_name = StringField(
        validators=[DataRequired(message="Enter your mother's last name")]
    )

    maiden_name = StringField(
        validators=[DataRequired(message="Enter your mother's maiden name")]
    )


class FatherNameCheckForm(FlaskForm):
    fathers_name_on_certificate = RadioField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        validators=[DataRequired(message="Select if your father's name is listed on the certificate")]
    )


class FathersNameForm(FlaskForm):
    first_name = StringField(
        validators=[DataRequired(message="Enter your father's first name")]
    )

    last_name = StringField(
        validators=[DataRequired(message="Enter your father's last name")]
    )


class AdoptedForm(FlaskForm):
    adopted = RadioField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        validators=[DataRequired(message='Select if you were you adopted')]
    )


class AdoptedUKForm(FlaskForm):
    adopted_uk = RadioField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
            ('DO_NOT_KNOW', "I don't know")
        ],
        validators=[DataRequired(message='Select if you were adopted in the United Kingdom')]
    )


class ForcesForm(FlaskForm):
    forces = RadioField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        validators=[DataRequired(message='Select if your birth was registered by a Forces registering service, or with a British Consul or High Commission, or under Merchant Shipping or Civil Aviation provisions')]
    )


class CheckYourAnswers(FlaskForm):
    # There are no fields on the CheckYourAnswers form
    # But, to avoid a compiler error, we need to write 'pass' here
    pass
