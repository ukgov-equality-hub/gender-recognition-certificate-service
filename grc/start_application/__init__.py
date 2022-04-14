from flask import Blueprint, flash, redirect, render_template, request, url_for, session
import json
from grc.models import ListStatus, Application
from grc.start_application.forms import SaveYourApplicationForm, ValidateEmailForm, OverseasCheckForm, OverseasApprovedCheckForm, DeclerationForm, IsFirstVisitForm
from grc.utils.security_code import send_security_code
from grc.utils.decorators import EmailRequired, LoginRequired, Unauthorized, ValidatedEmailRequired
from grc.utils.reference_number import reference_number_generator, reference_number_string
from grc.utils.application_progress import save_progress
from grc.utils.threading import Threading

startApplication = Blueprint('startApplication', __name__)


@startApplication.route('/', methods=['GET', 'POST'])
@Unauthorized
def index():
    form = SaveYourApplicationForm()

    if form.validate_on_submit():
        session.clear()
        session['email'] = form.email.data
        try:
            send_security_code(form.email.data)
            return redirect(url_for('startApplication.emailConfirmation'))
        except BaseException as err:
            error = err.args[0].json()
            flash(error['errors'][0]['message'], 'error')

    return render_template(
        'start-application/email-address.html',
        form=form
    )


@startApplication.route('/email-confirmation', methods=['GET', 'POST'])
@EmailRequired
@Unauthorized
def emailConfirmation():
    form = ValidateEmailForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            session['validatedEmail'] = session['email']
            return redirect(url_for('startApplication.isFirstVisit'))
        else:
            threading = Threading(form.attempt.data)
            form.attempt.data = threading.throttle()

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
        action=url_for('startApplication.emailConfirmation'),
        back=url_for('startApplication.index'),
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
                session['reference_number'] = reference_number_generator(session['email'])
                if session['reference_number'] != False:
                    session['application'] = save_progress()
                    return redirect(url_for(session['application']['confirmation']['step']))

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
                        # This application has already been submitted - show the user a friendly page explaining this
                        return render_template(
                            'start-application/application-already-submitted.html',
                            reference=reference_number_string(form.reference.data)
                        )

                    elif application.email == session['validatedEmail']:
                        # The reference number is associated with their email address - load the application
                        session['reference_number'] = application.reference_number
                        session['application'] = application.data()
                        return redirect(url_for('taskList.index'))

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

        if ListStatus[session['application']['confirmation']['progress']] == ListStatus.IN_PROGRESS:
            if form.overseasCheck.data == 'Yes':
                session['application']['confirmation']['step'] = 'startApplication.overseas_approved_check'
            else:
                session['application']['confirmation']['step'] = 'startApplication.declaration'
        elif form.overseasCheck.data == 'Yes':
            session['application']['confirmation']['step'] = 'startApplication.overseas_approved_check'

        session['application'] = save_progress()

        return redirect(url_for(session['application']['confirmation']['step']))

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
        session['application']['confirmation']['overseasApprovedCheck'] = form.check.data
        session['application']['confirmation']['step'] = 'startApplication.declaration'
        session['application'] = save_progress()

        return redirect(url_for(session['application']['confirmation']['step']))

    return render_template(
        'start-application/overseas-approved-check.html',
        form=form
    )


@startApplication.route('/declaration', methods=['GET', 'POST'])
@LoginRequired
def declaration():
    form = DeclerationForm()
    back = url_for('startApplication.overseas_check')

    if request.method == 'POST':
        if form.validate_on_submit():
            session['application']['confirmation']['declaration'] = form.check.data
            session['application']['confirmation']['progress'] = ListStatus.COMPLETED.name
            session['application']['confirmation']['step'] = 'startApplication.declaration'
            session['application'] = save_progress()

            return redirect(url_for('taskList.index'))

    session['application']['confirmation']['progress'] = ListStatus.IN_REVIEW.name
    session['application'] = save_progress()

    return render_template(
        'start-application/declaration.html',
        form=form,
        back=back
    )


@startApplication.route('/clearsession', methods=['GET'])
@LoginRequired
def clearsession():
    session.clear()
    return redirect(url_for('startApplication.index'))
