import datetime
from flask import Blueprint, render_template, request, url_for
from grc.business_logic.data_store import DataStore
from grc.business_logic.data_structures.application_data import ApplicationData
from grc.business_logic.data_structures.personal_details_data import AffirmedGender, ContactDatesAvoid
from grc.list_status import ListStatus
from grc.personal_details.forms import NameForm, DateRangeForm, AffirmedGenderForm, TransitionDateForm, StatutoryDeclarationDateForm, PreviousNamesCheck, AddressForm, ContactPreferencesForm, ContactDatesForm, HmrcForm, CheckYourAnswers
from grc.utils.decorators import LoginRequired
from grc.utils.get_next_page import get_next_page_global, get_previous_page_global
from grc.utils.redirect import local_redirect
from grc.utils.strtobool import strtobool
from grc.business_logic.data_structures.personal_details_data import DateRange
from grc.utils.flask_child_form_add_custom_errors import add_multiple_errors_for_child_form
from grc.utils.form_custom_validators import validate_date_range_form, validate_date_ranges


personalDetails = Blueprint('personalDetails', __name__)


@personalDetails.route('/personal-details', methods=['GET', 'POST'])
@LoginRequired
def index():
    form = NameForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.personal_details_data.title = form.title.data
        application_data.personal_details_data.first_name = form.first_name.data
        application_data.personal_details_data.middle_names = form.middle_names.data
        application_data.personal_details_data.last_name = form.last_name.data
        DataStore.save_application(application_data)

        return get_next_page(application_data, 'personalDetails.affirmedGender')

    if request.method == 'GET':
        form.title.data = application_data.personal_details_data.title
        form.first_name.data = application_data.personal_details_data.first_name
        form.middle_names.data = application_data.personal_details_data.middle_names
        form.last_name.data = application_data.personal_details_data.last_name

    return render_template(
        'personal-details/name.html',
        form=form,
        back=get_previous_page(application_data, 'taskList.index')
    )


