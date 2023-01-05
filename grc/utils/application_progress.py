from grc.utils.application_files import ApplicationFiles
from grc.models import db, ApplicationStatus
from grc.list_status import ListStatus


def calculate_progress_status_colour(value):
    if value == ListStatus.COMPLETED:
        return ''
    elif value == ListStatus.IN_PROGRESS:
        return 'govuk-tag--blue'
    elif value == ListStatus.ERROR:
        return 'govuk-tag--red'
    else:
        return 'govuk-tag--grey'


def anonymise_application(application_to_anonymise, new_status: ApplicationStatus):
    ApplicationFiles().delete_application_files(
        application_to_anonymise.reference_number,
        application_to_anonymise.application_data(),
    )
    application_to_anonymise.email = ''
    application_to_anonymise.user_input = ''
    application_to_anonymise.status = new_status

    db.session.commit()
