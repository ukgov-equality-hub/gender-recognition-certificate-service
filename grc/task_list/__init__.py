from flask import Blueprint, render_template, session
from grc.utils.decorators import LoginRequired
from grc.utils.application_progress import calculate_progress_status, calculate_progress_status_colour
from grc.list_status import ListStatus

taskList = Blueprint('taskList', __name__)


@taskList.route('/task-list', methods=['GET'])
@LoginRequired
def index():
    list_status = calculate_progress_status()

    return render_template(
        'task-list.html',
        application=session['application'],
        list_status=list_status,
        get_colour=calculate_progress_status_colour,
        ListStatus=ListStatus
    )
