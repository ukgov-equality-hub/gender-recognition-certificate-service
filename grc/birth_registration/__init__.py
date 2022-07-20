import datetime
from flask import Blueprint, render_template, request, url_for
from grc.business_logic.data_store import DataStore
from grc.business_logic.data_structures.application_data import ApplicationData
from grc.business_logic.data_structures.birth_registration_data import AdoptedInTheUkEnum
from grc.list_status import ListStatus
from grc.birth_registration.forms import NameForm, DobForm, UkCheckForm, CountryForm, PlaceOfBirthForm, MothersNameForm, FatherNameCheckForm, FathersNameForm, AdoptedForm, AdoptedUKForm, ForcesForm, CheckYourAnswers
from grc.utils.decorators import LoginRequired
from grc.utils.get_next_page import get_next_page_global, get_previous_page_global
from grc.utils.redirect import local_redirect
from grc.utils.strtobool import strtobool

birthRegistration = Blueprint('birthRegistration', __name__)


@birthRegistration.route('/birth-registration', methods=['GET', 'POST'])
@LoginRequired
def index():
    form = NameForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.birth_registration_data.first_name = form.first_name.data
        application_data.birth_registration_data.middle_names = form.middle_names.data
        application_data.birth_registration_data.last_name = form.last_name.data
        DataStore.save_application(application_data)

        return get_next_page(application_data, 'birthRegistration.dob')

    if request.method == 'GET':
        form.first_name.data = application_data.birth_registration_data.first_name
        form.middle_names.data = application_data.birth_registration_data.middle_names
        form.last_name.data = application_data.birth_registration_data.last_name

    return render_template(
        'birth-registration/name.html',
        form=form,
        back=get_previous_page(application_data, 'taskList.index')
    )


@birthRegistration.route('/birth-registration/dob', methods=['GET', 'POST'])
@LoginRequired
def dob():
    form = DobForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.birth_registration_data.date_of_birth = datetime.date(
            int(form.year.data),
            int(form.month.data),
            int(form.day.data))
        DataStore.save_application(application_data)

        return get_next_page(application_data, 'birthRegistration.ukCheck')

    if request.method == 'GET':
        if application_data.birth_registration_data.date_of_birth is not None:
            form.day.data = application_data.birth_registration_data.date_of_birth.day
            form.month.data = application_data.birth_registration_data.date_of_birth.month
            form.year.data = application_data.birth_registration_data.date_of_birth.year

    return render_template(
        'birth-registration/dob.html',
        form=form,
        back=get_previous_page(application_data, 'birthRegistration.index')
    )


@birthRegistration.route('/birth-registration/uk-check', methods=['GET', 'POST'])
@LoginRequired
def ukCheck():
    form = UkCheckForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.birth_registration_data.birth_registered_in_uk = strtobool(form.birth_registered_in_uk.data)

        if application_data.birth_registration_data.birth_registered_in_uk:
            application_data.birth_registration_data.country_of_birth = None
        else:
            application_data.birth_registration_data.town_city_of_birth = None
            application_data.birth_registration_data.mothers_first_name = None
            application_data.birth_registration_data.mothers_last_name = None
            application_data.birth_registration_data.mothers_maiden_name = None
            application_data.birth_registration_data.fathers_name_on_birth_certificate = None
            application_data.birth_registration_data.fathers_first_name = None
            application_data.birth_registration_data.fathers_last_name = None
            application_data.birth_registration_data.adopted = None
            application_data.birth_registration_data.adopted_in_the_uk = None
            application_data.birth_registration_data.forces_registration = None

        DataStore.save_application(application_data)

        if application_data.birth_registration_data.birth_registered_in_uk:
            next_page = 'birthRegistration.placeOfBirth'
        else:
            next_page = 'birthRegistration.country'

        return get_next_page(application_data, next_page)

    else:
        form.birth_registered_in_uk.data = application_data.birth_registration_data.birth_registered_in_uk

    return render_template(
        'birth-registration/uk-check.html',
        form=form,
        back=get_previous_page(application_data, 'birthRegistration.dob')
    )


