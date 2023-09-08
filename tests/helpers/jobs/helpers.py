from datetime import datetime
from dateutil.relativedelta import relativedelta
from grc.models import db, Application, ApplicationStatus
from grc.business_logic.data_store import DataStore


def create_test_apps():
    test_inactive_apps = []
    for _ in range(3):
        app = DataStore.create_new_application('ivan.touloumbadjian@hmcts.net')
        db.session.commit()
        new_app = Application.query.filter_by(
            reference_number=app.reference_number,
            email=app.email_address
        ).first()
        new_app.status = ApplicationStatus.STARTED
        new_app.updated = datetime.now() - relativedelta(days=93)
        db.session.commit()
        print(f'Test Inactive App Ref - {new_app.reference_number}', flush=True)
        test_inactive_apps.append(new_app)

    test_completed_apps = []
    for _ in range(3):
        app = DataStore.create_new_application('ivan.touloumbadjian@hmcts.net')
        db.session.commit()
        new_app = Application.query.filter_by(
            reference_number=app.reference_number,
            email=app.email_address
        ).first()
        new_app.status = ApplicationStatus.COMPLETED
        new_app.completed = datetime.now() - relativedelta(days=7)
        db.session.commit()
        print(f'Test Completed App Ref - {new_app.reference_number}', flush=True)
        test_completed_apps.append(new_app)

    return test_inactive_apps, test_completed_apps


def delete_test_application(app):
    Application.query.filter_by(
        reference_number=app.reference_number,
        email='ivan.touloumbadjian@hmcts.net'
    ).delete()
    db.session.commit()
    print(f'application - {app.reference_number} deleted', flush=True)