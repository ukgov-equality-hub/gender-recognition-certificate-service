from datetime import datetime
from flask import Blueprint, render_template, request, url_for, session
from grc.models import ListStatus
from grc.birth_registration.forms import  NameForm, DobForm, UkCheckForm, CountryForm, PlaceOfBirthForm, MothersNameForm, FatherNameCheckForm, FathersNameForm, AdoptedForm, AdoptedUKForm, ForcesForm, CheckYourAnswers
from grc.utils.decorators import LoginRequired
from grc.utils.application_progress import save_progress
from grc.utils.radio_values_helper import get_radio_pretty_value
from grc.utils.redirect import local_redirect

birthRegistration = Blueprint('birthRegistration', __name__)


@birthRegistration.route('/birth-registration', methods=['GET', 'POST'])
@LoginRequired
def index():
    form = NameForm()

    if form.validate_on_submit():
        session['application']['birthRegistration']['first_name'] = form.first_name.data
        session['application']['birthRegistration']['middle_names'] = form.middle_names.data
        session['application']['birthRegistration']['last_name'] = form.last_name.data

        if ListStatus[session['application']['birthRegistration']['progress']] == ListStatus.NOT_STARTED:
            session['application']['birthRegistration']['progress'] = ListStatus.IN_PROGRESS.name

        session['application'] = save_progress()

        next_page = ('birthRegistration.checkYourAnswers'
                     if ListStatus[session['application']['birthRegistration']['progress']] == ListStatus.IN_REVIEW
                     else 'birthRegistration.dob')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.first_name.data = (
            session['application']['birthRegistration']['first_name']
            if 'first_name' in session['application']['birthRegistration'] else None
        )
        form.middle_names.data = (
            session['application']['birthRegistration']['middle_names']
            if 'middle_names' in session['application']['birthRegistration'] else None
        )
        form.last_name.data = (
            session['application']['birthRegistration']['last_name']
            if 'last_name' in session['application']['birthRegistration'] else None
        )

    return render_template(
        'birth-registration/name.html',
        form=form
    )


@birthRegistration.route('/birth-registration/dob', methods=['GET', 'POST'])
@LoginRequired
def dob():
    form = DobForm()

    if form.validate_on_submit():
        if 'date' not in session['application']['birthRegistration']:
            session['application']['birthRegistration']['dob'] = {}

        session['application']['birthRegistration']['dob']['day'] = form.day.data
        session['application']['birthRegistration']['dob']['month'] = form.month.data
        session['application']['birthRegistration']['dob']['year'] = form.year.data
        session['application'] = save_progress()

        next_page = ('birthRegistration.checkYourAnswers'
                     if ListStatus[session['application']['birthRegistration']['progress']] == ListStatus.IN_REVIEW
                     else 'birthRegistration.ukCheck')

        return local_redirect(url_for(next_page))

    if request.method == 'GET' and 'dob' in session['application']['birthRegistration']:
        form.day.data = (
            session['application']['birthRegistration']['dob']['day']
            if 'day' in session['application']['birthRegistration']['dob'] else None
        )
        form.month.data = (
            session['application']['birthRegistration']['dob']['month']
            if 'month' in session['application']['birthRegistration']['dob'] else None
        )
        form.year.data = (
            session['application']['birthRegistration']['dob']['year']
            if 'year' in session['application']['birthRegistration']['dob'] else None
        )

    return render_template(
        'birth-registration/dob.html',
        form=form
    )


@birthRegistration.route('/birth-registration/uk-check', methods=['GET', 'POST'])
@LoginRequired
def ukCheck():
    form = UkCheckForm()

    if form.validate_on_submit():
        session['application']['birthRegistration']['ukCheck'] = form.birth_registered_in_uk.data
        session['application'] = save_progress()

        if form.birth_registered_in_uk.data == 'Yes':
            if 'place_of_birth' in session['application']['birthRegistration']:
                next_page = 'birthRegistration.checkYourAnswers'
            else:
                session['application']['birthRegistration']['progress'] = ListStatus.IN_PROGRESS.name
                next_page = 'birthRegistration.placeOfBirth'
        else:
            if 'country' in session['application']['birthRegistration']:
                next_page = 'birthRegistration.checkYourAnswers'
            else:
                session['application']['birthRegistration']['progress'] = ListStatus.IN_PROGRESS.name
                next_page = 'birthRegistration.country'

        return local_redirect(url_for(next_page))

    else:
        form.birth_registered_in_uk.data = (
            session['application']['birthRegistration']['ukCheck']
            if 'ukCheck' in session['application']['birthRegistration']
            else None
        )

    return render_template(
        'birth-registration/uk-check.html',
        form=form
    )


