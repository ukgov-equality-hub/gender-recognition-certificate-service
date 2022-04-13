from flask import Blueprint, flash, redirect, render_template, request, url_for, session
import json
from grc.models import ListStatus
from grc.start_application.forms import SaveYourApplicationForm, ValidateEmailForm, OverseasCheckForm, OverseasApprovedCheckForm, DeclerationForm
from grc.utils.security_code import send_security_code
from grc.utils.decorators import EmailRequired, LoginRequired, Unauthorized
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
            session['reference_number'] = reference_number_generator(session['email'])
            if session['reference_number'] != False:
                session['application'] = save_progress()

                return redirect(url_for(session['application']['confirmation']['step']))
            else:
                flash('There is a problem creating a new application', 'error')
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
        session['application']['confirmation']['overseasCheck'] = form.check.data

        if ListStatus[session['application']['confirmation']['progress']] == ListStatus.IN_PROGRESS:
            if form.check.data == 'Yes':
                session['application']['confirmation']['step'] = 'startApplication.overseas_approved_check'
            else:
                session['application']['confirmation']['step'] = 'startApplication.declaration'
        elif form.check.data == 'Yes':
            session['application']['confirmation']['step'] = 'startApplication.overseas_approved_check'

        session['application'] = save_progress()

        return redirect(url_for(session['application']['confirmation']['step']))

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
