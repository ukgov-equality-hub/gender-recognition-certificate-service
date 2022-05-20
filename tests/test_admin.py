from admin import create_app
from grc.config import TestConfig

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


def test_loggedout():
    response = client.get('/applications', subdomain='test')
    assert response.status_code == 302


def test_loggedin():
    with client.session_transaction(subdomain='test') as session:
        session['signedIn'] = 'test@example.com'
        session['userType'] = 'VIEWER'

    response = client.get('/applications', subdomain='test')
    assert response.status_code == 200

    response = client.get('/users', subdomain='test')
    assert response.status_code == 302


def test_adminloggedin():
    with client.session_transaction(subdomain='test') as session:
        session['signedIn'] = 'test@example.com'
        session['userType'] = 'ADMIN'

    response = client.get('/users', subdomain='test')
    assert response.status_code == 200