@birthRegistration.route('/birth-registration/country', methods=['GET', 'POST'])
@LoginRequired
def country():
    form = CountryForm()

    if form.validate_on_submit():
        session['application']['birthRegistration']['country'] = form.country_of_birth.data
        session['application']['birthRegistration']['progress'] = ListStatus.IN_REVIEW.name
        session['application'] = save_progress()

        return local_redirect(url_for('birthRegistration.checkYourAnswers'))

    if request.method == 'GET':
        form.country_of_birth.data = (
            session['application']['birthRegistration']['country']
            if 'country' in session['application']['birthRegistration'] else None
        )

    return render_template(
        'birth-registration/country.html',
        form=form
    )


@birthRegistration.route('/birth-registration/place-of-birth', methods=['GET', 'POST'])
@LoginRequired
def placeOfBirth():
    form = PlaceOfBirthForm()

    if form.validate_on_submit():
        session['application']['birthRegistration']['place_of_birth'] = form.place_of_birth.data
        session['application'] = save_progress()

        next_page = ('birthRegistration.checkYourAnswers'
                     if ListStatus[session['application']['birthRegistration']['progress']] == ListStatus.IN_REVIEW
                     else 'birthRegistration.mothersName')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.place_of_birth.data = (
            session['application']['birthRegistration']['place_of_birth']
            if 'place_of_birth' in session['application']['birthRegistration'] else None
        )

    return render_template(
        'birth-registration/place-of-birth.html',
        form=form
    )


@birthRegistration.route('/birth-registration/mothers-name', methods=['GET', 'POST'])
@LoginRequired
def mothersName():
    form = MothersNameForm()

    if form.validate_on_submit():
        session['application']['birthRegistration']['mothers_first_name'] = form.first_name.data
        session['application']['birthRegistration']['mothers_last_name'] = form.last_name.data
        session['application']['birthRegistration']['mothers_maiden_name'] = form.maiden_name.data
        session['application'] = save_progress()

        next_page = ('birthRegistration.checkYourAnswers'
                     if ListStatus[session['application']['birthRegistration']['progress']] == ListStatus.IN_REVIEW
                     else 'birthRegistration.fathersNameCheck')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.first_name.data = (
            session['application']['birthRegistration']['mothers_first_name']
            if 'mothers_first_name' in session['application']['birthRegistration'] else None
        )
        form.last_name.data = (
            session['application']['birthRegistration']['mothers_last_name']
            if 'mothers_last_name' in session['application']['birthRegistration'] else None
        )
        form.maiden_name.data = (
            session['application']['birthRegistration']['mothers_maiden_name']
            if 'mothers_maiden_name' in session['application']['birthRegistration'] else None
        )

    return render_template(
        'birth-registration/mothers-name.html',
        form=form
    )


@birthRegistration.route('/birth-registration/fathers-name-check', methods=['GET', 'POST'])
@LoginRequired
def fathersNameCheck():
    form = FatherNameCheckForm()

    if form.validate_on_submit():
        session['application']['birthRegistration']['fathersNameCheck'] = form.fathers_name_on_certificate.data

        session['application'] = save_progress()

        if form.fathers_name_on_certificate.data == 'Yes' and \
            ('fathers_first_name' not in session['application']['birthRegistration'] or
             'fathers_last_name' not in session['application']['birthRegistration']):
            # We are missing Father's Name - go to that page (even if we're IN_REVIEW)
            next_page = 'birthRegistration.fathersName'
        elif ListStatus[session['application']['birthRegistration']['progress']] == ListStatus.IN_REVIEW:
            next_page = 'birthRegistration.checkYourAnswers'
        elif form.fathers_name_on_certificate.data == 'Yes':
            next_page = 'birthRegistration.fathersName'
        else:
            next_page = 'birthRegistration.adopted'

        return local_redirect(url_for(next_page))

    else:
        form.fathers_name_on_certificate.data = (
            session['application']['birthRegistration']['fathersNameCheck']
            if 'fathersNameCheck' in session['application']['birthRegistration']
            else None
        )

    return render_template(
        'birth-registration/fathers-name-check.html',
        form=form
    )


