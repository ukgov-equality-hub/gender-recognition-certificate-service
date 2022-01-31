from datetime import datetime
from flask import session
from grc.models import db, Application


def save_progress():
    """An 8 alphanumeric characters code generator as string to be used as
    an application reference number
    """
    application_record = Application.query.filter_by(reference_number=session['reference_number'],email=session['email']).first()

    if application_record is not None:

        try:
            # application_record.user_input = application_record.data()
            # application_record.updated = datetime.now()
            # db.session.commit()
            # return application_record.data()

            if 'application' in session:
                application_record.user_input = session['application']
                application_record.updated = datetime.now()
                db.session.commit()
                session['application'] = application_record.data()
                return application_record.data()
            else:
                application_record.user_input = application_record.data()
                application_record.updated = datetime.now()
                db.session.commit()
                session['application'] = application_record.data()
                return application_record.data()

        except ValueError:
            print("Oops!  Something went wrong.")
    else:
        print("Application does not exist")
