from flask import Blueprint, render_template, request, url_for
from grc.business_logic.data_store import DataStore
from grc.business_logic.data_structures.partnership_details_data import CurrentlyInAPartnershipEnum
from grc.list_status import ListStatus
from grc.partnership_details.forms import MarriageCivilPartnershipForm, StayTogetherForm, PartnerAgreesForm, PartnerDiedForm, PreviousPartnershipEndedForm, InterimCheckForm, CheckYourAnswers
from grc.utils.decorators import LoginRequired
from grc.utils.redirect import local_redirect
from grc.utils.strtobool import strtobool

partnershipDetails = Blueprint('partnershipDetails', __name__)


@partnershipDetails.route('/partnership-details', methods=['GET', 'POST'])
@LoginRequired
def index():
    form = MarriageCivilPartnershipForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.partnership_details_data.currently_in_a_partnership = \
            CurrentlyInAPartnershipEnum[form.currently_married.data]

        if application_data.partnership_details_data.is_currently_in_partnership:
            application_data.partnership_details_data.previous_partnership_partner_died = None
            application_data.partnership_details_data.previous_partnership_ended = None
        else:
            application_data.partnership_details_data.plan_to_remain_in_a_partnership = None
            application_data.partnership_details_data.partner_agrees = None
            application_data.partnership_details_data.confirm_understood_interim_certificate = None

        DataStore.save_application(application_data)

        if application_data.partnership_details_data.currently_in_a_partnership == CurrentlyInAPartnershipEnum.NEITHER:
            return local_redirect(url_for('partnershipDetails.partnerDied'))
        else:
            return local_redirect(url_for('partnershipDetails.stayTogether'))

    if request.method == 'GET':
        form.currently_married.data = (
            application_data.partnership_details_data.currently_in_a_partnership.name
            if application_data.partnership_details_data.currently_in_a_partnership is not None else None)

    return render_template(
        'partnership-details/current-check.html',
        form=form
    )


@partnershipDetails.route('/partnership-details/stay-together', methods=['GET', 'POST'])
@LoginRequired
def stayTogether():
    form = StayTogetherForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.partnership_details_data.plan_to_remain_in_a_partnership = strtobool(form.stay_together.data)

        if not application_data.partnership_details_data.plan_to_remain_in_a_partnership:
            application_data.partnership_details_data.partner_agrees = None

        DataStore.save_application(application_data)

        if application_data.partnership_details_data.plan_to_remain_in_a_partnership:
            return local_redirect(url_for('partnershipDetails.partnerAgrees'))
        else:
            return local_redirect(url_for('partnershipDetails.interimCheck'))

    if request.method == 'GET':
        form.stay_together.data = application_data.partnership_details_data.plan_to_remain_in_a_partnership

    return render_template(
        'partnership-details/stay-together.html',
        form=form,
        application_data=application_data
    )


@partnershipDetails.route('/partnership-details/partner-agrees', methods=['GET', 'POST'])
@LoginRequired
def partnerAgrees():
    form = PartnerAgreesForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.partnership_details_data.partner_agrees = strtobool(form.partner_agrees.data)

        if application_data.partnership_details_data.partner_agrees:
            application_data.partnership_details_data.confirm_understood_interim_certificate = None

        DataStore.save_application(application_data)

        if application_data.partnership_details_data.partner_agrees:
            return local_redirect(url_for('partnershipDetails.checkYourAnswers'))
        else:
            return local_redirect(url_for('partnershipDetails.interimCheck'))

    if request.method == 'GET':
        form.partner_agrees.data = application_data.partnership_details_data.partner_agrees

    return render_template(
        'partnership-details/partner-agrees.html',
        form=form,
        application_data=application_data
    )


@partnershipDetails.route('/partnership-details/interim-check', methods=['GET', 'POST'])
@LoginRequired
def interimCheck():
    form = InterimCheckForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if request.method == 'POST':
        application_data.partnership_details_data.confirm_understood_interim_certificate = True
        DataStore.save_application(application_data)

        return local_redirect(url_for('partnershipDetails.checkYourAnswers'))

    if application_data.partnership_details_data.plan_to_remain_in_a_partnership:
        back = 'partnershipDetails.partnerAgrees'
    else:
        back = 'partnershipDetails.stayTogether'

    return render_template(
        'partnership-details/interim-check.html',
        form=form,
        back=back,
        application_data=application_data
    )



@partnershipDetails.route('/partnership-details/partner-died', methods=['GET', 'POST'])
@LoginRequired
def partnerDied():
    form = PartnerDiedForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.partnership_details_data.previous_partnership_partner_died = strtobool(form.partner_died.data)
        DataStore.save_application(application_data)

        return local_redirect(url_for('partnershipDetails.endedCheck'))

    if request.method == 'GET':
        form.partner_died.data = application_data.partnership_details_data.previous_partnership_partner_died

    return render_template(
        'partnership-details/partner-died.html',
        form=form
    )


@partnershipDetails.route('/partnership-details/ended-check', methods=['GET', 'POST'])
@LoginRequired
def endedCheck():
    form = PreviousPartnershipEndedForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.partnership_details_data.previous_partnership_ended = strtobool(form.previous_partnership_ended.data)
        DataStore.save_application(application_data)

        return local_redirect(url_for('partnershipDetails.checkYourAnswers'))

    if request.method == 'GET':
        form.previous_partnership_ended.data = application_data.partnership_details_data.previous_partnership_ended

    return render_template(
        'partnership-details/ended-check.html',
        form=form
    )


@partnershipDetails.route('/partnership-details/check-your-answers', methods=['GET', 'POST'])
@LoginRequired
def checkYourAnswers():
    form = CheckYourAnswers()
    application_data = DataStore.load_application_by_session_reference_number()

    if application_data.partnership_details_data.section_status != ListStatus.COMPLETED:
        return local_redirect(url_for('taskList.index'))

    if request.method == 'POST':
        return local_redirect(url_for('taskList.index'))

    return render_template(
        'partnership-details/check-your-answers.html',
        form=form,
        application_data=application_data
    )
