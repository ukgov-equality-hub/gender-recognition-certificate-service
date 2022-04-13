from datetime import datetime, timedelta
from dateutil import tz
from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app, session
from grc.save_and_return.forms import ReturnToYourApplicationForm
from notifications_python_client.notifications import NotificationsAPIClient
from grc.utils.security_code import send_security_code
from grc.utils.reference_number import validate_reference_number, reference_number_string
from grc.start_application.forms import ValidateEmailForm
from grc.utils.decorators import EmailRequired, LoginRequired, Unauthorized
from grc.utils.application_progress import save_progress
from grc.utils.threading import Threading

saveAndReturn = Blueprint('saveAndReturn', __name__)


@saveAndReturn.route('/save-and-return', methods=['GET'])
@Unauthorized
def index():
    return redirect(url_for('startApplication.index'))


@saveAndReturn.route('/save-and-return/exit-application', methods=['GET'])
@LoginRequired
def exitApplication():
    if current_app.config['NOTIFY_OVERRIDE_EMAIL']:
        send_to = current_app.config['NOTIFY_OVERRIDE_EMAIL']
    else:
        send_to = session['application']['email']

    local = datetime.now().replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/London'))
    notifications_client = NotificationsAPIClient(current_app.config['NOTIFY_API'])
    notifications_client.send_email_notification(
        email_address=send_to,
        template_id=current_app.config['NOTIFY_UNFINISHED_APPLICATION_EMAIL_TEMPLATE_ID'],
        personalisation={
            'expiry_days': datetime.strftime(local + timedelta(days=90), '%d/%m/%Y %H:%M:%S'),
            'grc_return_link': request.url_root + 'save-and-return'
        }
    )

    reference_number = reference_number_string(session['reference_number'])
    save_progress()
    session.clear()

    return render_template(
        'save-and-return/exit-application.html',
        reference_number=reference_number
    )