@birthRegistration.route('/birth-registration/country', methods=['GET', 'POST'])
@LoginRequired
def country():
    form = CountryForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.birth_registration_data.country_of_birth = form.country_of_birth.data
        DataStore.save_application(application_data)

        return get_next_page(application_data, 'birthRegistration.checkYourAnswers')

    if request.method == 'GET':
        form.country_of_birth.data = application_data.birth_registration_data.country_of_birth

    return render_template(
        'birth-registration/country.html',
        form=form,
        back=get_previous_page(application_data, 'birthRegistration.ukCheck')
    )


@birthRegistration.route('/birth-registration/place-of-birth', methods=['GET', 'POST'])
@LoginRequired
def placeOfBirth():
    form = PlaceOfBirthForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.birth_registration_data.town_city_of_birth = form.place_of_birth.data
        DataStore.save_application(application_data)

        return get_next_page(application_data, 'birthRegistration.mothersName')

    if request.method == 'GET':
        form.place_of_birth.data = application_data.birth_registration_data.town_city_of_birth

    return render_template(
        'birth-registration/place-of-birth.html',
        form=form,
        back=get_previous_page(application_data, 'birthRegistration.ukCheck')
    )


@birthRegistration.route('/birth-registration/mothers-name', methods=['GET', 'POST'])
@LoginRequired
def mothersName():
    form = MothersNameForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.birth_registration_data.mothers_first_name = form.first_name.data
        application_data.birth_registration_data.mothers_last_name = form.last_name.data
        application_data.birth_registration_data.mothers_maiden_name = form.maiden_name.data
        DataStore.save_application(application_data)

        return get_next_page(application_data, 'birthRegistration.fathersNameCheck')

    if request.method == 'GET':
        form.first_name.data = application_data.birth_registration_data.mothers_first_name
        form.last_name.data = application_data.birth_registration_data.mothers_last_name
        form.maiden_name.data = application_data.birth_registration_data.mothers_maiden_name

    back_link = get_previous_page(application_data, 'birthRegistration.placeOfBirth')

    return render_template(
        'birth-registration/mothers-name.html',
        form=form,
        back=back_link
    )


@birthRegistration.route('/birth-registration/fathers-name-check', methods=['GET', 'POST'])
@LoginRequired
def fathersNameCheck():
    form = FatherNameCheckForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.birth_registration_data.fathers_name_on_birth_certificate = \
            strtobool(form.fathers_name_on_certificate.data)

        if not application_data.birth_registration_data.fathers_name_on_birth_certificate:
            application_data.birth_registration_data.fathers_first_name = None
            application_data.birth_registration_data.fathers_last_name = None

        DataStore.save_application(application_data)

        if application_data.birth_registration_data.fathers_name_on_birth_certificate:
            next_page = 'birthRegistration.fathersName'
        else:
            next_page = 'birthRegistration.adopted'

        return get_next_page(application_data, next_page)

    else:
        form.fathers_name_on_certificate.data = application_data.birth_registration_data.fathers_name_on_birth_certificate

    return render_template(
        'birth-registration/fathers-name-check.html',
        form=form,
        back=get_previous_page(application_data, 'birthRegistration.mothersName')
    )


@birthRegistration.route('/birth-registration/fathers-name', methods=['GET', 'POST'])
@LoginRequired
def fathersName():
    form = FathersNameForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.birth_registration_data.fathers_first_name = form.first_name.data
        application_data.birth_registration_data.fathers_last_name = form.last_name.data
        DataStore.save_application(application_data)

        return get_next_page(application_data, 'birthRegistration.adopted')

    if request.method == 'GET':
        form.first_name.data = application_data.birth_registration_data.fathers_first_name
        form.last_name.data = application_data.birth_registration_data.fathers_last_name

    return render_template(
        'birth-registration/fathers-name.html',
        form=form,
        back=get_previous_page(application_data, 'birthRegistration.fathersNameCheck')
    )


