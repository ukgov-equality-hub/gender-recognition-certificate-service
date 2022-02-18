from datetime import datetime
from typing import List
from flask import session
from grc.models import db, Application, ListStatus, ApplicationStatus


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

            # confirmation
            list_status['confirmation'] = calculate_progress_status_display_name(ListStatus[session['application']['confirmation']['progress']])

            # personal details
            list_status['personalDetails'] = calculate_progress_status_display_name(ListStatus[session['application']['personalDetails']['progress']])

            # Birth registration
            list_status['birthRegistration'] = calculate_progress_status_display_name(ListStatus[session['application']['birthRegistration']['progress']])

            # Partnership details
            list_status['partnershipDetails'] = calculate_progress_status_display_name(ListStatus[session['application']['partnershipDetails']['progress']])

            # Medical reports
            list_status['medicalReports'] = calculate_progress_status_display_name(ListStatus[session['application']['medicalReports']['progress']])

            # Gender evidence
            list_status['genderEvidence'] = calculate_progress_status_display_name(ListStatus[session['application']['genderEvidence']['progress']])

            # Submit and pay
            if session['application']['submitAndPay']['progress']==ListStatus.CANNOT_START_YET.name and list_status['confirmation'] == ListStatus.COMPLETED and list_status['personalDetails'] == ListStatus.COMPLETED and list_status['birthRegistration'] == ListStatus.COMPLETED and list_status['partnershipDetails'] == ListStatus.COMPLETED and list_status['medicalReports'] == ListStatus.COMPLETED and list_status['genderEvidence'] == ListStatus.COMPLETED:
                session['application']['submitAndPay']['progress'] = ListStatus.NOT_STARTED.name
                save_progress()
                list_status['submitAndPay'] = calculate_progress_status_display_name(ListStatus[session['application']['submitAndPay']['progress']])
            elif session['application']['submitAndPay']['progress']!=ListStatus.CANNOT_START_YET.name and not (list_status['confirmation'] == ListStatus.COMPLETED and list_status['personalDetails'] == ListStatus.COMPLETED and list_status['birthRegistration'] == ListStatus.COMPLETED and list_status['partnershipDetails'] == ListStatus.COMPLETED and list_status['medicalReports'] == ListStatus.COMPLETED and list_status['genderEvidence'] == ListStatus.COMPLETED):
                session['application']['submitAndPay']['progress'] = ListStatus.CANNOT_START_YET.name
                save_progress()

            list_status['submitAndPay'] = calculate_progress_status_display_name(ListStatus[session['application']['submitAndPay']['progress']])

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


def mark_complete():
    """ Update DB application JSON field and also session application
    """
    application_record = Application.query.filter_by(reference_number=session['reference_number'],email=session['email']).first()

    if application_record is not None:
        try:
            if 'application' in session:
                application_record.user_input = session['application']
                application_record.updated = datetime.now()
                application_record.status = ApplicationStatus.COMPLETED
                db.session.commit()
                session['application'] = application_record.data()
        except ValueError:
            print("Oops!  Something went wrong.")
    else:
        print("Application does not exist")
