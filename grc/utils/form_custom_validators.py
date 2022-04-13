import re
from flask import session
from wtforms.validators import DataRequired, InputRequired, ValidationError, StopValidation, Optional
from werkzeug.datastructures import FileStorage
from collections.abc import Iterable
from datetime import datetime, date
from grc.utils.security_code import validate_security_code
from grc.utils.reference_number import validate_reference_number


class RequiredIf(DataRequired):
    """Validator which makes a field required if another field is set and has a truthy value.

    Sources:
        - http://wtforms.simplecodes.com/docs/1.0.1/validators.html
        - http://stackoverflow.com/questions/8463209/how-to-make-a-field-conditionally-optional-in-wtforms

    """
    field_flags = ('requiredif',)

    def __init__(self, other_field_name, message=None, *args, **kwargs):
        self.other_field_name = other_field_name
        self.message = message

    def __call__(self, form, field):
        other_field = form[self.other_field_name]
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)


class StrictRequiredIf(DataRequired):
    """Validator which makes a field required if another field is set and has a specific value.

    Sources:
        - http://wtforms.simplecodes.com/docs/1.0.1/validators.html
        - http://stackoverflow.com/questions/8463209/how-to-make-a-field-conditionally-optional-in-wtforms

    """
    field_flags = ('requiredif',)

    def __init__(self, other_field_name, other_field_value, message=None, *args, **kwargs):
        self.other_field_name = other_field_name
        self.other_field_value = other_field_value
        self.message = message

    def __call__(self, form, field):
        other_field = form[self.other_field_name]
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if other_field.data == self.other_field_value:
            super(StrictRequiredIf, self).__call__(form, field)
        elif isinstance(other_field.data, list) and self.other_field_value in other_field.data:
            super(StrictRequiredIf, self).__call__(form, field)


def validateSecurityCode(form, field):
    if validate_security_code(session['email'], field.data) is False:
        raise ValidationError('A valid code is required')


def validateReferenceNumber(form, field):
    if validate_reference_number(field.data) is False:
        raise ValidationError('Enter a valid reference number')


def validateEmailAddress(form, field):
    from email.utils import parseaddr
    if not '@' in parseaddr(field.data)[1]:
        raise ValidationError('Enter a valid email address')


def validatePasswordStrength(form, field):
    def password_check(password):
        length_error = len(password) < 8
        digit_error = re.search(r'\d', password) is None
        uppercase_error = re.search(r'[A-Z]', password) is None
        lowercase_error = re.search(r'[a-z]', password) is None
        symbol_error = re.search(r'\W', password) is None
        return not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

    if password_check(field.data) is False:
        raise ValidationError('Your password needs to contain 8 characters or more and include upper, lower case and special characters')


def validateAdopted(form, field):

    # Custom validator for the "Are you adopted", StrictRequiredIf doesn't play nice with this question
    if form['check'].data == 'Yes':
        if field.data is None or field.data == '':
            raise ValidationError('Select if your were you adopted in the United Kingdom')


def validatePostcode(form, field):

    # https://stackoverflow.com/questions/164979/regex-for-matching-uk-postcodes
    if not (field.data is None or field.data == ''):
        data = field.data
        match = re.search('^([A-Za-z][A-Ha-hJ-Yj-y]?[0-9][A-Za-z0-9]? ?[0-9][A-Za-z]{2}|[Gg][Ii][Rr] ?0[Aa]{2})$', data)
        if match is None:
            raise ValidationError('Your post code is not valid')


def validateDOB(form, field):
    d = form['day'].data or 0
    m = form['month'].data or 0
    y = form['year'].data or 0
    if d > 0 and m > 0 and y > 0:
        try:
            dt = datetime(y, m, d, 00, 00)
        except Exception as e:
            if field.name == 'year':
                raise ValidationError('You have entered a invalid date')
            return

        def age(dt):
            today = date.today()
            return today.year - dt.year - ((today.month, today.day) < (dt.month, dt.day))

        if age(dt) < 18 and field.name == 'year':
            raise ValidationError('You need to be 18 years old to apply')


def validateNino(form, field):

    # https://www.gov.uk/hmrc-internal-manuals/national-insurance-manual/nim39110
    # https://stackoverflow.com/questions/17928496/use-regex-to-validate-a-uk-national-insurance-no-nino-in-an-html5-pattern-attri
    if not (field.data is None or field.data == ''):
        data = field.data.replace(' ', '').upper()
        match = re.search('^(?!BG)(?!GB)(?!NK)(?!KN)(?!TN)(?!NT)(?!ZZ)(?:[A-CEGHJ-PR-TW-Z][A-CEGHJ-NPR-TW-Z])(?:\s*\d\s*){6}[A-D]{1}$', data)
        if match is None:
            raise ValidationError('Your national insurance number is not valid')


class MultiFileAllowed(object):
    def __init__(self, upload_set, message=None):
        self.upload_set = upload_set
        self.message = message

    def __call__(self, form, field):
        if not (all(isinstance(item, FileStorage) for item in field.data) and field.data):
            return

        for data in field.data:
            filename = data.filename.lower()

            if isinstance(self.upload_set, Iterable):
                if any(filename.endswith('.' + x) for x in self.upload_set):
                    return

                raise StopValidation(self.message or field.gettext(
                    'File does not have an approved extension: {extensions}'
                ).format(extensions=', '.join(self.upload_set)))

            if not self.upload_set.file_allowed(field.data, filename):
                raise StopValidation(self.message or field.gettext(
                    'File does not have an approved extension.'
                ))


def FileSizeLimit(max_size_in_mb):
    max_bytes = max_size_in_mb*1024*1024

    def file_length_check(form, field):
        for data in field.data:
            if len(data.read()) > max_bytes:
                raise ValidationError(f'File size must be less than {max_size_in_mb}MB')

    return file_length_check
