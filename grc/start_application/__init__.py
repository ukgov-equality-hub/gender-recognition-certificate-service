from flask import Blueprint, flash, render_template, request, url_for, session
from grc.business_logic.data_store import DataStore
from grc.business_logic.data_structures.application_data import ApplicationData
from grc.models import Application, ApplicationStatus
from grc.start_application.forms import EmailAddressForm, SecurityCodeForm, OverseasCheckForm, \
    OverseasApprovedCheckForm, DeclerationForm, IsFirstVisitForm
from grc.utils.get_next_page import get_next_page_global, get_previous_page_global
from grc.utils.security_code import send_security_code
from grc.utils.decorators import EmailRequired, LoginRequired, Unauthorized, ValidatedEmailRequired
from grc.utils.reference_number import reference_number_string
from grc.utils.redirect import local_redirect
from grc.utils.logger import LogLevel, Logger
from grc.utils.strtobool import strtobool

startApplication = Blueprint('startApplication', __name__)
logger = Logger()


@startApplication.route('/', methods=['GET', 'POST'])
@Unauthorized
def index():
    logger.log(LogLevel.INFO, "FIRING logging index")
    form = EmailAddressForm()

    if form.validate_on_submit():
        session.clear()
        session['email'] = form.email.data
        try:
            send_security_code(form.email.data)
            return local_redirect(url_for('startApplication.securityCode'))
        except BaseException as err:
            error = err.args[0].json()
            flash(error['errors'][0]['message'], 'error')

    return render_template(
        'start-application/email-address.html',
        form=form
    )


@startApplication.route('/security-code', methods=['GET', 'POST'])
@EmailRequired
@Unauthorized
def securityCode():
    form = SecurityCodeForm()

    if request.method == 'POST':
        email = session['email']
        if form.validate_on_submit():
            session.clear()  # Clear out session['email']
            session['validatedEmail'] = email
            return local_redirect(url_for('startApplication.isFirstVisit'))
        else:
            logger.log(LogLevel.WARN, f"{logger.mask_email_address(email)} entered an incorrect security code")

    elif request.args.get('resend') == 'true':
        try:
            send_security_code(session['email'])
            flash('We’ve resent you a security code. This can take a few minutes to arrive.', 'email')
        except BaseException as err:
            error = err.args[0].json()
            flash(error['errors'][0]['message'], 'error')

    return render_template(
        'security-code.html',
        form=form,
        email=session['email']
    )


@startApplication.route('/is-first-visit', methods=['GET', 'POST'])
@ValidatedEmailRequired
@Unauthorized
def isFirstVisit():
    form = IsFirstVisitForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            if form.isFirstVisit.data == 'FIRST_VISIT' or form.isFirstVisit.data == 'LOST_REFERENCE':
                try:
                    application = DataStore.create_new_application(email_address=session['validatedEmail'])
                    session.clear()  # Clear out session['validatedEmail']
                    session['reference_number'] = application.reference_number
                    DataStore.increment_application_sessions(application.reference_number)
                    return local_redirect(url_for('startApplication.reference'))

                except BaseException as err:
                    flash('There is a problem creating a new application', 'error')
                    return render_template('start-application/is-first-visit.html', form=form)

            elif form.isFirstVisit.data == 'HAS_REFERENCE':
                application = loadApplicationFromDatabaseByReferenceNumber(form.reference.data)
                if application is None:
                    # This should already be caught by the 'validateReferenceNumber' custom form validator
                    return returnToIsFirstVisitPageWithInvalidReferenceError(form)

                else:
                    if (not application.email) or \
                            application.status == ApplicationStatus.DELETED or \
                            application.status == ApplicationStatus.ABANDONED:
                        # This application has been anonymised (i.e. after it's been submitted and processed OR after it's been abandoned)
                        # Show the user a friendly page explaining this
                        logger.log(LogLevel.WARN, f"{logger.mask_email_address(session['validatedEmail'])} attempted to access an anonymised application")
                        return render_template('start-application/application-anonymised.html')

                    elif application.status == ApplicationStatus.COMPLETED or \
                            application.status == ApplicationStatus.SUBMITTED or \
                            application.status == ApplicationStatus.DOWNLOADED:
                        # This application has already been submitted
                        # Show the user a friendly page explaining this
                        logger.log(LogLevel.WARN, f"{logger.mask_email_address(session['validatedEmail'])} attempted to access a submitted application")
                        return render_template('start-application/application-already-submitted.html')

                    elif application.email == session['validatedEmail']:
                        # The reference number is associated with their email address - load the application
                        logger.log(LogLevel.INFO, f"{logger.mask_email_address(session['validatedEmail'])} accessed their application")
                        session.clear()  # Clear out session['validatedEmail']
                        session['reference_number'] = application.reference_number
                        DataStore.increment_application_sessions(application.reference_number)
                        return local_redirect(url_for('taskList.index'))

                    else:
                        # This reference number is owned by another email address - pretend it doesn't exist
                        logger.log(LogLevel.WARN, f"{logger.mask_email_address(session['validatedEmail'])} attempted to access someone elses application")
                        return returnToIsFirstVisitPageWithInvalidReferenceError(form)

    return render_template(
        'start-application/is-first-visit.html',
        form=form
    )


