import email
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, session
)
from werkzeug.exceptions import abort
from flask import render_template
from datetime import datetime, timedelta

from grc.save_and_return.forms import ReturnToYourApplicationForm, ValidateCodeForm
from notifications_python_client.notifications import NotificationsAPIClient
from grc.utils.security_code import send_security_code
from grc.utils.reference_number import validate_reference_number, reference_number_string
from grc.start_application.forms import ValidateEmailForm
from grc.utils.decorators import EmailRequired, LoginRequired, Unauthorized
from grc.utils.application_progress import save_progress

saveAndReturn = Blueprint('saveAndReturn', __name__)

@saveAndReturn.route('/save-and-return', methods=['GET', 'POST'])
@Unauthorized
def index():
    form = ReturnToYourApplicationForm()

    if form.validate_on_submit():
        session.clear()
        application = validate_reference_number(form.reference.data)
        session['reference_number']  = application.reference_number
        session['email'] = application.email
        response = send_security_code(application.email)


        return redirect(url_for('saveAndReturn.securityCode'))

    return render_template('save-and-return/return.html', form=form)

@saveAndReturn.route('/save-and-return/security-code', methods=['GET', 'POST'])
@EmailRequired
@Unauthorized
def securityCode():
    form = ValidateEmailForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            application = validate_reference_number(session['reference_number'])
            session['reference_number']  = application.reference_number
            session['application'] = application.data()
            return redirect(url_for('taskList.index'))
    elif request.args.get('resend') == 'true':
        try:
            send_security_code(session['email'])
            flash('We’ve resent you a security code. This can take a few minutes to arrive.', 'email')
        except BaseException as err:
            error = err.args[0].json()
            flash(error['errors'][0]['message'], 'error')



    return render_template('security-code.html', form=form, action=url_for('saveAndReturn.securityCode'), back=url_for('saveAndReturn.index'), email=session['email'])

@saveAndReturn.route('/save-and-return/exit-application', methods=['GET'])
@LoginRequired
def exitApplication():
    # Send email
    notifications_client = NotificationsAPIClient(current_app.config['NOTIFY_API'])
    response = notifications_client.send_email_notification(
        email_address=session["application"]['email'], # required string
        template_id=current_app.config['NOTIFY_UNFINISHED_APPLICATION_EMAIL_TEMPLATE_ID'], # required UUID string
        personalisation={
            'expiry_days': datetime.strftime(datetime.now() + timedelta(days=90), '%d/%m/%Y %H:%M:%S'),
            'grc_return_link': request.url_root + 'save-and-return'
        }
    )

    reference_number = reference_number_string(session['reference_number'])
    save_progress()
    session.clear()

    return render_template('save-and-return/exit-application.html', reference_number=reference_number)