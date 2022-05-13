from datetime import datetime
from flask import session
from grc.models import db, Application, ListStatus, ApplicationStatus


def save_progress():
    application_record = Application.query.filter_by(
        reference_number=session['reference_number'],
        email=session['email']
    ).first()

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
            print('Oops!  Something went wrong.', flush=True)
    else:
        print('Application does not exist', flush=True)


def calculate_progress_status():
    try:
        if 'application' in session:
            list_status = {
                'confirmation': ListStatus.NOT_STARTED,
                'personalDetails': ListStatus.NOT_STARTED,
                'birthRegistration': ListStatus.NOT_STARTED,
                'partnershipDetails': ListStatus.NOT_STARTED,
                'medicalReports': ListStatus.NOT_STARTED,
                'genderEvidence': ListStatus.NOT_STARTED,
                'nameChange': ListStatus.CANNOT_START_YET,
                'marriageDocuments': ListStatus.CANNOT_START_YET,
                'overseasCertificate': ListStatus.CANNOT_START_YET,
                'statutoryDeclarations': ListStatus.NOT_STARTED,
                'submitAndPay': ListStatus.CANNOT_START_YET,
            }

            # Confirmation
            list_status['confirmation'] = calculate_progress_status_display_name(
                ListStatus[session['application']['confirmation']['progress']]
            )

            # Personal details
            list_status['personalDetails'] = calculate_progress_status_display_name(
                ListStatus[session['application']['personalDetails']['progress']]
            )

            # Birth registration
            list_status['birthRegistration'] = calculate_progress_status_display_name(
                ListStatus[session['application']['birthRegistration']['progress']]
            )

            # Partnership details
            list_status['partnershipDetails'] = calculate_progress_status_display_name(
                ListStatus[session['application']['partnershipDetails']['progress']]
            )

            # Medical reports
            if session['application']['medicalReports']['progress'] == ListStatus.CANNOT_START_YET.name and session['application']['confirmation']['overseasCheck'] == 'No':
                session['application']['medicalReports']['progress'] = ListStatus.NOT_STARTED.name
                session['application'] = save_progress()
            elif session['application']['medicalReports']['progress'] != ListStatus.CANNOT_START_YET.name and session['application']['confirmation']['overseasCheck'] == 'Yes':
                session['application']['medicalReports']['progress'] = ListStatus.CANNOT_START_YET.name
                session['application'] = save_progress()

            list_status['medicalReports'] = calculate_progress_status_display_name(
                ListStatus[session['application']['medicalReports']['progress']]
            )

            # Gender evidence
            if session['application']['genderEvidence']['progress'] == ListStatus.CANNOT_START_YET.name and session['application']['confirmation']['overseasCheck'] == 'No':
                session['application']['genderEvidence']['progress'] = ListStatus.NOT_STARTED.name
                session['application'] = save_progress()
            elif session['application']['genderEvidence']['progress'] != ListStatus.CANNOT_START_YET.name and session['application']['confirmation']['overseasCheck'] == 'Yes':
                session['application']['genderEvidence']['progress'] = ListStatus.CANNOT_START_YET.name
                session['application'] = save_progress()

            list_status['genderEvidence'] = calculate_progress_status_display_name(
                ListStatus[session['application']['genderEvidence']['progress']]
            )

            # Name change
            if (
                session['application']['nameChange']['progress'] == ListStatus.CANNOT_START_YET.name
                and 'previousNamesCheck' in session['application']['personalDetails']
                and session['application']['personalDetails']['previousNamesCheck'] == 'Yes'
            ):
                session['application']['nameChange']['progress'] = ListStatus.NOT_STARTED.name
                session['application'] = save_progress()
            elif (
                session['application']['nameChange']['progress'] != ListStatus.CANNOT_START_YET.name
                and 'previousNamesCheck' in session['application']['personalDetails']
                and session['application']['personalDetails']['previousNamesCheck'] != 'Yes'
            ):
                session['application']['nameChange']['progress'] = ListStatus.CANNOT_START_YET.name
                session['application'] = save_progress()

            list_status['nameChange'] = calculate_progress_status_display_name(
                ListStatus[session['application']['nameChange']['progress']]
            )

            # Marriage Documents
            if (
                session['application']['marriageDocuments']['progress'] == ListStatus.CANNOT_START_YET.name
                and 'marriageCivilPartnership' in session['application']['partnershipDetails']
                and (
                    session['application']['partnershipDetails']['marriageCivilPartnership'] == 'Married'
                    or (
                        session['application']['partnershipDetails']['marriageCivilPartnership'] == 'Neither'
                        and (
                            session['application']['partnershipDetails']['partnerDied'] == 'Yes'
                            or session['application']['partnershipDetails']['endedCheck'] == 'Yes'
                        )
                    )
                )
            ):
                session['application']['marriageDocuments']['progress'] = ListStatus.NOT_STARTED.name
                session['application'] = save_progress()
            elif (
                session['application']['marriageDocuments']['progress'] != ListStatus.CANNOT_START_YET.name
                and 'marriageCivilPartnership' in session['application']['partnershipDetails']
                and (
                    session['application']['partnershipDetails']['marriageCivilPartnership'] == 'Neither'
                    and session['application']['partnershipDetails']['partnerDied'] == 'No'
                    and session['application']['partnershipDetails']['endedCheck'] == 'No'
                )
            ):
                session['application']['marriageDocuments']['progress'] = ListStatus.CANNOT_START_YET.name
                session['application'] = save_progress()

            list_status['marriageDocuments'] = calculate_progress_status_display_name(
                ListStatus[session['application']['marriageDocuments']['progress']]
            )

            # Overseas certificate
            if session['application']['overseasCertificate']['progress'] == ListStatus.CANNOT_START_YET.name and session['application']['confirmation']['overseasApprovedCheck'] == 'Yes':
                session['application']['overseasCertificate']['progress'] = ListStatus.NOT_STARTED.name
                session['application'] = save_progress()

            list_status['overseasCertificate'] = calculate_progress_status_display_name(
                ListStatus[session['application']['overseasCertificate']['progress']]
            )

            # Statutory declarations
            list_status['statutoryDeclarations'] = calculate_progress_status_display_name(
                ListStatus[session['application']['statutoryDeclarations']['progress']]
            )

            # Submit and pay
            if session['application']['submitAndPay']['progress'] == ListStatus.IN_PROGRESS.name:
                list_status['submitAndPay'] = calculate_progress_status_display_name(
                    ListStatus[session['application']['submitAndPay']['progress']]
                )
            elif (
                (
                    session['application']['submitAndPay']['progress'] == ListStatus.CANNOT_START_YET.name
                    or session['application']['submitAndPay']['progress'] == ListStatus.NOT_STARTED.name
                    #or session['application']['submitAndPay']['progress'] == ListStatus.IN_PROGRESS.name
                )
                and list_status['confirmation'] == ListStatus.COMPLETED
                and list_status['personalDetails'] == ListStatus.COMPLETED
                and list_status['birthRegistration'] == ListStatus.COMPLETED
                and list_status['partnershipDetails'] == ListStatus.COMPLETED
                and list_status['statutoryDeclarations'] == ListStatus.COMPLETED
                and (
                    session['application']['medicalReports']['progress'] == ListStatus.CANNOT_START_YET.name
                    or session['application']['medicalReports']['progress'] == ListStatus.COMPLETED.name
                )
                and (
                    session['application']['genderEvidence']['progress'] == ListStatus.CANNOT_START_YET.name
                    or session['application']['genderEvidence']['progress'] == ListStatus.COMPLETED.name
                )
                and (
                    session['application']['nameChange']['progress'] == ListStatus.CANNOT_START_YET.name
                    or session['application']['nameChange']['progress'] == ListStatus.COMPLETED.name
                )
                and (
                    session['application']['marriageDocuments']['progress'] == ListStatus.CANNOT_START_YET.name
                    or session['application']['marriageDocuments']['progress'] == ListStatus.COMPLETED.name
                )
                and (
                    session['application']['overseasCertificate']['progress'] == ListStatus.CANNOT_START_YET.name
                    or session['application']['overseasCertificate']['progress'] == ListStatus.COMPLETED.name
                )
            ):
                session['application']['submitAndPay']['progress'] = ListStatus.NOT_STARTED.name
                session['application'] = save_progress()
                list_status['submitAndPay'] = calculate_progress_status_display_name(
                    ListStatus[session['application']['submitAndPay']['progress']]
                )
            elif session['application']['submitAndPay']['progress'] != ListStatus.CANNOT_START_YET.name and not (
                list_status['confirmation'] == ListStatus.COMPLETED
                and list_status['personalDetails'] == ListStatus.COMPLETED
                and list_status['birthRegistration'] == ListStatus.COMPLETED
                and list_status['partnershipDetails'] == ListStatus.COMPLETED
                and list_status['statutoryDeclarations'] == ListStatus.COMPLETED
                and (
                    session['application']['medicalReports']['progress'] == ListStatus.CANNOT_START_YET.name
                    or session['application']['medicalReports']['progress'] == ListStatus.COMPLETED.name
                )
                and (
                    session['application']['genderEvidence']['progress'] == ListStatus.CANNOT_START_YET.name
                    or session['application']['genderEvidence']['progress'] == ListStatus.COMPLETED.name
                )
                and (
                    session['application']['nameChange']['progress'] == ListStatus.CANNOT_START_YET.name
                    or session['application']['nameChange']['progress'] == ListStatus.COMPLETED.name
                )
                and (
                    session['application']['marriageDocuments']['progress'] == ListStatus.CANNOT_START_YET.name
                    or session['application']['marriageDocuments']['progress'] == ListStatus.COMPLETED.name
                )
            ):
                session['application']['submitAndPay']['progress'] = ListStatus.CANNOT_START_YET.name
                session['application'] = save_progress()

            list_status['submitAndPay'] = calculate_progress_status_display_name(
                ListStatus[session['application']['submitAndPay']['progress']]
            )

            return list_status

    except ValueError:
        print('Oops!  Session does not exist', flush=True)

    except Exception as e:
        print(e, flush=True)


def calculate_progress_status_display_name(value):
    if value == ListStatus.IN_PROGRESS or value == ListStatus.IN_REVIEW:
        return ListStatus.IN_PROGRESS

    return value


def calculate_progress_status_colour(value):
    if value == ListStatus.COMPLETED:
        return ''
    elif value == ListStatus.IN_PROGRESS:
        return 'govuk-tag--blue'
    else:
        return 'govuk-tag--grey'


def mark_complete():
    application_record = Application.query.filter_by(
        reference_number=session['reference_number'],
        email=session['email']
    ).first()

    if application_record is not None:
        try:
            if 'application' in session:
                application_record.user_input = session['application']
                application_record.updated = datetime.now()
                application_record.status = ApplicationStatus.SUBMITTED
                db.session.commit()
                session['application'] = application_record.data()
        except ValueError:
            print('Oops!  Something went wrong.', flush=True)
    else:
        print('Application does not exist', flush=True)
