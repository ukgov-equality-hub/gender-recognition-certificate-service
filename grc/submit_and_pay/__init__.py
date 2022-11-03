import os
import threading
from datetime import datetime
from flask import Blueprint, flash, render_template, request, current_app, url_for, session, copy_current_request_context, make_response
import requests
from requests.structures import CaseInsensitiveDict
import json
import uuid
from grc.business_logic.data_store import DataStore
from grc.business_logic.data_structures.application_data import ApplicationData
from grc.business_logic.data_structures.submit_and_pay_data import HelpWithFeesType
from grc.external_services.gov_uk_notify import GovUkNotify
from grc.models import db, Application, ApplicationStatus
from grc.list_status import ListStatus
from grc.submit_and_pay.forms import MethodCheckForm, HelpTypeForm, CheckYourAnswers
from grc.utils.application_files import ApplicationFiles
from grc.utils.decorators import LoginRequired
from grc.utils.get_next_page import get_next_page_global, get_previous_page_global
from grc.utils.redirect import local_redirect
from grc.utils.strtobool import strtobool

submitAndPay = Blueprint('submitAndPay', __name__)


@submitAndPay.route('/submit-and-pay', methods=['GET', 'POST'])
@LoginRequired
def index():
    form = MethodCheckForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.submit_and_pay_data.applying_for_help_with_fee = strtobool(form.applying_for_help_with_fee.data)

        if not application_data.submit_and_pay_data.applying_for_help_with_fee:
            application_data.submit_and_pay_data.how_applying_for_help_with_fees = None
            application_data.submit_and_pay_data.help_with_fees_reference_number = None

        DataStore.save_application(application_data)

        if application_data.submit_and_pay_data.applying_for_help_with_fee:
            return get_next_page(application_data, 'submitAndPay.helpType')
        else:
            return get_next_page(application_data, 'submitAndPay.checkYourAnswers')

    if request.method == 'GET':
        form.applying_for_help_with_fee.data = application_data.submit_and_pay_data.applying_for_help_with_fee

    return render_template(
        'submit-and-pay/method.html',
        form=form,
        back=get_previous_page(application_data, 'taskList.index')
    )


@submitAndPay.route('/submit-and-pay/help-type', methods=['GET', 'POST'])
@LoginRequired
def helpType():
    form = HelpTypeForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if request.method == 'POST':
        if form.validate_on_submit():
            application_data.submit_and_pay_data.how_applying_for_help_with_fees = \
                HelpWithFeesType[form.how_applying_for_fees.data]

            if application_data.submit_and_pay_data.how_applying_for_help_with_fees == HelpWithFeesType.USING_ONLINE_SERVICE:
                application_data.submit_and_pay_data.help_with_fees_reference_number = form.help_with_fees_reference_number.data
            else:
                application_data.submit_and_pay_data.help_with_fees_reference_number = None

            DataStore.save_application(application_data)

            return get_next_page(application_data, 'submitAndPay.checkYourAnswers')

    if request.method == 'GET' and application_data.submit_and_pay_data.how_applying_for_help_with_fees is not None:
        form.how_applying_for_fees.data = application_data.submit_and_pay_data.how_applying_for_help_with_fees.name
        form.help_with_fees_reference_number.data = application_data.submit_and_pay_data.help_with_fees_reference_number

    return render_template(
        'submit-and-pay/help-type.html',
        form=form,
        back=get_previous_page(application_data, 'submitAndPay.index')
    )


@submitAndPay.route('/submit-and-pay/check-your-answers', methods=['GET', 'POST'])
@LoginRequired
def checkYourAnswers():
    form = CheckYourAnswers()
    application_data = DataStore.load_application_by_session_reference_number()

    if application_data.section_status_submit_and_pay_data != ListStatus.IN_REVIEW:
        return local_redirect(url_for('taskList.index'))

    if request.method == 'POST' and form.validate_on_submit():
        application_data.submit_and_pay_data.declaration = form.certify.data

        if application_data.submit_and_pay_data.applying_for_help_with_fee:
            application_data.submit_and_pay_data.is_submitted = True
            DataStore.save_application(application_data)

            return local_redirect(url_for('submitAndPay.confirmation'))
        else:
            random_uuid = str(uuid.uuid4())
            return_link = request.url_root if os.getenv('TEST_URL', '') != '' or os.getenv('FLASK_ENV', '') == 'development' else str(request.url_root).replace('http://', 'https://')
            data = {
                'amount': 500,
                'reference': application_data.reference_number,
                'description': 'Pay for Gender Recognition Certificate',
                'return_url': return_link + 'submit-and-pay/payment-confirmation/' + random_uuid,
                'delayed_capture': False,
                'language': 'en'
            }

            headers = CaseInsensitiveDict()
            headers['Accept'] = 'application/json'
            headers['Authorization'] = 'Bearer ' + current_app.config['GOVUK_PAY_API_KEY']

            try:
                r = requests.post(
                    current_app.config['GOVUK_PAY_API'] + 'v1/payments',
                    headers=headers,
                    json=data
                )
                res = json.loads(r.text)

                application_data.submit_and_pay_data.gov_pay_payment_id = res['payment_id']
                application_data.submit_and_pay_data.gov_pay_uuid = random_uuid
                DataStore.save_application(application_data)

                return local_redirect(res['_links']['next_url']['href'])
            except BaseException as err:
                flash(err, 'error')

    if application_data.submit_and_pay_data.applying_for_help_with_fee:
        back_link = 'submitAndPay.helpType'
    else:
        back_link = 'submitAndPay.index'

    return render_template(
        'submit-and-pay/check-your-answers.html',
        form=form,
        application_data=application_data,
        back=get_previous_page(application_data, back_link)
    )


