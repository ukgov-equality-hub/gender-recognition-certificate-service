from datetime import datetime
from flask import session
from grc.models import db, Application, ListStatus


def save_progress():
    """ Update DB application JSON field and also session application
    """
    application_record = Application.query.filter_by(reference_number=session['reference_number'],email=session['email']).first()

    if application_record is not None:
        try:
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



def calculate_progress_status():
    """ Calculate list status
    """
    try:
        if 'application' in session:
            list_status = {
                        "confirmation": ListStatus.NOT_STARTED,
                        "personalDetails": ListStatus.NOT_STARTED,
                        "birthRegistration": ListStatus.NOT_STARTED,
                        "partnershipDetails": ListStatus.NOT_STARTED,
                        "medicalReports": ListStatus.NOT_STARTED,
                        "genderEvidence": ListStatus.NOT_STARTED,
                        "submitAndPay": ListStatus.CANNOT_START_YET
                        }

            # calculate confirmation
            list_status['confirmation'] = calculate_progress_status_display_name(ListStatus[session['application']['confirmation']['progress']])
            # if 'overseasCheck' in session['application']["confirmation"] and 'declaration' in session['application']["confirmation"] and  (session['application']["confirmation"]["overseasCheck"] == 'Yes' or "overseasApprovedCheck" in session['application']["confirmation"]) and session['application']["confirmation"]["declaration"] == True:
            #     list_status['confirmation'] = ListStatus.COMPLETED
            # elif 'overseasCheck' not in session['application']["confirmation"] and "declaration" not in session['application']["confirmation"]:
            #     list_status['confirmation'] = ListStatus.NOT_STARTED
            # else:
            #     list_status['confirmation'] = ListStatus.IN_PROGRESS

            # personal details
            list_status['personalDetails'] = calculate_progress_status_display_name(ListStatus[session['application']['personalDetails']['progress']])

            return list_status

    except ValueError:
        print("Oops!  Session does not exist")


def calculate_progress_status_display_name(value):
    """ Calculate list status
    """
    if value == ListStatus.IN_PROGRESS or value == ListStatus.IN_REVIEW:
       return ListStatus.IN_PROGRESS

    return value



def calculate_progress_status_colour(value):
    """ Calculate list status
    """
    if value == ListStatus.COMPLETED:
        return ''
    elif value == ListStatus.IN_PROGRESS:
        return 'govuk-tag--blue'
    else:
        return 'govuk-tag--grey'
