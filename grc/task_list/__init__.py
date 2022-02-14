import email
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, session
)
from werkzeug.exceptions import abort
from flask import render_template


from grc.utils.decorators import LoginRequired
from grc.utils.application_progress import calculate_progress_status, calculate_progress_status_colour

taskList = Blueprint('taskList', __name__)



@taskList.route('/task-list', methods=['GET', 'POST'])
@LoginRequired
def index():

    return render_template('task-list.html', application=session['application'], list_status=calculate_progress_status(), get_colour=calculate_progress_status_colour)