def loadApplicationFromDatabaseByReferenceNumber(reference) -> Application:
    trimmed_reference = reference.replace('-', '').replace(' ', '').upper()
    return Application.query.filter_by(reference_number=trimmed_reference).first()


def returnToIsFirstVisitPageWithInvalidReferenceError(form):
    form.reference.errors.append('Enter a valid reference number')
    return render_template('start-application/is-first-visit.html', form=form)


@startApplication.route('/back-to-is-first-visit', methods=['GET', 'POST'])
@LoginRequired
def backToIsFirstVisit():
    application = loadApplicationFromDatabaseByReferenceNumber(session['reference_number'])
    session.clear()  # Clear out session['reference_number']
    session['validatedEmail'] = application.email
    return local_redirect(url_for('startApplication.isFirstVisit'))


@startApplication.route('/reference-number', methods=['GET'])
@LoginRequired
def reference():
    return render_template(
        'start-application/reference-number.html',
        reference_number=reference_number_string(session['reference_number'])
    )


@startApplication.route('/overseas-check', methods=['GET', 'POST'])
@LoginRequired
def overseas_check():
    form = OverseasCheckForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.confirmation_data.gender_recognition_outside_uk = strtobool(form.overseasCheck.data)

        if not application_data.confirmation_data.gender_recognition_outside_uk:
            application_data.confirmation_data.gender_recognition_from_approved_country = None

        DataStore.save_application(application_data)

        if application_data.confirmation_data.gender_recognition_outside_uk:
            return get_next_page(application_data, 'startApplication.overseas_approved_check')
        else:
            return get_next_page(application_data, 'startApplication.declaration')

    elif request.method == 'GET':
        form.overseasCheck.data = application_data.confirmation_data.gender_recognition_outside_uk

    return render_template(
        'start-application/overseas-check.html',
        form=form,
        back=get_previous_page(application_data, 'startApplication.reference')
    )


@startApplication.route('/overseas-approved-check', methods=['GET', 'POST'])
@LoginRequired
def overseas_approved_check():
    form = OverseasApprovedCheckForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.confirmation_data.gender_recognition_from_approved_country = strtobool(form.overseasApprovedCheck.data)
        DataStore.save_application(application_data)

        return get_next_page(application_data, 'startApplication.declaration')

    elif request.method == 'GET':
        form.overseasApprovedCheck.data = application_data.confirmation_data.gender_recognition_from_approved_country

    return render_template(
        'start-application/overseas-approved-check.html',
        form=form,
        back=get_previous_page(application_data, 'startApplication.overseas_check')
    )


@startApplication.route('/declaration', methods=['GET', 'POST'])
@LoginRequired
def declaration():
    form = DeclerationForm()
    application_data = DataStore.load_application_by_session_reference_number()
    back_link = ('startApplication.overseas_approved_check'
                 if application_data.confirmation_data.gender_recognition_outside_uk
                 else 'startApplication.overseas_check')

    if request.method == 'POST':
        if form.validate_on_submit():
            application_data.confirmation_data.consent_to_GRO_contact = form.consent.data
            DataStore.save_application(application_data)

            return get_next_page(application_data, 'taskList.index')

    else:
        form.consent.data = application_data.confirmation_data.consent_to_GRO_contact

    return render_template(
        'start-application/declaration.html',
        form=form,
        back=get_previous_page(application_data, back_link)
    )


@startApplication.route('/clearsession', methods=['GET'])
@LoginRequired
def clearsession():
    session.clear()
    return local_redirect(url_for('startApplication.index'))


def get_next_page(application_data: ApplicationData, next_page_in_journey: str):
    return get_next_page_global(
        next_page_in_journey=next_page_in_journey,
        section_check_your_answers_page=None,
        section_status=application_data.confirmation_data.section_status,
        application_data=application_data)


def get_previous_page(application_data: ApplicationData, previous_page_in_journey: str):
    return get_previous_page_global(
        previous_page_in_journey=previous_page_in_journey,
        section_check_your_answers_page=None,
        section_status=application_data.confirmation_data.section_status,
        application_data=application_data)
