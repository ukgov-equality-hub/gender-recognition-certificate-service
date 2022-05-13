from grc import create_app
from grc.config import TestConfig
from grc.utils.form_custom_validators import validatePasswordStrength, validatePostcode, validateDOB, validateDateOfTransiton, validateNationalInsuranceNumber
from wtforms.validators import ValidationError


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


def test_email_page():
    data = {
        "email": "blah"
    }
    response = client.post('/', data=data)
    print(response.data, flush=True)
    assert response.status_code==200
    assert b"The CSRF token is missing" not in response.data
    assert b"A valid email address is required" in response.data

    data = {
        "email": "blah@blah.com"
    }
    response = client.post('/', data=data)
    print(response.data, flush=True)
    assert response.status_code==200
    assert b"A valid email address is required" not in response.data


def test_validatePasswordStrength():

    # Password fails
    try:
        validatePasswordStrength(None, FormItem('', 'password'))
        assert False
    except ValidationError:
        assert True

    try:
        validatePasswordStrength(None, FormItem('', 'Password'))
        assert False
    except ValidationError:
        assert True

    try:
        validatePasswordStrength(None, FormItem('', 'Password123'))
        assert False
    except ValidationError:
        assert True

    # Pass
    try:
        validatePasswordStrength(None, FormItem('', 'Password!123'))
        assert True
    except ValidationError:
        assert False


def test_validatePostcode():
    try:
        validatePostcode(None, FormItem('', 'AA'))
        assert False
    except ValidationError:
        assert True

    try:
        validatePostcode(None, FormItem('', 'AB12CD'))
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
        validateDOB(form, FormItem('year', 2001))
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
        validateDOB(form, FormItem('year', 2001))
        assert False
    except ValidationError:
        assert True

    form = {
        'day': FormItem('day', 22),
        'month': FormItem('month', 1),
        'year': FormItem('year', 2021)
    }

    try:
        validateDOB(form, FormItem('year', 2021))
        assert False
    except ValidationError:
        assert True

    form = {
        'day': FormItem('day', 22),
        'month': FormItem('month', 1),
        'year': FormItem('year', 2001)
    }

    try:
        validateDOB(form, FormItem('year', 2001))
        assert True
    except ValidationError:
        assert False


def test_validateDateOfTransiton():
    pass


def test_validateNationalInsuranceNumber():
    try:
        validateNationalInsuranceNumber(None, FormItem('', 'AA'))
        assert False
    except ValidationError:
        assert True

    try:
        validateNationalInsuranceNumber(None, FormItem('', 'AA123456A'))
        assert True
    except ValidationError:
        assert False
