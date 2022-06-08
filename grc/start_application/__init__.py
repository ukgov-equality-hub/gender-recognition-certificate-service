from flask import Blueprint, flash, render_template, request, url_for, session
from grc.models import ListStatus, Application, ApplicationStatus
from grc.start_application.forms import EmailAddressForm, SecurityCodeForm, OverseasCheckForm, \
    OverseasApprovedCheckForm, DeclerationForm, IsFirstVisitForm
from grc.utils.security_code import send_security_code
from grc.utils.decorators import EmailRequired, LoginRequired, Unauthorized, ValidatedEmailRequired
from grc.utils.reference_number import reference_number_generator, reference_number_string
from grc.utils.application_progress import save_progress
from grc.utils.redirect import local_redirect

startApplication = Blueprint('startApplication', __name__)


@startApplication.route('/', methods=['GET', 'POST'])
@Unauthorized
def index():
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
        if form.validate_on_submit():
            email = session['email']
            session.clear()  # Clear out session['email']
            session['validatedEmail'] = email
            return local_redirect(url_for('startApplication.isFirstVisit'))

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
                reference_number = reference_number_generator(session['validatedEmail'])
                if reference_number != False:
                    session.clear()  # Clear out session['validatedEmail']
                    session['reference_number'] = reference_number
                    session['application'] = save_progress()
                    return local_redirect(url_for('startApplication.reference'))

                else:
                    flash('There is a problem creating a new application', 'error')
                    return render_template('start-application/is-first-visit.html', form=form)

            elif form.isFirstVisit.data == 'HAS_REFERENCE':
                application = loadApplicationFromDatabaseByReferenceNumber(form.reference.data)
                if application is None:
                    # This should already be caught by the 'validateReferenceNumber' custom form validator
                    return returnToIsFirstVisitPageWithInvalidReferenceError(form)

                else:
                    if not application.email:
                        # This application has been anonymised (i.e. after it's been submitted and processed)
                        # Show the user a friendly page explaining this
                        return render_template('start-application/application-already-submitted.html')

                    elif application.status == ApplicationStatus.COMPLETED or \
                            application.status == ApplicationStatus.SUBMITTED or \
                            application.status == ApplicationStatus.DOWNLOADED or \
                            application.status == ApplicationStatus.DELETED:
                        # This application has already been submitted
                        # Show the user a friendly page explaining this
                        return render_template('start-application/application-already-submitted.html')

                    elif application.email == session['validatedEmail']:
                        # The reference number is associated with their email address - load the application
                        session.clear()  # Clear out session['validatedEmail']
                        session['reference_number'] = application.reference_number
                        session['application'] = application.data()
                        save_progress()
                        return local_redirect(url_for('taskList.index'))

                    else:
                        # This reference number is owned by another email address - pretend it doesn't exist
                        return returnToIsFirstVisitPageWithInvalidReferenceError(form)

    return render_template(
        'start-application/is-first-visit.html',
        form=form
    )


def loadApplicationFromDatabaseByReferenceNumber(reference):
    trimmed_reference = reference.replace('-', '').replace(' ', '').upper()
    return Application.query.filter_by(reference_number=trimmed_reference).first()


def returnToIsFirstVisitPageWithInvalidReferenceError(form):
    form.reference.errors.append('Enter a valid reference number')
    return render_template('start-application/is-first-visit.html', form=form)


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

    if form.validate_on_submit():
        session['application']['confirmation']['overseasCheck'] = form.overseasCheck.data
        session['application'] = save_progress()

        if form.overseasCheck.data == 'Yes':
            return local_redirect(url_for('startApplication.overseas_approved_check'))
        else:
            return local_redirect(url_for('startApplication.declaration'))

    else:
        form.overseasCheck.data = session['application']['confirmation']['overseasCheck']
        return render_template(
            'start-application/overseas-check.html',
            form=form
        )


@startApplication.route('/overseas-approved-check', methods=['GET', 'POST'])
@LoginRequired
def overseas_approved_check():
    form = OverseasApprovedCheckForm()

    if form.validate_on_submit():
        session['application']['confirmation']['overseasApprovedCheck'] = form.overseasApprovedCheck.data
        session['application'] = save_progress()

        return local_redirect(url_for('startApplication.declaration'))

    else:
        form.overseasApprovedCheck.data = session['application']['confirmation']['overseasApprovedCheck']
        return render_template(
            'start-application/overseas-approved-check.html',
            form=form
        )


@startApplication.route('/declaration', methods=['GET', 'POST'])
@LoginRequired
def declaration():
    form = DeclerationForm()
    back = (url_for('startApplication.overseas_approved_check')
            if session['application']['confirmation']['overseasCheck'] == 'Yes'
            else url_for('startApplication.overseas_check'))

    if request.method == 'POST':
        if form.validate_on_submit():
            session['application']['confirmation']['declaration'] = form.consent.data
            session['application']['confirmation']['progress'] = ListStatus.COMPLETED.name
            session['application'] = save_progress()

            return local_redirect(url_for('taskList.index'))

        session['application']['confirmation']['progress'] = ListStatus.IN_REVIEW.name
        session['application'] = save_progress()

        return render_template(
            'start-application/declaration.html',
            form=form,
            back=back
        )

    else:
        session['application']['confirmation']['progress'] = ListStatus.IN_REVIEW.name
        session['application'] = save_progress()
        form.consent.data = session['application']['confirmation']['declaration'] == True

        return render_template(
            'start-application/declaration.html',
            form=form,
            back=back
        )


@startApplication.route('/clearsession', methods=['GET'])
@LoginRequired
def clearsession():
    session.clear()
    return local_redirect(url_for('startApplication.index'))
