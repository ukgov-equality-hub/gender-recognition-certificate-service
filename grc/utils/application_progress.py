from grc.list_status import ListStatus


def calculate_progress_status_colour(value):
    if value == ListStatus.COMPLETED:
        return ''
    elif value == ListStatus.IN_PROGRESS:
        return 'govuk-tag--blue'
    else:
        return 'govuk-tag--grey'