@birthRegistration.route('/birth-registration/adopted', methods=['GET', 'POST'])
@LoginRequired
def adopted():
    form = AdoptedForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if application_data.birth_registration_data.fathers_name_on_birth_certificate:
        back = 'birthRegistration.fathersName'
    else:
        back = 'birthRegistration.fathersNameCheck'

    if form.validate_on_submit():
        application_data.birth_registration_data.adopted = strtobool(form.adopted.data)

        if not application_data.birth_registration_data.adopted:
            application_data.birth_registration_data.adopted_in_the_uk = None

        DataStore.save_application(application_data)

        if application_data.birth_registration_data.adopted:
            next_page = 'birthRegistration.adoptedUK'
        else:
            next_page = 'birthRegistration.forces'

        return get_next_page(application_data, next_page)

    if request.method == 'GET':
        form.adopted.data = application_data.birth_registration_data.adopted

    return render_template(
        'birth-registration/adopted.html',
        form=form,
        back=get_previous_page(application_data, back)
    )


@birthRegistration.route('/birth-registration/adopted-uk', methods=['GET', 'POST'])
@LoginRequired
def adoptedUK():
    form = AdoptedUKForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.birth_registration_data.adopted_in_the_uk = AdoptedInTheUkEnum[form.adopted_uk.data]
        DataStore.save_application(application_data)

        next_page = ('birthRegistration.checkYourAnswers'
                     if application_data.birth_registration_data.section_status == ListStatus.COMPLETED
                     else 'birthRegistration.forces')

        return get_next_page(application_data, next_page)

    if request.method == 'GET':
        form.adopted_uk.data = (
            application_data.birth_registration_data.adopted_in_the_uk.name
            if application_data.birth_registration_data.adopted_in_the_uk is not None else None)

    return render_template(
        'birth-registration/adopted-uk.html',
        form=form,
        back=get_previous_page(application_data, 'birthRegistration.adopted')
    )


@birthRegistration.route('/birth-registration/forces', methods=['GET', 'POST'])
@LoginRequired
def forces():
    form = ForcesForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.birth_registration_data.forces_registration = strtobool(form.forces.data)
        DataStore.save_application(application_data)

        return get_next_page(application_data, 'birthRegistration.checkYourAnswers')

    if request.method == 'GET':
        form.forces.data = application_data.birth_registration_data.forces_registration

    back_link = ('birthRegistration.adoptedUK'
                 if application_data.birth_registration_data.adopted
                 else 'birthRegistration.adopted')

    return render_template(
        'birth-registration/forces.html',
        form=form,
        application_data=application_data,
        back=get_previous_page(application_data, back_link)
    )


@birthRegistration.route('/birth-registration/check-your-answers', methods=['GET', 'POST'])
@LoginRequired
def checkYourAnswers():
    form = CheckYourAnswers()
    application_data = DataStore.load_application_by_session_reference_number()

    if application_data.birth_registration_data.section_status != ListStatus.COMPLETED:
        return local_redirect(url_for('taskList.index'))

    if request.method == 'POST':
        return local_redirect(url_for('taskList.index'))

    back_link = ('birthRegistration.forces'
                 if application_data.birth_registration_data.birth_registered_in_uk
                 else 'birthRegistration.country')

    return render_template(
        'birth-registration/check-your-answers.html',
        form=form,
        application_data=application_data,
        back=get_previous_page(application_data, back_link)
    )


def get_next_page(application_data: ApplicationData, next_page_in_journey: str):
    return get_next_page_global(
        next_page_in_journey=next_page_in_journey,
        section_check_your_answers_page='birthRegistration.checkYourAnswers',
        section_status=application_data.birth_registration_data.section_status,
        application_data=application_data)


def get_previous_page(application_data: ApplicationData, previous_page_in_journey: str):
    return get_previous_page_global(
        previous_page_in_journey=previous_page_in_journey,
        section_check_your_answers_page='birthRegistration.checkYourAnswers',
        section_status=application_data.birth_registration_data.section_status,
        application_data=application_data)
