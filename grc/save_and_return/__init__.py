from flask import Blueprint, render_template, request, session
from grc.business_logic.data_store import DataStore
from grc.utils.reference_number import reference_number_string
from grc.utils.decorators import LoginRequired

saveAndReturn = Blueprint('saveAndReturn', __name__)


@saveAndReturn.route('/save-and-return/exit-application', methods=['GET'])
@LoginRequired
def exitApplication():
    application_data = DataStore.load_application_by_session_reference_number()

    reference_number = reference_number_string(application_data.reference_number)
    session.clear()

    return render_template(
        'save-and-return/exit-application.html',
        reference_number=reference_number
    )
