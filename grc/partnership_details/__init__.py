from flask import Blueprint, render_template, request, url_for, session
from grc.models import ListStatus
from grc.partnership_details.forms import MarriageCivilPartnershipForm, StayTogetherForm, PartnerAgreesForm, PartnerDiedForm, PreviousPartnershipEndedForm, InterimCheckForm, CheckYourAnswers
from grc.utils.decorators import LoginRequired
from grc.utils.application_progress import save_progress
from grc.utils.redirect import local_redirect

partnershipDetails = Blueprint('partnershipDetails', __name__)


@partnershipDetails.route('/partnership-details', methods=['GET', 'POST'])
@LoginRequired
def index():
    form = MarriageCivilPartnershipForm()

    if form.validate_on_submit():
        session['application']['partnershipDetails']['marriageCivilPartnership'] = form.currently_married.data
        session['application'] = save_progress()

        if form.currently_married.data == 'Neither':
            return local_redirect(url_for('partnershipDetails.partnerDied'))
        else:
            return local_redirect(url_for('partnershipDetails.stayTogether'))

    if request.method == 'GET':
        form.currently_married.data = (
            session['application']['partnershipDetails']['marriageCivilPartnership']
            if 'marriageCivilPartnership' in session['application']['partnershipDetails']
            else None
        )

    return render_template(
        'partnership-details/current-check.html',
        form=form
    )


@partnershipDetails.route('/partnership-details/stay-together', methods=['GET', 'POST'])
@LoginRequired
def stayTogether():
    form = StayTogetherForm()

    if form.validate_on_submit():
        session['application']['partnershipDetails']['stayTogether'] = form.stay_together.data
        session['application'] = save_progress()

        if form.stay_together.data == 'Yes':
            return local_redirect(url_for('partnershipDetails.partnerAgrees'))
        else:
            return local_redirect(url_for('partnershipDetails.interimCheck'))

    if request.method == 'GET':
        form.stay_together.data = (
            session['application']['partnershipDetails']['stayTogether']
            if 'stayTogether' in session['application']['partnershipDetails']
            else None
        )

    return render_template(
        'partnership-details/stay-together.html',
        form=form
    )


@partnershipDetails.route('/partnership-details/partner-agrees', methods=['GET', 'POST'])
@LoginRequired
def partnerAgrees():
    form = PartnerAgreesForm()

    if form.validate_on_submit():
        session['application']['partnershipDetails']['partnerAgrees'] = form.partner_agrees.data
        session['application'] = save_progress()

        if form.partner_agrees.data == 'Yes':
            session['application']['partnershipDetails']['progress'] = ListStatus.IN_REVIEW.name
            return local_redirect(url_for('partnershipDetails.checkYourAnswers'))
        else:
            return local_redirect(url_for('partnershipDetails.interimCheck'))

    if request.method == 'GET':
        form.partner_agrees.data = (
            session['application']['partnershipDetails']['partnerAgrees']
            if 'partnerAgrees' in session['application']['partnershipDetails']
            else None
        )

    return render_template(
        'partnership-details/partner-agrees.html',
        form=form
    )


@partnershipDetails.route('/partnership-details/interim-check', methods=['GET', 'POST'])
@LoginRequired
def interimCheck():
    form = InterimCheckForm()

    if request.method == 'POST':
        session['application']['partnershipDetails']['interimCheck'] = 'Yes'
        session['application']['partnershipDetails']['progress'] = ListStatus.IN_REVIEW.name
        session['application'] = save_progress()

        return local_redirect(url_for('partnershipDetails.checkYourAnswers'))

    if session['application']['partnershipDetails']['stayTogether'] == 'No':
        back = 'partnershipDetails.stayTogether'
    else:
        back = 'partnershipDetails.partnerAgrees'

    return render_template(
        'partnership-details/interim-check.html',
        form=form,
        back=back
    )



@partnershipDetails.route('/partnership-details/partner-died', methods=['GET', 'POST'])
@LoginRequired
def partnerDied():
    form = PartnerDiedForm()

    if form.validate_on_submit():
        session['application']['partnershipDetails']['partnerDied'] = form.partner_died.data
        session['application'] = save_progress()

        return local_redirect(url_for('partnershipDetails.endedCheck'))

    if request.method == 'GET':
        form.partner_died.data = (
            session['application']['partnershipDetails']['partnerDied']
            if 'partnerDied' in session['application']['partnershipDetails']
            else None
        )

    return render_template(
        'partnership-details/partner-died.html',
        form=form
    )


@partnershipDetails.route('/partnership-details/ended-check', methods=['GET', 'POST'])
@LoginRequired
def endedCheck():
    form = PreviousPartnershipEndedForm()

    if form.validate_on_submit():
        session['application']['partnershipDetails']['endedCheck'] = form.previous_partnership_ended.data
        session['application']['partnershipDetails']['progress'] = ListStatus.IN_REVIEW.name
        session['application'] = save_progress()

        return local_redirect(url_for('partnershipDetails.checkYourAnswers'))

    if request.method == 'GET':
        form.previous_partnership_ended.data = (
            session['application']['partnershipDetails']['endedCheck']
            if 'endedCheck' in session['application']['partnershipDetails']
            else None
        )

    return render_template(
        'partnership-details/ended-check.html',
        form=form
    )


@partnershipDetails.route('/partnership-details/check-your-answers', methods=['GET', 'POST'])
@LoginRequired
def checkYourAnswers():
    form = CheckYourAnswers()

    if 'partnershipDetails' not in session['application'] or (session['application']['partnershipDetails']['progress'] != ListStatus.IN_REVIEW.name and session['application']['partnershipDetails']['progress'] != ListStatus.COMPLETED.name):
        return local_redirect(url_for('taskList.index'))

    if request.method == 'POST':
        session['application']['partnershipDetails']['progress'] = ListStatus.COMPLETED.name
        session['application'] = save_progress()

        return local_redirect(url_for('taskList.index'))

    session['application']['partnershipDetails']['progress'] = ListStatus.IN_REVIEW.name
    session['application'] = save_progress()

    return render_template(
        'partnership-details/check-your-answers.html',
        form=form
    )
