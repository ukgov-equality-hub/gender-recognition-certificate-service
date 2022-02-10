from flask import session
from wtforms.validators import DataRequired, ValidationError
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
    if validate_security_code(session['email'],field.data) is False:
        raise ValidationError('A valid code is required')

def validateReferenceNumber(form, field):
    if validate_reference_number(field.data) is False:
        raise ValidationError('A valid code is required')