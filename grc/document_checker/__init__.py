from flask import Blueprint, flash, render_template, request, url_for
from grc.document_checker.doc_checker_data_store import DocCheckerDataStore
from grc.document_checker.doc_checker_state import DocCheckerState, CurrentlyInAPartnershipEnum
from grc.document_checker.forms import PreviousNamesCheck, MarriageCivilPartnershipForm, PlanToRemainInAPartnershipForm, \
    PartnerDiedForm, PreviousPartnershipEndedForm, GenderRecognitionOutsideUKForm, EmailForm
from grc.external_services.gov_uk_notify import GovUkNotify
from grc.utils.strtobool import strtobool
from grc.utils.redirect import local_redirect

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

        return local_redirect(url_for('documentChecker.currentlyInAPartnership'))

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

        if doc_checker_state.is_currently_in_partnership:
            next_step = 'documentChecker.planToRemainInAPartnership'
        else:
            next_step = 'documentChecker.previousPartnershipPartnerDied'

        return local_redirect(url_for(next_step))

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


@documentChecker.route('/check-documents/plan-to-remain-in-a-partnership', methods=['GET', 'POST'])
def planToRemainInAPartnership():
    form = PlanToRemainInAPartnershipForm()
    doc_checker_state = DocCheckerDataStore.load_doc_checker_state()

    if form.validate_on_submit():
        doc_checker_state.plan_to_remain_in_a_partnership = strtobool(form.plan_to_remain_in_a_partnership.data)
        DocCheckerDataStore.save_doc_checker_state(doc_checker_state)

        return local_redirect(url_for('documentChecker.genderRecognitionOutsideUK'))

    if request.method == 'GET':
        form.plan_to_remain_in_a_partnership.data = doc_checker_state.plan_to_remain_in_a_partnership

    return render_template(
        'document-checker/plan-to-remain-in-a-partnership.html',
        form=form,
        doc_checker_state=doc_checker_state
    )


@documentChecker.route('/check-documents/previous-partnership-partner-died', methods=['GET', 'POST'])
def previousPartnershipPartnerDied():
    form = PartnerDiedForm()
    doc_checker_state = DocCheckerDataStore.load_doc_checker_state()

    if form.validate_on_submit():
        doc_checker_state.previous_partnership_partner_died = strtobool(form.previous_partnership_partner_died.data)
        DocCheckerDataStore.save_doc_checker_state(doc_checker_state)

        return local_redirect(url_for('documentChecker.previousPartnershipEnded'))

    if request.method == 'GET':
        form.previous_partnership_partner_died.data = doc_checker_state.previous_partnership_partner_died

    return render_template(
        'document-checker/partner-died.html',
        form=form
    )


@documentChecker.route('/check-documents/previous-partnership-ended', methods=['GET', 'POST'])
def previousPartnershipEnded():
    form = PreviousPartnershipEndedForm()
    doc_checker_state = DocCheckerDataStore.load_doc_checker_state()

    if form.validate_on_submit():
        doc_checker_state.previous_partnership_ended = strtobool(form.previous_partnership_ended.data)
        DocCheckerDataStore.save_doc_checker_state(doc_checker_state)

        return local_redirect(url_for('documentChecker.genderRecognitionOutsideUK'))

    if request.method == 'GET':
        form.previous_partnership_ended.data = doc_checker_state.previous_partnership_ended

    return render_template(
        'document-checker/previous-partnership-ended.html',
        form=form
    )


@documentChecker.route('/check-documents/gender-recognition-outside-uk', methods=['GET', 'POST'])
def genderRecognitionOutsideUK():
    form = GenderRecognitionOutsideUKForm()
    doc_checker_state = DocCheckerDataStore.load_doc_checker_state()

    if form.validate_on_submit():
        doc_checker_state.gender_recognition_outside_uk = strtobool(form.gender_recognition_outside_uk.data)
        DocCheckerDataStore.save_doc_checker_state(doc_checker_state)

        return local_redirect(url_for('documentChecker.your_documents'))

    if request.method == 'GET':
        form.gender_recognition_outside_uk.data = doc_checker_state.gender_recognition_outside_uk

    return render_template(
        'document-checker/gender-recognition-outside-uk.html',
        form=form,
        doc_checker_state=doc_checker_state
    )


@documentChecker.route('/check-documents/your-documents', methods=['GET', 'POST'])
def your_documents():
    doc_checker_state = DocCheckerDataStore.load_doc_checker_state()

    if not hasUserAnswersAllTheQuestions():
        return local_redirect(getUrlForNextUnansweredQuestion())

    return render_template(
        'document-checker/your-documents.html',
        doc_checker_state=doc_checker_state
    )


