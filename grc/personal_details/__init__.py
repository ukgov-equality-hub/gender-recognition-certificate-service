import datetime
from flask import Blueprint, render_template, request, url_for
from grc.business_logic.data_store import DataStore
from grc.business_logic.data_structures.personal_details_data import AffirmedGender
from grc.list_status import ListStatus
from grc.personal_details.forms import NameForm, AffirmedGenderForm, TransitionDateForm, StatutoryDeclarationDateForm, PreviousNamesCheck, AddressForm, ContactPreferencesForm, ContactDatesForm, HmrcForm, CheckYourAnswers
from grc.utils.decorators import LoginRequired
from grc.utils.redirect import local_redirect
from grc.utils.strtobool import strtobool

personalDetails = Blueprint('personalDetails', __name__)


@personalDetails.route('/personal-details', methods=['GET', 'POST'])
@LoginRequired
def index():
    form = NameForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.personal_details_data.title = form.title.data
        application_data.personal_details_data.first_names = form.first_name.data
        application_data.personal_details_data.last_name = form.last_name.data
        DataStore.save_application(application_data)

        next_page = ('personalDetails.checkYourAnswers'
                     if application_data.personal_details_data.section_status == ListStatus.COMPLETED
                     else 'personalDetails.affirmedGender')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.title.data = application_data.personal_details_data.title
        form.first_name.data = application_data.personal_details_data.first_names
        form.last_name.data = application_data.personal_details_data.last_name

    return render_template(
        'personal-details/name.html',
        form=form
    )


@personalDetails.route('/personal-details/affirmed-gender', methods=['GET', 'POST'])
@LoginRequired
def affirmedGender():
    form = AffirmedGenderForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.personal_details_data.affirmed_gender = AffirmedGender[form.affirmedGender.data]
        DataStore.save_application(application_data)

        next_page = ('personalDetails.checkYourAnswers'
                     if application_data.personal_details_data.section_status == ListStatus.COMPLETED
                     else 'personalDetails.transitionDate')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.affirmedGender.data = (
            application_data.personal_details_data.affirmed_gender.name
            if application_data.personal_details_data.affirmed_gender is not None else None)

    return render_template(
        'personal-details/affirmed-gender.html',
        form=form
    )


@personalDetails.route('/personal-details/transition-date', methods=['GET', 'POST'])
@LoginRequired
def transitionDate():
    form = TransitionDateForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.personal_details_data.transition_date = datetime.date(
            int(form.transition_date_year.data),
            int(form.transition_date_month.data),
            1)
        DataStore.save_application(application_data)

        next_page = ('personalDetails.checkYourAnswers'
                     if application_data.personal_details_data.section_status == ListStatus.COMPLETED
                     else 'personalDetails.statutoryDeclarationDate')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        if application_data.personal_details_data.transition_date is not None:
            form.transition_date_month.data = application_data.personal_details_data.transition_date.month
            form.transition_date_year.data = application_data.personal_details_data.transition_date.year

    return render_template(
        'personal-details/transition-date.html',
        form=form
    )


@personalDetails.route('/personal-details/statutory-declaration-date', methods=['GET', 'POST'])
@LoginRequired
def statutoryDeclarationDate():
    form = StatutoryDeclarationDateForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.personal_details_data.statutory_declaration_date = datetime.date(
            int(form.statutory_declaration_date_year.data),
            int(form.statutory_declaration_date_month.data),
            int(form.statutory_declaration_date_day.data))
        DataStore.save_application(application_data)

        next_page = ('personalDetails.checkYourAnswers'
                     if application_data.personal_details_data.section_status == ListStatus.COMPLETED
                     else 'personalDetails.previousNamesCheck')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        if application_data.personal_details_data.statutory_declaration_date is not None:
            form.statutory_declaration_date_day.data = application_data.personal_details_data.statutory_declaration_date.day
            form.statutory_declaration_date_month.data = application_data.personal_details_data.statutory_declaration_date.month
            form.statutory_declaration_date_year.data = application_data.personal_details_data.statutory_declaration_date.year

    return render_template(
        'personal-details/statutory-declaration-date.html',
        form=form
    )


@personalDetails.route('/personal-details/previous-names-check', methods=['GET', 'POST'])
@LoginRequired
def previousNamesCheck():
    form = PreviousNamesCheck()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.personal_details_data.changed_name_to_reflect_gender = strtobool(form.previousNameCheck.data)
        DataStore.save_application(application_data)

        next_page = ('personalDetails.checkYourAnswers'
                     if application_data.personal_details_data.section_status == ListStatus.COMPLETED
                     else 'personalDetails.address')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.previousNameCheck.data = application_data.personal_details_data.changed_name_to_reflect_gender

    return render_template(
        'personal-details/previous-names-check.html',
        form=form
    )


