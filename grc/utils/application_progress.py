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
