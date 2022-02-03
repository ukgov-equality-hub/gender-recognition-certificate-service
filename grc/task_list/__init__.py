import email
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, session
)
from werkzeug.exceptions import abort
from flask import render_template

from grc.save_and_return.forms import ReturnToYourApplicationForm, ValidateCodeForm

from grc.utils.security_code import send_security_code
from grc.utils.decorators import LoginRequired

taskList = Blueprint('taskList', __name__)

@taskList.route('/task-list', methods=['GET', 'POST'])
@LoginRequired
def index():

    # form = ReturnToYourApplicationForm()
    # notifications_client = NotificationsAPIClient(current_app.config['NOTIFY_API'])

    # if form.validate_on_submit():
    #     session.clear()
    #     application = ValidateReferenceNumber(form.reference.data)
    #     session['reference_number']  = application.reference_number
    #     session['email'] = application.email
    #     response = send_security_code(application.email)


    #     return redirect(url_for('taskList.securityCode'))

    return render_template('task-list.html', application=session['application'])

# @taskList.route('/save-and-return/security-code', methods=['GET', 'POST'])
# @LoginRequired
# def securityCode():
#     form = ValidateEmailForm()

#     if request.method == 'POST':
#         if form.validate_on_submit():
#             application = ValidateReferenceNumber(session['reference_number'])
#             session['reference_number']  = application.reference_number
#             session['application'] = application.data()
#             return redirect(url_for('startApplication.declaration'))
#     elif request.args.get('resend') == 'true':
#         response = send_security_code(session['email'])
#         flash('We’ve resent you a security code. This can take a few minutes to arrive.', 'email')



#     return render_template('security-code.html', form=form, action=url_for('taskList.securityCode'), back=url_for('taskList.index'), email=session['email'])