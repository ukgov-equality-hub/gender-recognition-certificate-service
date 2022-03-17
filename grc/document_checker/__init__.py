from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from flask import render_template

from grc.models import ListStatus
from grc.document_checker.forms import PreviousNamesCheck, MarriageCivilPartnershipForm, StayTogetherForm, PartnerAgreesForm, PartnerDiedForm, InterimCheckForm, OverseasApprovedCheckForm



documentChecker = Blueprint('documentChecker', __name__)

@documentChecker.route('/check-documents', methods=['GET', 'POST'])
def index():
    if 'documentChecker' not in session:
        session['documentChecker'] = {
            "previousNamesCheck": "",
            "partnershipDetails": {
                "marriageCivilPartnership": "",
                "stayTogether": "",
                "partnerAgrees": "",
                "interimCheck": "",
                "partnerDied": ""
            },
            "confirmation": {
                "overseasApprovedCheck": ""
            }
        }

    return render_template('/document-checker/start.html')


@documentChecker.route('/check-documents/personal-details/previous-names-check', methods=['GET', 'POST'])
def previousNamesCheck():

    form = PreviousNamesCheck()

    if form.validate_on_submit():
        session["documentChecker"]["previousNamesCheck"] = form.check.data
        session['documentChecker'] = session["documentChecker"]

        return redirect(url_for('documentChecker.partnershipDetails'))

    return render_template('document-checker/previous-names-check.html', form=form)


@documentChecker.route('/check-documents/partnership-details', methods=['GET', 'POST'])
def partnershipDetails():

    form = MarriageCivilPartnershipForm()

    if form.validate_on_submit():
        session["documentChecker"]["partnershipDetails"]["marriageCivilPartnership"] = form.check.data
        session['documentChecker'] = session["documentChecker"]

        if form.check.data == 'Neither':
            next_step = 'documentChecker.partnerDied'
        else:
            next_step = 'documentChecker.stayTogether'

        return redirect(url_for(next_step))

    return render_template('document-checker/current-check.html', form=form)


@documentChecker.route('/check-documents/partnership-details/stay-together', methods=['GET', 'POST'])
def stayTogether():

    form = StayTogetherForm()

    if form.validate_on_submit():
        session["documentChecker"]["partnershipDetails"]["stayTogether"] = form.check.data
        session['documentChecker'] = session["documentChecker"]

        # if form.check.data == 'Yes':
        #     next_step = 'documentChecker.partnerAgrees'
        # else:
        #     next_step = 'documentChecker.interimCheck'
        next_step = 'documentChecker.overseas_approved_check'

        return redirect(url_for(next_step))

    return render_template('document-checker/stay-together.html', form=form)


@documentChecker.route('/check-documents/partnership-details/partner-agrees', methods=['GET', 'POST'])
def partnerAgrees():

    form = PartnerAgreesForm()

    if form.validate_on_submit():
        session["documentChecker"]["partnershipDetails"]["partnerAgrees"] = form.check.data
        session['documentChecker'] = session["documentChecker"]

        if form.check.data == 'Yes':
            next_step = 'documentChecker.checkYourAnswers'
        else:
            next_step = 'documentChecker.interimCheck'

        return redirect(url_for(next_step))

    return render_template('document-checker/partner-agrees.html', form=form)


@documentChecker.route('/check-documents/partnership-details/interim-check', methods=['GET', 'POST'])
def interimCheck():

    form = InterimCheckForm()

    if request.method == 'POST':
        session["documentChecker"]["partnershipDetails"]["interimCheck"] = 'Yes'
        session['documentChecker'] = session["documentChecker"]

        # set current step in case user exits the app
        next_step = 'documentChecker.checkYourAnswers'

        return redirect(url_for(next_step))

    if session["documentChecker"]["partnershipDetails"]["stayTogether"] == 'No':
        back = 'documentChecker.stayTogether'
    else:
        back = 'documentChecker.partnerAgrees'

    return render_template('document-checker/interim-check.html', form=form, back=back)



@documentChecker.route('/check-documents/partnership-details/partner-died', methods=['GET', 'POST'])
def partnerDied():

    form = PartnerDiedForm()

    if form.validate_on_submit():
        session["documentChecker"]["partnershipDetails"]["partnerDied"] = form.check.data
        session['documentChecker'] = session["documentChecker"]
        next_step = 'documentChecker.endedCheck'

        return redirect(url_for(next_step))

    return render_template('document-checker/partner-died.html', form=form)


@documentChecker.route('/check-documents/partnership-details/ended-check', methods=['GET', 'POST'])
def endedCheck():

    form = PartnerDiedForm()

    if form.validate_on_submit():
        session["documentChecker"]["partnershipDetails"]["endedCheck"] = form.check.data
        session['documentChecker'] = session["documentChecker"]

        # set current step in case user exits the app
        next_step = 'documentChecker.overseas_approved_check'

        return redirect(url_for(next_step))

    return render_template('document-checker/ended-check.html', form=form)

@documentChecker.route('/check-documents/overseas-approved-check', methods=['GET', 'POST'])
def overseas_approved_check():
    form = OverseasApprovedCheckForm()

    if form.validate_on_submit():
        session['documentChecker']["confirmation"]["overseasApprovedCheck"] = form.check.data
        session['documentChecker'] = session["documentChecker"]

        return redirect(url_for('documentChecker.your_documents'))

    if session["documentChecker"]["partnershipDetails"]["marriageCivilPartnership"] == 'Neither':
        back = 'documentChecker.endedCheck'
    else:
        back = 'documentChecker.stayTogether'

    return render_template('document-checker/overseas-approved-check.html',  form=form, back=back)

@documentChecker.route('/check-documents/your-documents', methods=['GET', 'POST'])
def your_documents():
    return render_template('document-checker/your-documents.html')
