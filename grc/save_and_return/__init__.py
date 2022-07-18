from datetime import datetime, timedelta
from dateutil import tz
from flask import Blueprint, render_template, request, session
from grc.business_logic.data_store import DataStore
from grc.external_services.gov_uk_notify import GovUkNotify
from grc.utils.reference_number import reference_number_string
from grc.utils.decorators import LoginRequired

saveAndReturn = Blueprint('saveAndReturn', __name__)


@saveAndReturn.route('/save-and-return/exit-application', methods=['GET'])
@LoginRequired
def exitApplication():
    application_data = DataStore.load_application_by_session_reference_number()

    local = datetime.now().replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/London'))
    GovUkNotify().send_email_unfinished_application(
        email_address=application_data.email_address,
        expiry_days=datetime.strftime(local + timedelta(days=90), '%d/%m/%Y %H:%M:%S'),
        grc_return_link=str(request.url_root).replace('http://', 'https://')
    )

    reference_number = reference_number_string(application_data.reference_number)
    session.clear()

    return render_template(
        'save-and-return/exit-application.html',
        reference_number=reference_number
    )
