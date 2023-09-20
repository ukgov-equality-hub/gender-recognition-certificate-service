from grc import create_app
from grc.config import TestConfig
from grc.models import ApplicationStatus
from admin.jobs.notify_applicants_inactive_apps import application_notifications
from tests.helpers.jobs.helpers import create_test_apps, delete_test_application


def create_test_app():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app(TestConfig)
    flask_app.config['WTF_CSRF_ENABLED'] = False
    return flask_app


def test_notify_applicants_inactive_applications():
    flask_app = create_test_app()

    with flask_app.test_client() as test_client:
        _ = test_client.get('/')
        test_inactive_apps, test_completed_apps = create_test_apps()

        response = application_notifications()

        assert response == 200

        for app in test_completed_apps:
            assert app.status == ApplicationStatus.DELETED
            delete_test_application(app)

        for app in test_inactive_apps:
            delete_test_application(app)