@submitAndPay.route('/submit-and-pay/download', methods=['GET'])
@LoginRequired
def download():
    from grc.utils.application_files import ApplicationFiles

    application_data = DataStore.load_application_by_session_reference_number()

    bytes, file_name = ApplicationFiles().create_or_download_pdf(
        application_data.reference_number,
        application_data,
        is_admin=False,
        download=True
    )

    response = make_response(bytes)
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename=file_name)
    return response


@submitAndPay.route('/submit-and-pay/payment-confirmation/<uuid:id>', methods=['GET', 'POST'])
@LoginRequired
def paymentConfirmation(id):
    application_data = DataStore.load_application_by_session_reference_number()

    if application_data.submit_and_pay_data.gov_pay_uuid == str(id):
        headers = CaseInsensitiveDict()
        headers['Accept'] = 'application/json'
        headers['Authorization'] = 'Bearer ' + current_app.config['GOVUK_PAY_API_KEY']

        try:
            r = requests.get(
                current_app.config['GOVUK_PAY_API'] + 'v1/payments/' + application_data.submit_and_pay_data.gov_pay_payment_id,
                headers=headers
            )
            res = json.loads(r.text)
            if res['state']['status'] == 'success' and res['state']['finished'] == True:
                application_data.submit_and_pay_data.is_submitted = True
                application_data.submit_and_pay_data.gov_pay_payment_details = r.text
                DataStore.save_application(application_data)
                return local_redirect(url_for('submitAndPay.confirmation'))
            elif res['state']['status'] == 'failed':
                flash(res['state']['message'], 'error')
        except BaseException as err:
            flash(err, 'error')
    else:
        flash('Something went wrong', 'error')

    return local_redirect(url_for('submitAndPay.checkYourAnswers'))


@submitAndPay.route('/submit-and-pay/confirmation', methods=['GET'])
@LoginRequired
def confirmation():
    application_data = DataStore.load_application_by_session_reference_number()
    mark_complete(application_data.reference_number)

    @copy_current_request_context
    def create_files(reference_number, application_data):
        from grc.utils.application_files import ApplicationFiles
        ApplicationFiles().create_or_download_attachments(
            reference_number,
            application_data,
            download=False
        )
        ApplicationFiles().create_or_download_pdf(
            reference_number,
            application_data
        )

        mark_files_created(reference_number)

    threading.Thread(target=create_files, args=[application_data.reference_number, application_data]).start()

    GovUkNotify().send_email_completed_application(
        email_address=application_data.email_address,
        documents_to_be_posted=render_template('documents.html', application_data=application_data)
    )

    applications_to_anonymise = Application.query.filter(
        Application.status == ApplicationStatus.STARTED,
        Application.email == application_data.email_address,
        Application.reference_number != application_data.reference_number
    )

    for application_to_anonymise in applications_to_anonymise:
        anonymise_application(application_to_anonymise)

    html = render_template(
        'submit-and-pay/confirmation.html',
        application_data=application_data
    )
    session.clear()
    return html


def mark_complete(reference_number: str):
    application_record = Application.query.filter_by(
        reference_number=reference_number
    ).first()

    if application_record is not None:
        try:
            application_record.updated = datetime.now()
            application_record.status = ApplicationStatus.SUBMITTED
            db.session.commit()
        except ValueError:
            print('Oops!  Something went wrong.', flush=True)
    else:
        print('Application does not exist', flush=True)


def mark_files_created(reference_number: str):
    application = Application.query.filter_by(
        reference_number=reference_number
    ).first()

    if application is not None:
        application.filesCreated = True
        db.session.commit()


def get_next_page(application_data: ApplicationData, next_page_in_journey: str):
    return get_next_page_global(
        next_page_in_journey=next_page_in_journey,
        section_check_your_answers_page=None,
        section_status=application_data.section_status_submit_and_pay_data,
        application_data=application_data)


def get_previous_page(application_data: ApplicationData, previous_page_in_journey: str):
    return get_previous_page_global(
        previous_page_in_journey=previous_page_in_journey,
        section_check_your_answers_page=None,
        section_status=application_data.section_status_submit_and_pay_data,
        application_data=application_data)


def anonymise_application(application_to_anonymise):
    ApplicationFiles().delete_application_files(
        application_to_anonymise.reference_number,
        application_to_anonymise.application_data(),
    )
    application_to_anonymise.email = ''
    application_to_anonymise.user_input = ''
    application_to_anonymise.status = ApplicationStatus.ABANDONED

    db.session.commit()
