from datetime import datetime, timedelta
from dateutil import tz
from flask import Blueprint, redirect, render_template, request, url_for, session
from grc.external_services.gov_uk_notify import GovUkNotify
from grc.utils.reference_number import reference_number_string
from grc.utils.decorators import LoginRequired, Unauthorized
from grc.utils.application_progress import save_progress

saveAndReturn = Blueprint('saveAndReturn', __name__)


@saveAndReturn.route('/save-and-return/exit-application', methods=['GET'])
@LoginRequired
def exitApplication():
    local = datetime.now().replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/London'))
    GovUkNotify().send_email_unfinished_application(
        email_address=session['application']['email'],
        expiry_days=datetime.strftime(local + timedelta(days=90), '%d/%m/%Y %H:%M:%S'),
        grc_return_link=str(request.url_root).replace('http://', 'https://')
    )

    reference_number = reference_number_string(session['reference_number'])
    save_progress()
    session.clear()

    return render_template(
        'save-and-return/exit-application.html',
        reference_number=reference_number
    )
