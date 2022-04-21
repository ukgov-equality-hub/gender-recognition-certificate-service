from flask import Blueprint, flash, redirect, render_template, request, current_app, url_for, session
import requests
from requests.structures import CaseInsensitiveDict
import json
import uuid
from notifications_python_client.notifications import NotificationsAPIClient
from grc.models import ListStatus
from grc.submit_and_pay.forms import MethodCheckForm, HelpTypeForm, CheckYourAnswers
from grc.utils.decorators import LoginRequired
from grc.utils.application_progress import save_progress, mark_complete

submitAndPay = Blueprint('submitAndPay', __name__)


@submitAndPay.route('/submit-and-pay', methods=['GET', 'POST'])
@LoginRequired
def index():
    form = MethodCheckForm()

    if form.validate_on_submit():
        session['application']['submitAndPay']['method'] = form.check.data

        if form.check.data == 'Help':
            session['application']['submitAndPay']['progress'] = ListStatus.IN_PROGRESS.name
            session['application']['submitAndPay']['step'] = 'submitAndPay.helpType'
        else:
            session['application']['submitAndPay']['progress'] = ListStatus.IN_REVIEW.name
            session['application']['submitAndPay']['step'] = 'submitAndPay.checkYourAnswers'

        session['application'] = save_progress()

        return redirect(url_for(session['application']['submitAndPay']['step']))

    return render_template(
        'submit-and-pay/method.html',
        form=form
    )


@submitAndPay.route('/submit-and-pay/help-type', methods=['GET', 'POST'])
@LoginRequired
def helpType():
    form = HelpTypeForm()

    if request.method == 'POST':
        if 'Using the EX160 form' == form.check.data:
            form.referenceNumber.data = None

        if form.validate_on_submit():
            session['application']['submitAndPay']['helpType'] = form.check.data

            if 'Using the online service' == form.check.data:
                session['application']['submitAndPay']['referenceNumber'] = form.referenceNumber.data

            session['application']['submitAndPay']['progress'] = ListStatus.IN_REVIEW.name
            session['application']['submitAndPay']['step'] = 'submitAndPay.checkYourAnswers'
            session['application'] = save_progress()

            return redirect(url_for(session['application']['submitAndPay']['step']))

    if request.method == 'GET' and 'helpType' in session['application']['submitAndPay']:
        form.check.data = session['application']['submitAndPay']['helpType']
        form.referenceNumber.data = session['application']['submitAndPay']['referenceNumber']

    return render_template(
        'submit-and-pay/help-type.html',
        form=form
    )


@submitAndPay.route('/submit-and-pay/check-your-answers', methods=['GET', 'POST'])
@LoginRequired
def checkYourAnswers():
    form = CheckYourAnswers()

    if 'submitAndPay' not in session['application'] or (session['application']['submitAndPay']['progress'] != ListStatus.IN_REVIEW.name and session['application']['submitAndPay']['progress'] != ListStatus.COMPLETED.name):
        return redirect(url_for('taskList.index'))

    if request.method == 'POST' and form.validate_on_submit():
        session['application']['submitAndPay']['declaration'] = form.check.data

        if session['application']['submitAndPay']['method'] == 'Help':
            session['application']['submitAndPay']['progress'] = ListStatus.COMPLETED.name
            session['application']['submitAndPay']['step'] = 'submitAndPay.confirmation'
            session['application'] = save_progress()

            return redirect(url_for(session['application']['submitAndPay']['step']))
        else:
            random_uuid = str(uuid.uuid4())
            data = {
                'amount': 500,
                'reference':  session['application']['reference_number'],
                'description': 'Pay for Gender Recognition Certificate',
                'return_url': request.url_root + 'submit-and-pay/payment-confirmation/' + random_uuid,
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

                session['application']['submitAndPay']['payment_id'] = res['payment_id']
                session['application']['submitAndPay']['uuid'] = random_uuid
                session['application'] = save_progress()

                return redirect(res['_links']['next_url']['href'])
            except BaseException as err:
                flash(err, 'error')

    session['application']['submitAndPay']['progress'] = ListStatus.IN_REVIEW.name
    session['application'] = save_progress()

    return render_template(
        'submit-and-pay/check-your-answers.html',
        form=form
    )


@submitAndPay.route('/submit-and-pay/payment-confirmation/<uuid:id>', methods=['GET', 'POST'])
@LoginRequired
def paymentConfirmation(id):
    if 'uuid' in session['application']['submitAndPay'] and session['application']['submitAndPay']['uuid'] == str(id):
        headers = CaseInsensitiveDict()
        headers['Accept'] = 'application/json'
        headers['Authorization'] = 'Bearer ' + current_app.config['GOVUK_PAY_API_KEY']

        try:
            r = requests.get(
                current_app.config['GOVUK_PAY_API'] + 'v1/payments/' + session['application']['submitAndPay']['payment_id'],
                headers=headers
            )
            res = json.loads(r.text)
            if res['state']['status'] == 'success' and res['state']['finished'] == True:
                session['application']['submitAndPay']['progress'] = ListStatus.COMPLETED.name
                session['application']['submitAndPay']['step'] = 'submitAndPay.confirmation'
                session['application']['submitAndPay']['paymentDetails'] = r.text
                session['application'] = save_progress()
                return redirect(url_for('submitAndPay.confirmation'))
            elif res['state']['status'] == 'failed':
                flash(res['state']['message'], 'error')
        except BaseException as err:
            flash(err, 'error')
    else:
        flash('Something went wrong', 'error')

    return redirect(url_for('submitAndPay.checkYourAnswers'))


@submitAndPay.route('/submit-and-pay/confirmation', methods=['GET'])
@LoginRequired
def confirmation():
    mark_complete()

    if current_app.config['NOTIFY_OVERRIDE_EMAIL']:
        send_to = current_app.config['NOTIFY_OVERRIDE_EMAIL']
    else:
        send_to = session['application']['email']

    notifications_client = NotificationsAPIClient(current_app.config['NOTIFY_API'])
    notifications_client.send_email_notification(
        email_address=send_to,
        template_id=current_app.config['NOTIFY_COMPLETED_APPLICATION_EMAIL_TEMPLATE_ID'],
        personalisation={
            'documents_to_be_posted': render_template('documents.html')
        }
    )

    html = render_template('submit-and-pay/confirmation.html')
    session.clear()
    return html