@personalDetails.route('/personal-details/affirmed-gender', methods=['GET', 'POST'])
@LoginRequired
def affirmedGender():
    form = AffirmedGenderForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.personal_details_data.affirmed_gender = AffirmedGender[form.affirmedGender.data]
        DataStore.save_application(application_data)

        return get_next_page(application_data, 'personalDetails.transitionDate')

    if request.method == 'GET':
        form.affirmedGender.data = (
            application_data.personal_details_data.affirmed_gender.name
            if application_data.personal_details_data.affirmed_gender is not None else None)

    return render_template(
        'personal-details/affirmed-gender.html',
        form=form,
        back=get_previous_page(application_data, 'personalDetails.index')
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

        return get_next_page(application_data, 'personalDetails.statutoryDeclarationDate')

    if request.method == 'GET':
        if application_data.personal_details_data.transition_date is not None:
            form.transition_date_month.data = application_data.personal_details_data.transition_date.month
            form.transition_date_year.data = application_data.personal_details_data.transition_date.year

    return render_template(
        'personal-details/transition-date.html',
        form=form,
        back=get_previous_page(application_data, 'personalDetails.affirmedGender')
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

        return get_next_page(application_data, 'personalDetails.previousNamesCheck')

    if request.method == 'GET':
        if application_data.personal_details_data.statutory_declaration_date is not None:
            form.statutory_declaration_date_day.data = application_data.personal_details_data.statutory_declaration_date.day
            form.statutory_declaration_date_month.data = application_data.personal_details_data.statutory_declaration_date.month
            form.statutory_declaration_date_year.data = application_data.personal_details_data.statutory_declaration_date.year

    return render_template(
        'personal-details/statutory-declaration-date.html',
        form=form,
        back=get_previous_page(application_data, 'personalDetails.transitionDate')
    )


@personalDetails.route('/personal-details/previous-names-check', methods=['GET', 'POST'])
@LoginRequired
def previousNamesCheck():
    form = PreviousNamesCheck()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.personal_details_data.changed_name_to_reflect_gender = strtobool(form.previousNameCheck.data)
        DataStore.save_application(application_data)

        return get_next_page(application_data, 'personalDetails.address')

    if request.method == 'GET':
        form.previousNameCheck.data = application_data.personal_details_data.changed_name_to_reflect_gender

    return render_template(
        'personal-details/previous-names-check.html',
        form=form,
        back=get_previous_page(application_data, 'personalDetails.statutoryDeclarationDate')
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
        application_data.personal_details_data.address_country = form.country.data
        application_data.personal_details_data.address_postcode = form.postcode.data
        DataStore.save_application(application_data)

        return get_next_page(application_data, 'personalDetails.contactDates')

    if request.method == 'GET':
        form.address_line_one.data = application_data.personal_details_data.address_line_one
        form.address_line_two.data = application_data.personal_details_data.address_line_two
        form.town.data = application_data.personal_details_data.address_town_city
        form.country.data = application_data.personal_details_data.address_country
        form.postcode.data = application_data.personal_details_data.address_postcode

    return render_template(
        'personal-details/address.html',
        form=form,
        back=get_previous_page(application_data, 'personalDetails.previousNamesCheck'),
        countries=[{ 'Value': Value, 'Option': Option } for Value, Option in form.country.choices]
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

            return get_next_page(application_data, 'personalDetails.hmrc')

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
        address=application_data.personal_details_data.address_comma_separated,
        back=get_previous_page(application_data, 'personalDetails.contactDates')
    )


@personalDetails.route('/personal-details/contact-dates', methods=['GET', 'POST'])
@LoginRequired
def contactDates():
    form = ContactDatesForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.personal_details_data.contact_dates_to_avoid_option = ContactDatesAvoid[form.contactDatesCheck.data]
        new_date_range_requested = True if form.add_date_range_button_clicked.data else False
        remove_date_range_requested = True if form.remove_date_range_button_clicked.data else False

        if form.contactDatesCheck.data == ContactDatesAvoid.NO_DATES.value:
            application_data.personal_details_data.contact_date_to_avoid = None
            application_data.personal_details_data.contact_date_ranges_to_avoid = None
            application_data.personal_details_data.remove_old_contact_dates_to_avoid_data()
            DataStore.save_application(application_data)
            return get_next_page(application_data, 'personalDetails.contactPreferences')

        if form.contactDatesCheck.data == ContactDatesAvoid.SINGLE_DATE.value:
            if form.day.data and form.month.data and form.year.data:
                application_data.personal_details_data.contact_date_to_avoid = datetime.date(
                    int(form.year.data),
                    int(form.month.data),
                    int(form.day.data))

            application_data.personal_details_data.contact_date_ranges_to_avoid = None
            application_data.personal_details_data.remove_old_contact_dates_to_avoid_data()
            DataStore.save_application(application_data)
            return get_next_page(application_data, 'personalDetails.contactPreferences')

        if form.contactDatesCheck.data == ContactDatesAvoid.DATE_RANGE.value and remove_date_range_requested:
            form.date_ranges.pop_entry()

        elif form.contactDatesCheck.data == ContactDatesAvoid.DATE_RANGE.value:
            date_range_results = []
            date_range_errors = dict()

            for i, date_range_form in enumerate(form.date_ranges):
                date_range_errors[i] = validate_date_range_form(date_range_form)

                if not date_range_errors[i]:
                    date_range_result = DateRange()
                    try:
                        date_range_result.index = i
                        date_range_result.from_date = datetime.date(
                            int(date_range_form.from_date_year.data),
                            int(date_range_form.from_date_month.data),
                            int(date_range_form.from_date_day.data)
                        )
                    except ValueError as err:
                        print(f'Error setting from date as datetime, message={err}', flush=True)
                        date_range_errors[i] = {'from_date_year': 'Enter a valid date'}

                    try:
                        date_range_result.to_date = datetime.date(
                            int(date_range_form.to_date_year.data),
                            int(date_range_form.to_date_month.data),
                            int(date_range_form.to_date_day.data)
                        )
                    except ValueError as err:
                        print(f'Error setting to date as datetime, message={err}', flush=True)
                        date_range_errors[i] = {'to_date_year': 'Enter a valid date'}

                    if not date_range_errors[i]:
                        date_range_errors[i] = validate_date_ranges(date_range_result.from_date,
                                                                    date_range_result.to_date)

                    if not date_range_errors[i]:
                        date_range_results.append(date_range_result)

                if date_range_errors[i]:
                    add_multiple_errors_for_child_form(form.date_ranges, date_range_form, date_range_errors[i])

            date_range_errors = tuple(error for i, error in date_range_errors.items() if error)

            if not date_range_errors and new_date_range_requested:
                empty_date_range_form = DateRangeForm()
                empty_date_range_form.from_date_day = ''
                empty_date_range_form.from_date_month = ''
                empty_date_range_form.from_date_year = ''
                empty_date_range_form.to_date_day = ''
                empty_date_range_form.to_date_month = ''
                empty_date_range_form.to_date_year = ''

                form.date_ranges.append_entry(empty_date_range_form)

            application_data.personal_details_data.contact_date_ranges_to_avoid = date_range_results

            if not date_range_errors and not new_date_range_requested:
                application_data.personal_details_data.contact_date_to_avoid = None
                application_data.personal_details_data.remove_old_contact_dates_to_avoid_data()
                DataStore.save_application(application_data)
                return get_next_page(application_data, 'personalDetails.contactPreferences')

    if request.method == 'GET':

        if application_data.personal_details_data.contact_dates_to_avoid_option:
            form.contactDatesCheck.data = application_data.personal_details_data.contact_dates_to_avoid_option.name

        if application_data.personal_details_data.contact_date_to_avoid:
            form.day.data = application_data.personal_details_data.contact_date_to_avoid.day
            form.month.data = application_data.personal_details_data.contact_date_to_avoid.month
            form.year.data = application_data.personal_details_data.contact_date_to_avoid.year

        if application_data.personal_details_data.contact_date_ranges_to_avoid:
            for date_range in application_data.personal_details_data.contact_date_ranges_to_avoid:
                date_range_form = DateRangeForm()
                date_range_form.from_date_day = date_range.from_date.day
                date_range_form.from_date_month = date_range.from_date.month
                date_range_form.from_date_year = date_range.from_date.year

                date_range_form.to_date_day = date_range.to_date.day
                date_range_form.to_date_month = date_range.to_date.month
                date_range_form.to_date_year = date_range.to_date.year

                form.date_ranges.append_entry(date_range_form)

    return render_template(
        'personal-details/contact-dates.html',
        form=form,
        back=get_previous_page(application_data, 'personalDetails.address')
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

        return get_next_page(application_data, 'personalDetails.checkYourAnswers')

    if request.method == 'GET':
        form.tell_hmrc.data = application_data.personal_details_data.tell_hmrc
        form.national_insurance_number.data = application_data.personal_details_data.national_insurance_number

    return render_template(
        'personal-details/hmrc.html',
        form=form,
        back=get_previous_page(application_data, 'personalDetails.contactPreferences')
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
        application_data=application_data,
        back=get_previous_page(application_data, 'personalDetails.hmrc')
    )


def get_next_page(application_data: ApplicationData, next_page_in_journey: str):
    return get_next_page_global(
        next_page_in_journey=next_page_in_journey,
        section_check_your_answers_page='personalDetails.checkYourAnswers',
        section_status=application_data.personal_details_data.section_status,
        application_data=application_data)


def get_previous_page(application_data: ApplicationData, previous_page_in_journey: str):
    return get_previous_page_global(
        previous_page_in_journey=previous_page_in_journey,
        section_check_your_answers_page='personalDetails.checkYourAnswers',
        section_status=application_data.personal_details_data.section_status,
        application_data=application_data)