@birthRegistration.route('/birth-registration/fathers-name', methods=['GET', 'POST'])
@LoginRequired
def fathersName():
    form = FathersNameForm()

    if form.validate_on_submit():
        session['application']['birthRegistration']['fathers_first_name'] = form.first_name.data
        session['application']['birthRegistration']['fathers_last_name'] = form.last_name.data
        session['application'] = save_progress()

        next_page = ('birthRegistration.checkYourAnswers'
                     if ListStatus[session['application']['birthRegistration']['progress']] == ListStatus.IN_REVIEW
                     else 'birthRegistration.adopted')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.first_name.data = (
            session['application']['birthRegistration']['fathers_first_name']
            if 'fathers_first_name' in session['application']['birthRegistration'] else None
        )
        form.last_name.data = (
            session['application']['birthRegistration']['fathers_last_name']
            if 'fathers_last_name' in session['application']['birthRegistration'] else None
        )

    return render_template(
        'birth-registration/fathers-name.html',
        form=form
    )


@birthRegistration.route('/birth-registration/adopted', methods=['GET', 'POST'])
@LoginRequired
def adopted():
    form = AdoptedForm()

    if session['application']['birthRegistration']['fathersNameCheck'] == 'Yes':
        back = 'birthRegistration.fathersName'
    else:
        back = 'birthRegistration.fathersNameCheck'

    if form.validate_on_submit():
        session['application']['birthRegistration']['adopted'] = form.adopted.data
        if form.adopted.data == 'No':
            session['application']['birthRegistration'].pop('adopted_uk', None)

        session['application'] = save_progress()

        if form.adopted.data == 'Yes' and \
            ('adopted_uk' not in session['application']['birthRegistration']):
            # We are missing "Adopted in the UK" - go to that page (even if we're IN_REVIEW)
            next_page = 'birthRegistration.adoptedUK'
        elif ListStatus[session['application']['birthRegistration']['progress']] == ListStatus.IN_REVIEW:
            next_page = 'birthRegistration.checkYourAnswers'
        elif form.adopted.data == 'Yes':
            next_page = 'birthRegistration.adoptedUK'
        else:
            next_page = 'birthRegistration.forces'

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.adopted.data = (
            session['application']['birthRegistration']['adopted']
            if 'adopted' in session['application']['birthRegistration']
            else None
        )

    return render_template(
        'birth-registration/adopted.html',
        form=form,
        back=back
    )


@birthRegistration.route('/birth-registration/adopted-uk', methods=['GET', 'POST'])
@LoginRequired
def adoptedUK():
    form = AdoptedUKForm()

    if form.validate_on_submit():
        session['application']['birthRegistration']['adopted_uk'] = form.adopted_uk.data
        session['application'] = save_progress()

        next_page = ('birthRegistration.checkYourAnswers'
                     if ListStatus[session['application']['birthRegistration']['progress']] == ListStatus.IN_REVIEW
                     else 'birthRegistration.forces')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.adopted_uk.data = (
            session['application']['birthRegistration']['adopted_uk']
            if 'adopted_uk' in session['application']['birthRegistration']
            else None
        )

    return render_template(
        'birth-registration/adopted-uk.html',
        form=form
    )


@birthRegistration.route('/birth-registration/forces', methods=['GET', 'POST'])
@LoginRequired
def forces():
    form = ForcesForm()

    if form.validate_on_submit():
        session['application']['birthRegistration']['forces'] = form.forces.data
        session['application']['birthRegistration']['progress'] = ListStatus.IN_REVIEW.name
        session['application'] = save_progress()

        return local_redirect(url_for('birthRegistration.checkYourAnswers'))

    if request.method == 'GET':
        form.forces.data = (
            session['application']['birthRegistration']['forces']
            if 'forces' in session['application']['birthRegistration']
            else None
        )

    return render_template(
        'birth-registration/forces.html',
        form=form
    )


@birthRegistration.route('/birth-registration/check-your-answers', methods=['GET', 'POST'])
@LoginRequired
def checkYourAnswers():
    form = CheckYourAnswers()

    if 'birthRegistration' not in session['application'] or (
        session['application']['birthRegistration']['progress'] != ListStatus.IN_REVIEW.name
        and session['application']['birthRegistration']['progress'] != ListStatus.COMPLETED.name
    ):
        return local_redirect(url_for('taskList.index'))

    if request.method == 'POST':
        session['application']['birthRegistration']['progress'] = ListStatus.COMPLETED.name
        session['application'] = save_progress()

        return local_redirect(url_for('taskList.index'))

    session['application']['birthRegistration']['progress'] = ListStatus.IN_REVIEW.name
    session['application'] = save_progress()

    return render_template(
        'birth-registration/check-your-answers.html',
        form=form,
        strptime=datetime.strptime,
        get_radio_pretty_value=get_radio_pretty_value
    )
