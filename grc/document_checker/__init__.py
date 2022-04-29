from distutils.util import strtobool
from flask import Blueprint, flash, redirect, render_template, request, url_for, session, current_app
from notifications_python_client.notifications import NotificationsAPIClient
from grc.document_checker.doc_checker_data_store import DocCheckerDataStore
from grc.document_checker.doc_checker_state import DocCheckerState, CurrentlyInAPartnershipEnum
from grc.document_checker.forms import PreviousNamesCheck, MarriageCivilPartnershipForm, StayTogetherForm, PartnerAgreesForm, PartnerDiedForm, InterimCheckForm, OverseasApprovedCheckForm, EmailForm, ValidateEmailForm
from grc.utils.security_code import send_security_code
from grc.utils.threading import Threading

documentChecker = Blueprint('documentChecker', __name__)


@documentChecker.route('/check-documents', methods=['GET', 'POST'])
def index():
    return render_template('document-checker/start.html')


@documentChecker.route('/check-documents/changed-name-to-reflect-gender', methods=['GET', 'POST'])
def previousNamesCheck():
    form = PreviousNamesCheck()
    doc_checker_state = DocCheckerDataStore.load_doc_checker_state()

    if form.validate_on_submit():
        doc_checker_state.changed_name_to_reflect_gender = strtobool(form.changed_name_to_reflect_gender.data)
        DocCheckerDataStore.save_doc_checker_state(doc_checker_state)

        return redirect(url_for('documentChecker.currentlyInAPartnership'))

    if request.method == 'GET':
        form.changed_name_to_reflect_gender.data = doc_checker_state.changed_name_to_reflect_gender

    return render_template(
        'document-checker/previous-names-check.html',
        form=form
    )


@documentChecker.route('/check-documents/currently-in-a-partnership', methods=['GET', 'POST'])
def currentlyInAPartnership():
    form = MarriageCivilPartnershipForm()
    doc_checker_state = DocCheckerDataStore.load_doc_checker_state()

    if form.validate_on_submit():
        doc_checker_state.currently_in_a_partnership = CurrentlyInAPartnershipEnum(form.currently_in_a_partnership.data)
        DocCheckerDataStore.save_doc_checker_state(doc_checker_state)

        if doc_checker_state.currently_in_a_partnership.is_currently_in_partnership:
            next_step = 'documentChecker.stayTogether'
        else:
            next_step = 'documentChecker.partnerDied'

        return redirect(url_for(next_step))

    if request.method == 'GET':
        form.currently_in_a_partnership.data = (
            doc_checker_state.currently_in_a_partnership.name
            if doc_checker_state.currently_in_a_partnership is not None
            else None
        )

    return render_template(
        'document-checker/currently_in_a_partnership.html',
        form=form,
        CurrentlyInAPartnershipEnum=CurrentlyInAPartnershipEnum
    )


@documentChecker.route('/check-documents/partnership-details/stay-together', methods=['GET', 'POST'])
def stayTogether():
    form = StayTogetherForm()

    if form.validate_on_submit():
        session['documentChecker']['partnershipDetails']['stayTogether'] = form.check.data
        session['documentChecker'] = session['documentChecker']

        # if form.check.data == 'Yes':
        #     next_step = 'documentChecker.partnerAgrees'
        # else:
        #     next_step = 'documentChecker.interimCheck'
        next_step = 'documentChecker.overseas_approved_check'

        return redirect(url_for(next_step))

    return render_template(
        'document-checker/stay-together.html',
        form=form
    )


@documentChecker.route('/check-documents/partnership-details/partner-agrees', methods=['GET', 'POST'])
def partnerAgrees():
    form = PartnerAgreesForm()

    if form.validate_on_submit():
        session['documentChecker']['partnershipDetails']['partnerAgrees'] = form.check.data
        session['documentChecker'] = session['documentChecker']

        if form.check.data == 'Yes':
            next_step = 'documentChecker.checkYourAnswers'
        else:
            next_step = 'documentChecker.interimCheck'

        return redirect(url_for(next_step))

    return render_template(
        'document-checker/partner-agrees.html',
        form=form
    )


@documentChecker.route('/check-documents/partnership-details/interim-check', methods=['GET', 'POST'])
def interimCheck():
    form = InterimCheckForm()

    if request.method == 'POST':
        session['documentChecker']['partnershipDetails']['interimCheck'] = 'Yes'
        session['documentChecker'] = session['documentChecker']

        # set current step in case user exits the app
        next_step = 'documentChecker.checkYourAnswers'

        return redirect(url_for(next_step))

    if session['documentChecker']['partnershipDetails']['stayTogether'] == 'No':
        back = 'documentChecker.stayTogether'
    else:
        back = 'documentChecker.partnerAgrees'

    return render_template(
        'document-checker/interim-check.html',
        form=form,
        back=back
    )


