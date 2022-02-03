from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, session
)
from werkzeug.exceptions import abort
from flask import render_template
import json

from grc.models import db, Application
from grc.start_application.forms import SaveYourApplicationForm, ValidateEmailForm, OverseasCheckForm, OverseasApprovedCheckForm, DeclerationForm

from grc.utils.security_code import send_security_code
from grc.utils.decorators import EmailRequired, LoginRequired, Unauthorized
from grc.utils.reference_number import reference_number_generator, reference_number_string
from grc.utils.application_progress import save_progress


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

    return render_template('start-application/email-address.html', form=form)


@startApplication.route('/email-confirmation', methods=['GET', 'POST'])
@EmailRequired
@Unauthorized
def emailConfirmation():
    form = ValidateEmailForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            session['reference_number'] = reference_number_generator(session['email'])
            session['application'] = save_progress()

            return redirect(url_for('startApplication.reference'))
    elif request.args.get('resend') == 'true':
        try:
            send_security_code(session['email'])
            flash('We’ve resent you a security code. This can take a few minutes to arrive.', 'email')
        except BaseException as err:
            error = err.args[0].json()
            flash(error['errors'][0]['message'], 'error')

    return render_template('security-code.html', form=form, action=url_for('startApplication.emailConfirmation'), back=url_for('startApplication.index'), email=session['email'])


@startApplication.route('/reference-number', methods=['GET'])
@LoginRequired
def reference():
    return render_template('start-application/reference-number.html', reference_number=reference_number_string(session['reference_number']))

@startApplication.route('/overseas-check', methods=['GET', 'POST'])
@LoginRequired
def overseas_check():
    form = OverseasCheckForm()

    if form.validate_on_submit():
        session['application']["confirmation"]["overseasCheck"] = form.check.data
        session['application'] = save_progress()

        if form.check.data == 'Yes':
            return redirect(url_for('startApplication.overseas_approved_check'))
        else:
            return redirect(url_for('startApplication.declaration'))

    return render_template('start-application/overseas-check.html',  form=form)


@startApplication.route('/overseas-approved-check', methods=['GET', 'POST'])
@LoginRequired
def overseas_approved_check():
    form = OverseasApprovedCheckForm()

    if form.validate_on_submit():
        session['application']["confirmation"]["overseasApprovedCheck"] = form.check.data
        session['application'] = save_progress()

        return redirect(url_for('startApplication.declaration'))

    return render_template('start-application/overseas-approved-check.html',  form=form)


@startApplication.route('/declaration', methods=['GET', 'POST'])
@LoginRequired
def declaration():
    form = DeclerationForm()
    back = url_for('startApplication.overseas_check')

    if form.validate_on_submit():
        session['application']["confirmation"]["declaration"] = form.check.data
        session['application'] = save_progress()

        return redirect(url_for('taskList.index'))

    return render_template('start-application/declaration.html',  form=form, back=back)
