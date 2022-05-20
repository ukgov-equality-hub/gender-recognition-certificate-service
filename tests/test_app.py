import re
from grc import create_app
from grc.config import TestConfig
from grc.utils import form_custom_validators
from grc.utils import reference_number
from grc.utils import security_code
from wtforms.validators import ValidationError

# FLASK_ENV='production' pytest tests/test_app.py

flask_app = create_app(TestConfig)
flask_app.config['TESTING'] = True
flask_app.config['WTF_CSRF_METHODS'] = []
flask_app.config['WTF_CSRF_ENABLED'] = False
client = flask_app.test_client()


class FormItem():
    def __init__(self, name, data):
        self.name = name
        self.data = data


def test_home_page():
    response = client.get('/')
    assert response.status_code == 200
    assert b"Apply for a Gender Recognition Certificate" in response.data


def test_email_page1():
    data = {
        "email": "test"
    }
    response = client.post('/', data=data)
    assert response.status_code==200
    assert b"The CSRF token is missing" not in response.data
    assert b"Enter a valid email address" in response.data


def test_email_page2():
    data = {
        "email": "test@example.com"
    }
    response = client.post('/', data=data)
    assert response.status_code==200
    assert b"Enter a valid email address" not in response.data


def test_validatePasswordStrength():

    # Password fails
    try:
        form_custom_validators.validatePasswordStrength(None, FormItem('', 'password'))
        assert False
    except ValidationError:
        assert True

    try:
        form_custom_validators.validatePasswordStrength(None, FormItem('', 'Password'))
        assert False
    except ValidationError:
        assert True

    try:
        form_custom_validators.validatePasswordStrength(None, FormItem('', 'Password123'))
        assert False
    except ValidationError:
        assert True

    # Pass
    try:
        form_custom_validators.validatePasswordStrength(None, FormItem('', 'Password!123'))
        assert True
    except ValidationError:
        assert False


def test_validatePostcode():
    try:
        form_custom_validators.validatePostcode(None, FormItem('', 'AA'))
        assert False
    except ValidationError:
        assert True

    try:
        form_custom_validators.validatePostcode(None, FormItem('', 'AB12CD'))
        assert True
    except ValidationError:
        assert False


def test_validateDOB():
    form = {
        'day': FormItem('day', 'a'),
        'month': FormItem('month', 1),
        'year': FormItem('year', 2001)
    }

    try:
        form_custom_validators.validateDOB(form, FormItem('year', 2001))
        assert False
    except TypeError:
        assert True
    except ValidationError:
        assert True

    form = {
        'day': FormItem('day', 22),
        'month': FormItem('month', 15),
        'year': FormItem('year', 2001)
    }

    try:
        form_custom_validators.validateDOB(form, FormItem('year', 2001))
        assert False
    except ValidationError:
        assert True

    form = {
        'day': FormItem('day', 22),
        'month': FormItem('month', 1),
        'year': FormItem('year', 2021)
    }

    try:
        form_custom_validators.validateDOB(form, FormItem('year', 2021))
        assert False
    except ValidationError:
        assert True

    form = {
        'day': FormItem('day', 22),
        'month': FormItem('month', 1),
        'year': FormItem('year', 2001)
    }

    try:
        form_custom_validators.validateDOB(form, FormItem('year', 2001))
        assert True
    except ValidationError:
        assert False


def test_validateDateOfTransiton():
    form = {
        'transition_date_month': FormItem('transition_date_month', 'a'),
        'transition_date_year': FormItem('transition_date_year', 2001)
    }

    try:
        form_custom_validators.validateDateOfTransiton(form, FormItem('year', 2001))
        assert False
    except TypeError:
        assert True
    except ValidationError:
        assert True

    form = {
        'transition_date_month': FormItem('transition_date_month', 20),
        'transition_date_year': FormItem('transition_date_year', 2001)
    }

    try:
        form_custom_validators.validateDateOfTransiton(form, FormItem('year', 2001))
        assert False
    except ValidationError:
        assert True

    form = {
        'transition_date_month': FormItem('transition_date_month', 1),
        'transition_date_year': FormItem('transition_date_year', 2030)
    }

    try:
        form_custom_validators.validateDateOfTransiton(form, FormItem('year', 2030))
        assert False
    except ValidationError:
        assert True

    form = {
        'transition_date_month': FormItem('transition_date_month', 1),
        'transition_date_year': FormItem('transition_date_year', 2001)
    }

    try:
        form_custom_validators.validateDateOfTransiton(form, FormItem('year', 2001))
        assert True
    except ValidationError:
        assert False


def test_validateNationalInsuranceNumber():
    try:
        form_custom_validators.validateNationalInsuranceNumber(None, FormItem('', 'AA'))
        assert False
    except ValidationError:
        assert True

    try:
        form_custom_validators.validateNationalInsuranceNumber(None, FormItem('', 'AA123456A'))
        assert True
    except ValidationError:
        assert False


def test_reference_number_generator():
    code = reference_number.generate_reference_number(8)
    match = re.search('^[0-9A-Z]{8}$', code)
    assert match is not None

    code = reference_number.reference_number_string(code)
    match = re.search('^[0-9A-Z]{4}-[0-9A-Z]{4}$', code)
    assert match is not None


def test_security_code_generator():
    code = security_code.generate_security_code(5)
    match = re.search('^[0-9]{5}$', code)
    assert match is not None


def test_404_page():
    response = client.get('/this_page_does_not_exist')
    assert response.status_code == 404