@documentChecker.route('/check-documents/email-address', methods=['GET', 'POST'])
def askForEmailAddress():
    if not hasUserAnswersAllTheQuestions():
        return local_redirect(getUrlForNextUnansweredQuestion())

    doc_checker_state = DocCheckerDataStore.load_doc_checker_state()
    form = EmailForm()

    if form.validate_on_submit():
        try:
            GovUkNotify().send_email_documents_you_need_for_your_grc_application(
                email_address=
                    form.email_address.data,
                need_to_send_name_change_documents=
                    doc_checker_state.need_to_send_name_change_documents,
                need_to_send_medical_reports=
                    doc_checker_state.need_to_send_medical_reports,
                need_to_send_evidence_of_living_in_gender=
                    doc_checker_state.need_to_send_evidence_of_living_in_gender,
                need_to_send_statutory_declaration_for_single_applicant=
                    doc_checker_state.need_to_send_statutory_declaration_for_single_applicant,
                need_to_send_statutory_declaration_for_married_applicant=
                    doc_checker_state.need_to_send_statutory_declaration_for_applicant_in_partnership and
                    doc_checker_state.is_married,
                need_to_send_statutory_declaration_for_applicant_in_civil_partnership=
                    doc_checker_state.need_to_send_statutory_declaration_for_applicant_in_partnership and
                    doc_checker_state.is_in_civil_partnership,
                need_to_send_spouses_statutory_declaration=
                    doc_checker_state.need_to_send_partners_statutory_declaration and
                    doc_checker_state.is_married,
                need_to_send_civil_partners_statutory_declaration=
                    doc_checker_state.need_to_send_partners_statutory_declaration and
                    doc_checker_state.is_in_civil_partnership,
                need_to_send_marriage_certificate=
                    doc_checker_state.need_to_send_partnership_certificate and
                    doc_checker_state.is_married,
                need_to_send_civil_partnership_certificate=
                    doc_checker_state.need_to_send_partnership_certificate and
                    doc_checker_state.is_in_civil_partnership,
                need_to_send_death_certificate=
                    doc_checker_state.need_to_send_death_certificate,
                need_to_send_decree_absolute=
                    doc_checker_state.need_to_send_decree_absolute,
                need_to_send_proof_gender_recognised_outside_uk=
                    doc_checker_state.need_to_send_proof_gender_recognised_outside_uk
            )

            return local_redirect(url_for('documentChecker.emailSent'))
        except BaseException as err:
            error = err.args[0].json()
            flash(error['errors'][0]['message'], 'error')

    return render_template(
        'document-checker/email-address.html',
        form=form
    )


@documentChecker.route('/check-documents/email-sent', methods=['GET'])
def emailSent():
    return render_template('document-checker/email-sent.html')


def hasUserAnswersAllTheQuestions() -> bool:
    doc_checker_state = DocCheckerDataStore.load_doc_checker_state()

    if doc_checker_state.changed_name_to_reflect_gender is None: return False
    if doc_checker_state.currently_in_a_partnership is None: return False
    if doc_checker_state.is_currently_in_partnership and doc_checker_state.plan_to_remain_in_a_partnership is None: return False
    if doc_checker_state.is_not_in_partnership and doc_checker_state.previous_partnership_partner_died is None: return False
    if doc_checker_state.is_not_in_partnership and doc_checker_state.previous_partnership_ended is None: return False
    if doc_checker_state.gender_recognition_outside_uk is None: return False
    return True


def getUrlForNextUnansweredQuestion() -> str:
    doc_checker_state = DocCheckerDataStore.load_doc_checker_state()

    if doc_checker_state.changed_name_to_reflect_gender is None: return url_for('documentChecker.previousNamesCheck')
    if doc_checker_state.currently_in_a_partnership is None: return url_for('documentChecker.currentlyInAPartnership')
    if doc_checker_state.is_currently_in_partnership and doc_checker_state.plan_to_remain_in_a_partnership is None: return url_for(
        'documentChecker.planToRemainInAPartnership')
    if doc_checker_state.is_not_in_partnership and doc_checker_state.previous_partnership_partner_died is None: return url_for(
        'documentChecker.previousPartnershipPartnerDied')
    if doc_checker_state.is_not_in_partnership and doc_checker_state.previous_partnership_ended is None: return url_for(
        'documentChecker.previousPartnershipEnded')
    if doc_checker_state.gender_recognition_outside_uk is None: return url_for(
        'documentChecker.genderRecognitionOutsideUK')
    return url_for('documentChecker.your_documents')