@documentChecker.route('/check-documents/partnership-details/partner-died', methods=['GET', 'POST'])
def partnerDied():
    form = PartnerDiedForm()

    if form.validate_on_submit():
        session['documentChecker']['partnershipDetails']['partnerDied'] = form.check.data
        session['documentChecker'] = session['documentChecker']
        next_step = 'documentChecker.endedCheck'

        return redirect(url_for(next_step))

    return render_template(
        'document-checker/partner-died.html',
        form=form
    )


@documentChecker.route('/check-documents/partnership-details/ended-check', methods=['GET', 'POST'])
def endedCheck():
    form = PartnerDiedForm()

    if form.validate_on_submit():
        session['documentChecker']['partnershipDetails']['endedCheck'] = form.check.data
        session['documentChecker'] = session['documentChecker']

        # set current step in case user exits the app
        next_step = 'documentChecker.overseas_approved_check'

        return redirect(url_for(next_step))

    return render_template(
        'document-checker/ended-check.html',
        form=form
    )


@documentChecker.route('/check-documents/overseas-approved-check', methods=['GET', 'POST'])
def overseas_approved_check():
    form = OverseasApprovedCheckForm()

    if form.validate_on_submit():
        session['documentChecker']['confirmation']['overseasApprovedCheck'] = form.check.data
        session['documentChecker'] = session['documentChecker']

        return redirect(url_for('documentChecker.your_documents'))

    if session['documentChecker']['partnershipDetails']['marriageCivilPartnership'] == 'Neither':
        back = 'documentChecker.endedCheck'
    else:
        back = 'documentChecker.stayTogether'

    return render_template(
        'document-checker/overseas-approved-check.html',
        form=form,
        back=back
    )


@documentChecker.route('/check-documents/your-documents', methods=['GET', 'POST'])
def your_documents():
    return render_template('document-checker/your-documents.html')


@documentChecker.route('/check-documents/email-address', methods=['GET', 'POST'])
def email():
    if 'documentChecker' not in session or session['documentChecker']['confirmation']['overseasApprovedCheck'] == '':
        return redirect(url_for('documentChecker.index'))

    form = EmailForm()

    if form.validate_on_submit():
        session['email'] = form.email.data
        session.modified = True
        try:
            send_security_code(form.email.data)
            return redirect(url_for('documentChecker.emailConfirmation'))
        except BaseException as err:
            error = err.args[0].json()
            flash(error['errors'][0]['message'], 'error')

    return render_template(
        'document-checker/email-address.html',
        form=form
    )


@documentChecker.route('/check-documents/email-confirmation', methods=['GET', 'POST'])
def emailConfirmation():
    if 'email' not in session or session['email'] is None:
        return redirect(url_for('documentChecker.email'))

    form = ValidateEmailForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            return redirect(url_for('documentChecker.confirmation'))
        else:
            threading = Threading(form.attempt.data)
            form.attempt.data = threading.throttle()

    elif request.args.get('resend') == 'true':
        try:
            send_security_code(session['email'])
            flash(
                'We’ve resent you a security code. This can take a few minutes to arrive.',
                'email',
            )
        except BaseException as err:
            error = err.args[0].json()
            flash(error['errors'][0]['message'], 'error')

    return render_template(
        'document-checker/security-code.html',
        form=form,
        email=session['email']
    )


@documentChecker.route('/check-documents/confirmation', methods=['GET'])
def confirmation():
    if 'email' not in session or session['email'] is None:
        return redirect(url_for('documentChecker.email'))

    # Notify success
    if current_app.config['NOTIFY_OVERRIDE_EMAIL']:
        send_to = current_app.config['NOTIFY_OVERRIDE_EMAIL']
    else:
        send_to = session['email']

    notifications_client = NotificationsAPIClient(current_app.config['NOTIFY_API'])
    notifications_client.send_email_notification(
        email_address=send_to,
        template_id=current_app.config['NOTIFY_DOCUMENT_CHECKER_LIST_TEMPLATE_ID'],
        personalisation={
            'documents_list': render_template('document-checker/documents.html')
        }
    )

    return render_template('document-checker/confirmation.html')