@personalDetails.route('/personal-details/address', methods=['GET', 'POST'])
@LoginRequired
def address():
    form = AddressForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.personal_details_data.address_line_one = form.address_line_one.data
        application_data.personal_details_data.address_line_two = form.address_line_two.data
        application_data.personal_details_data.address_town_city = form.town.data
        application_data.personal_details_data.address_postcode = form.postcode.data
        DataStore.save_application(application_data)

        next_page = ('personalDetails.checkYourAnswers'
                     if application_data.personal_details_data.section_status == ListStatus.COMPLETED
                     else 'personalDetails.contactDates')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.address_line_one.data = application_data.personal_details_data.address_line_one
        form.address_line_two.data = application_data.personal_details_data.address_line_two
        form.town.data = application_data.personal_details_data.address_town_city
        form.postcode.data = application_data.personal_details_data.address_postcode

    return render_template(
        'personal-details/address.html',
        form=form
    )


@personalDetails.route('/personal-details/contact-preferences', methods=['GET', 'POST'])
@LoginRequired
def contactPreferences():
    form = ContactPreferencesForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if request.method == 'POST':
        if 'EMAIL' not in form.contact_options.data:
            form.email.data = None
        if 'PHONE' not in form.contact_options.data:
            form.phone.data = None

        if form.validate_on_submit():
            application_data.personal_details_data.contact_email_address = \
                form.email.data if 'EMAIL' in form.contact_options.data else ''
            application_data.personal_details_data.contact_phone_number = \
                form.phone.data if 'PHONE' in form.contact_options.data else ''
            application_data.personal_details_data.contact_by_post = ('POST' in form.contact_options.data)
            DataStore.save_application(application_data)

            next_page = ('personalDetails.checkYourAnswers'
                         if application_data.personal_details_data.section_status == ListStatus.COMPLETED
                         else 'personalDetails.hmrc')

            return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.contact_options.data = []
        if application_data.personal_details_data.contact_email_address:
            form.contact_options.data.append('EMAIL')
        if application_data.personal_details_data.contact_phone_number:
            form.contact_options.data.append('PHONE')
        if application_data.personal_details_data.contact_by_post:
            form.contact_options.data.append('POST')

        form.email.data = application_data.personal_details_data.contact_email_address
        form.phone.data = application_data.personal_details_data.contact_phone_number

    return render_template(
        'personal-details/contact-preferences.html',
        form=form,
        address=application_data.personal_details_data.address_comma_separated
    )


@personalDetails.route('/personal-details/contact-dates', methods=['GET', 'POST'])
@LoginRequired
def contactDates():
    form = ContactDatesForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.personal_details_data.contact_dates_should_avoid = strtobool(form.contactDatesCheck.data)
        application_data.personal_details_data.contact_dates_to_avoid = \
            form.dates.data if application_data.personal_details_data.contact_dates_should_avoid else None
        DataStore.save_application(application_data)

        next_page = ('personalDetails.checkYourAnswers'
                     if application_data.personal_details_data.section_status == ListStatus.COMPLETED
                     else 'personalDetails.contactPreferences')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.contactDatesCheck.data = application_data.personal_details_data.contact_dates_should_avoid
        form.dates.data = application_data.personal_details_data.contact_dates_to_avoid

    return render_template(
        'personal-details/contact-dates.html',
        form=form
    )


@personalDetails.route('/personal-details/hmrc', methods=['GET', 'POST'])
@LoginRequired
def hmrc():
    form = HmrcForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.personal_details_data.tell_hmrc = strtobool(form.tell_hmrc.data)
        application_data.personal_details_data.national_insurance_number = \
            form.national_insurance_number.data if application_data.personal_details_data.tell_hmrc else None
        DataStore.save_application(application_data)

        return local_redirect(url_for('personalDetails.checkYourAnswers'))

    if request.method == 'GET':
        form.tell_hmrc.data = application_data.personal_details_data.tell_hmrc
        form.national_insurance_number.data = application_data.personal_details_data.national_insurance_number

    return render_template(
        'personal-details/hmrc.html',
        form=form
    )


@personalDetails.route('/personal-details/check-your-answers', methods=['GET', 'POST'])
@LoginRequired
def checkYourAnswers():
    form = CheckYourAnswers()
    application_data = DataStore.load_application_by_session_reference_number()

    if application_data.personal_details_data.section_status != ListStatus.COMPLETED:
        return local_redirect(url_for('taskList.index'))

    if request.method == 'POST':
        return local_redirect(url_for('taskList.index'))

    return render_template(
        'personal-details/check-your-answers.html',
        form=form,
        application_data=application_data
    )
