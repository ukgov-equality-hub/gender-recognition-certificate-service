from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from flask import render_template

from grc.models import ListStatus
from grc.partnership_details.forms import MarriageCivilPartnershipForm, StayTogetherForm, PartnerAgreesForm, PartnerDiedForm, InterimCheckForm, CheckYourAnswers

from grc.utils.decorators import LoginRequired
from grc.utils.application_progress import save_progress


partnershipDetails = Blueprint('partnershipDetails', __name__)

@partnershipDetails.route('/partnership-details', methods=['GET', 'POST'])
@LoginRequired
def index():

    form = MarriageCivilPartnershipForm()

    if form.validate_on_submit():
        session["application"]["partnershipDetails"]["marriageCivilPartnership"] = form.check.data

        if form.check.data == 'Neither':
            session["application"]["partnershipDetails"]["step"] = 'partnershipDetails.partnerDied'
        else:
            session["application"]["partnershipDetails"]["step"] = 'partnershipDetails.stayTogether'

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["partnershipDetails"]["step"]))

    return render_template('partnership-details/current-check.html', form=form)


@partnershipDetails.route('/partnership-details/stay-together', methods=['GET', 'POST'])
@LoginRequired
def stayTogether():

    form = StayTogetherForm()

    if form.validate_on_submit():
        session["application"]["partnershipDetails"]["stayTogether"] = form.check.data

        if form.check.data == 'Yes':
            session["application"]["partnershipDetails"]["step"] = 'partnershipDetails.partnerAgrees'
        else:
            session["application"]["partnershipDetails"]["step"] = 'partnershipDetails.interimCheck'

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["partnershipDetails"]["step"]))

    return render_template('partnership-details/stay-together.html', form=form)


@partnershipDetails.route('/partnership-details/partner-agrees', methods=['GET', 'POST'])
@LoginRequired
def partnerAgrees():

    form = PartnerAgreesForm()

    if form.validate_on_submit():
        session["application"]["partnershipDetails"]["partnerAgrees"] = form.check.data

        if form.check.data == 'Yes':
            session["application"]["partnershipDetails"]["progress"] = ListStatus.IN_REVIEW.name
            session["application"]["partnershipDetails"]["step"] = 'partnershipDetails.checkYourAnswers'
        else:
            session["application"]["partnershipDetails"]["step"] = 'partnershipDetails.interimCheck'

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["partnershipDetails"]["step"]))

    return render_template('partnership-details/partner-agrees.html', form=form)


@partnershipDetails.route('/partnership-details/interim-check', methods=['GET', 'POST'])
@LoginRequired
def interimCheck():

    form = InterimCheckForm()

    if request.method == 'POST':
        session["application"]["partnershipDetails"]["interimCheck"] = 'Yes'

        # update progress status
        session["application"]["partnershipDetails"]["progress"] = ListStatus.IN_REVIEW.name

        # set current step in case user exits the app
        session["application"]["partnershipDetails"]["step"] = 'partnershipDetails.checkYourAnswers'

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["partnershipDetails"]["step"]))

    if session["application"]["partnershipDetails"]["stayTogether"] == 'No':
        back = 'partnershipDetails.stayTogether'
    else:
        back = 'partnershipDetails.partnerAgrees'

    return render_template('partnership-details/interim-check.html', form=form, back=back)



@partnershipDetails.route('/partnership-details/partner-died', methods=['GET', 'POST'])
@LoginRequired
def partnerDied():

    form = PartnerDiedForm()

    if form.validate_on_submit():
        session["application"]["partnershipDetails"]["partnerDied"] = form.check.data
        session["application"]["partnershipDetails"]["step"] = 'partnershipDetails.endedCheck'

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["partnershipDetails"]["step"]))

    return render_template('partnership-details/partner-died.html', form=form)


@partnershipDetails.route('/partnership-details/ended-check', methods=['GET', 'POST'])
@LoginRequired
def endedCheck():

    form = PartnerDiedForm()

    if form.validate_on_submit():
        session["application"]["partnershipDetails"]["endedCheck"] = form.check.data

        # update progress status
        session["application"]["partnershipDetails"]["progress"] = ListStatus.IN_REVIEW.name

        # set current step in case user exits the app
        session["application"]["partnershipDetails"]["step"] = 'partnershipDetails.checkYourAnswers'

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["partnershipDetails"]["step"]))

    return render_template('partnership-details/ended-check.html', form=form)


@partnershipDetails.route('/partnership-details/check-your-answers', methods=['GET', 'POST'])
@LoginRequired
def checkYourAnswers():

    form = CheckYourAnswers()

    if "partnershipDetails" not in session["application"] or (session["application"]["partnershipDetails"]["progress"] != ListStatus.IN_REVIEW.name and session["application"]["partnershipDetails"]["progress"] != ListStatus.COMPLETED.name):
        return redirect(url_for('taskList.index'))

    session["application"]["partnershipDetails"]["step"] = 'partnershipDetails.checkYourAnswers'

    if request.method == 'POST':
        # update progress status on Save and Continue
        session["application"]["partnershipDetails"]["progress"] = ListStatus.COMPLETED.name
        session["application"] = save_progress()
        return redirect(url_for('taskList.index'))

    # update progress status
    session["application"]["partnershipDetails"]["progress"] = ListStatus.IN_REVIEW.name
    session["application"] = save_progress()

    return render_template('partnership-details/check-your-answers.html', form=form)