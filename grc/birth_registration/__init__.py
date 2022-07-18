import datetime
from flask import Blueprint, render_template, request, url_for
from grc.business_logic.data_store import DataStore
from grc.business_logic.data_structures.birth_registration_data import AdoptedInTheUkEnum
from grc.list_status import ListStatus
from grc.birth_registration.forms import NameForm, DobForm, UkCheckForm, CountryForm, PlaceOfBirthForm, MothersNameForm, FatherNameCheckForm, FathersNameForm, AdoptedForm, AdoptedUKForm, ForcesForm, CheckYourAnswers
from grc.utils.decorators import LoginRequired
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

        next_page = ('birthRegistration.checkYourAnswers'
                     if application_data.birth_registration_data.section_status == ListStatus.COMPLETED
                     else 'birthRegistration.dob')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.first_name.data = application_data.birth_registration_data.first_name
        form.middle_names.data = application_data.birth_registration_data.middle_names
        form.last_name.data = application_data.birth_registration_data.last_name

    return render_template(
        'birth-registration/name.html',
        form=form
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

        next_page = ('birthRegistration.checkYourAnswers'
                     if application_data.birth_registration_data.section_status == ListStatus.COMPLETED
                     else 'birthRegistration.ukCheck')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        if application_data.birth_registration_data.date_of_birth is not None:
            form.day.data = application_data.birth_registration_data.date_of_birth.day
            form.month.data = application_data.birth_registration_data.date_of_birth.month
            form.year.data = application_data.birth_registration_data.date_of_birth.year

    return render_template(
        'birth-registration/dob.html',
        form=form
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
            if application_data.birth_registration_data.town_city_of_birth is not None:
                next_page = 'birthRegistration.checkYourAnswers'
            else:
                next_page = 'birthRegistration.placeOfBirth'
        else:
            if application_data.birth_registration_data.country_of_birth is not None:
                next_page = 'birthRegistration.checkYourAnswers'
            else:
                next_page = 'birthRegistration.country'

        return local_redirect(url_for(next_page))

    else:
        form.birth_registered_in_uk.data = application_data.birth_registration_data.birth_registered_in_uk

    return render_template(
        'birth-registration/uk-check.html',
        form=form
    )


@birthRegistration.route('/birth-registration/country', methods=['GET', 'POST'])
@LoginRequired
def country():
    form = CountryForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.birth_registration_data.country_of_birth = form.country_of_birth.data
        DataStore.save_application(application_data)

        return local_redirect(url_for('birthRegistration.checkYourAnswers'))

    if request.method == 'GET':
        form.country_of_birth.data = application_data.birth_registration_data.country_of_birth

    return render_template(
        'birth-registration/country.html',
        form=form
    )


@birthRegistration.route('/birth-registration/place-of-birth', methods=['GET', 'POST'])
@LoginRequired
def placeOfBirth():
    form = PlaceOfBirthForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.birth_registration_data.town_city_of_birth = form.place_of_birth.data
        DataStore.save_application(application_data)

        next_page = ('birthRegistration.checkYourAnswers'
                     if application_data.birth_registration_data.section_status == ListStatus.COMPLETED
                     else 'birthRegistration.mothersName')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.place_of_birth.data = application_data.birth_registration_data.town_city_of_birth

    return render_template(
        'birth-registration/place-of-birth.html',
        form=form
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

        next_page = ('birthRegistration.checkYourAnswers'
                     if application_data.birth_registration_data.section_status == ListStatus.COMPLETED
                     else 'birthRegistration.fathersNameCheck')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.first_name.data = application_data.birth_registration_data.mothers_first_name
        form.last_name.data = application_data.birth_registration_data.mothers_last_name
        form.maiden_name.data = application_data.birth_registration_data.mothers_maiden_name

    return render_template(
        'birth-registration/mothers-name.html',
        form=form
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

        if application_data.birth_registration_data.fathers_name_on_birth_certificate and \
            (application_data.birth_registration_data.fathers_first_name is None or
             application_data.birth_registration_data.fathers_last_name is None):
            # We are missing Father's Name - go to that page (even if we're IN_REVIEW)
            next_page = 'birthRegistration.fathersName'
        elif application_data.birth_registration_data.section_status == ListStatus.COMPLETED:
            next_page = 'birthRegistration.checkYourAnswers'
        elif application_data.birth_registration_data.fathers_name_on_birth_certificate:
            next_page = 'birthRegistration.fathersName'
        else:
            next_page = 'birthRegistration.adopted'

        return local_redirect(url_for(next_page))

    else:
        form.fathers_name_on_certificate.data = application_data.birth_registration_data.fathers_name_on_birth_certificate

    return render_template(
        'birth-registration/fathers-name-check.html',
        form=form
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

        next_page = ('birthRegistration.checkYourAnswers'
                     if application_data.birth_registration_data.section_status == ListStatus.COMPLETED
                     else 'birthRegistration.adopted')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.first_name.data = application_data.birth_registration_data.fathers_first_name
        form.last_name.data = application_data.birth_registration_data.fathers_last_name

    return render_template(
        'birth-registration/fathers-name.html',
        form=form
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

        if application_data.birth_registration_data.adopted and \
           application_data.birth_registration_data.adopted_in_the_uk is None:
            # We are missing "Adopted in the UK" - go to that page (even if we're IN_REVIEW)
            next_page = 'birthRegistration.adoptedUK'
        elif application_data.birth_registration_data.section_status == ListStatus.COMPLETED:
            next_page = 'birthRegistration.checkYourAnswers'
        elif application_data.birth_registration_data.adopted:
            next_page = 'birthRegistration.adoptedUK'
        else:
            next_page = 'birthRegistration.forces'

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.adopted.data = application_data.birth_registration_data.adopted

    return render_template(
        'birth-registration/adopted.html',
        form=form,
        back=back
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

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.adopted_uk.data = (
            application_data.birth_registration_data.adopted_in_the_uk.name
            if application_data.birth_registration_data.adopted_in_the_uk is not None else None)

    return render_template(
        'birth-registration/adopted-uk.html',
        form=form
    )


@birthRegistration.route('/birth-registration/forces', methods=['GET', 'POST'])
@LoginRequired
def forces():
    form = ForcesForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data.birth_registration_data.forces_registration = strtobool(form.forces.data)
        DataStore.save_application(application_data)

        return local_redirect(url_for('birthRegistration.checkYourAnswers'))

    if request.method == 'GET':
        form.forces.data = application_data.birth_registration_data.forces_registration

    return render_template(
        'birth-registration/forces.html',
        form=form,
        application_data=application_data
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

    return render_template(
        'birth-registration/check-your-answers.html',
        form=form,
        application_data=application_data
    )
