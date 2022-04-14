from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, RadioField, TelField
from wtforms.validators import DataRequired
from grc.utils.form_custom_validators import StrictRequiredIf, validateNino, validatePostcode
from grc.utils.form_widgets import MultiCheckboxField


class NameForm(FlaskForm):
    first_name = StringField(
        validators=[DataRequired(message='Enter your first name(s)')]
    )

    last_name = StringField(
        validators=[DataRequired(message='Enter your last name')]
    )


class AffirmedGenderForm(FlaskForm):
    affirmedGender = RadioField(
        choices=[
            ('MALE', 'Male'),
            ('FEMALE', 'Female')
        ],
        validators=[DataRequired(message='Select your affirmed gender')]
    )


class PreviousNamesCheck(FlaskForm):
    previousNameCheck = RadioField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        validators=[DataRequired(message='Select if you have ever changed your name to reflect your gender')]
    )


class AddressForm(FlaskForm):
    address_line_one = StringField(
        validators=[DataRequired(message='Enter your building')]
    )

    address_line_two = StringField(
        validators=[DataRequired(message='Enter your street')]
    )

    town = StringField(
        validators=[DataRequired(message='Enter your town or city')]
    )

    postcode = StringField(
        validators=[DataRequired(message='Enter your postcode'), validatePostcode]
    )


class ContactPreferencesForm(FlaskForm):
    options = MultiCheckboxField(
        'options',
        choices=[('email'), ('phone'), ('post')],
        validators=[DataRequired(message='Please select how would you like to be contacted')]
    )

    email = EmailField(
        'email',
        validators=[StrictRequiredIf('options', 'email', message='Email address is required')]
    )  # Email(message='A valid email address is required')

    phone = TelField(
        'phone',
        validators=[StrictRequiredIf('options', 'phone', message='Phone number is required')]
    )

    submit = SubmitField('Save and continue')


class ContactNameForm(FlaskForm):
    check = RadioField(
        'check',
        choices=[('Yes'), ('No')],
        validators=[DataRequired(message='Select if you want us to use a different name')]
    )

    name = StringField(
        'name',
        validators=[StrictRequiredIf('check', 'Yes', message='Full name is required')]
    )

    submit = SubmitField('Save and continue')


class ContactDatesForm(FlaskForm):
    check = RadioField(
        'check',
        choices=[('Yes'), ('No')],
        validators=[DataRequired(message='Select if you’ll be unavailable')]
    )

    dates = StringField(
        'dates', validators=[StrictRequiredIf('check', 'Yes', message='Dates are required')]
    )

    submit = SubmitField('Save and continue')


class HmrcForm(FlaskForm):
    check = RadioField(
        'check',
        choices=[('Yes'),('No')],
        validators=[DataRequired(message='Select if you would like us to tell HMRC after you receive a Gender Recognition Certificate')]
    )

    nino = StringField(
        'nino',
        validators=[StrictRequiredIf('check', 'Yes', message='A valid National Insurance number is required'), validateNino]
    )

    submit = SubmitField('Save and continue')


class CheckYourAnswers(FlaskForm):
    submit = SubmitField('Save and continue')
