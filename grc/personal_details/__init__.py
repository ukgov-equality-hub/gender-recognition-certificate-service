from datetime import datetime
from flask import Blueprint, render_template, request, url_for, session
from grc.models import ListStatus
from grc.personal_details.forms import NameForm, AffirmedGenderForm, TransitionDateForm, StatutoryDeclarationDateForm, PreviousNamesCheck, AddressForm, ContactPreferencesForm, ContactDatesForm, HmrcForm, CheckYourAnswers
from grc.utils.decorators import LoginRequired
from grc.utils.application_progress import save_progress
from grc.utils.redirect import local_redirect

personalDetails = Blueprint('personalDetails', __name__)


@personalDetails.route('/personal-details', methods=['GET', 'POST'])
@LoginRequired
def index():
    form = NameForm()

    if form.validate_on_submit():
        session['application']['personalDetails']['title'] = form.title.data
        session['application']['personalDetails']['first_name'] = form.first_name.data
        session['application']['personalDetails']['last_name'] = form.last_name.data

        if ListStatus[session['application']['personalDetails']['progress']] == ListStatus.NOT_STARTED:
            session['application']['personalDetails']['progress'] = ListStatus.IN_PROGRESS.name

        session['application'] = save_progress()

        next_page = ('personalDetails.checkYourAnswers'
                     if ListStatus[session['application']['birthRegistration']['progress']] == ListStatus.IN_REVIEW
                     else 'personalDetails.affirmedGender')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.title.data = (
            session['application']['personalDetails']['title']
            if 'title' in session['application']['personalDetails'] else None
        )
        form.first_name.data = (
            session['application']['personalDetails']['first_name']
            if 'first_name' in session['application']['personalDetails'] else None
        )
        form.last_name.data = (
            session['application']['personalDetails']['last_name']
            if 'last_name' in session['application']['personalDetails'] else None
        )

    return render_template(
        'personal-details/name.html',
        form=form
    )


@personalDetails.route('/personal-details/affirmed-gender', methods=['GET', 'POST'])
@LoginRequired
def affirmedGender():
    form = AffirmedGenderForm()

    if form.validate_on_submit():
        session['application']['personalDetails']['affirmed_gender'] = form.affirmedGender.data
        session['application'] = save_progress()

        next_page = ('personalDetails.checkYourAnswers'
                     if ListStatus[session['application']['birthRegistration']['progress']] == ListStatus.IN_REVIEW
                     else 'personalDetails.transitionDate')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.affirmedGender.data = (
            session['application']['personalDetails']['affirmed_gender']
            if 'affirmed_gender' in session['application']['personalDetails'] else None
        )

    return render_template(
        'personal-details/affirmed-gender.html',
        form=form
    )


@personalDetails.route('/personal-details/transition-date', methods=['GET', 'POST'])
@LoginRequired
def transitionDate():
    form = TransitionDateForm()

    if form.validate_on_submit():
        session['application']['personalDetails']['transition_date_month'] = form.transition_date_month.data
        session['application']['personalDetails']['transition_date_year'] = form.transition_date_year.data
        session['application'] = save_progress()

        next_page = ('personalDetails.checkYourAnswers'
                     if ListStatus[session['application']['birthRegistration']['progress']] == ListStatus.IN_REVIEW
                     else 'personalDetails.statutoryDeclarationDate')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.transition_date_month.data = (
            session['application']['personalDetails']['transition_date_month']
            if 'transition_date_month' in session['application']['personalDetails'] else None
        )
        form.transition_date_year.data = (
            session['application']['personalDetails']['transition_date_year']
            if 'transition_date_year' in session['application']['personalDetails'] else None
        )

    return render_template(
        'personal-details/transition-date.html',
        form=form
    )


@personalDetails.route('/personal-details/statutory-declaration-date', methods=['GET', 'POST'])
@LoginRequired
def statutoryDeclarationDate():
    form = StatutoryDeclarationDateForm()

    if form.validate_on_submit():
        session['application']['personalDetails']['statutory_declaration_date_day'] = form.statutory_declaration_date_day.data
        session['application']['personalDetails']['statutory_declaration_date_month'] = form.statutory_declaration_date_month.data
        session['application']['personalDetails']['statutory_declaration_date_year'] = form.statutory_declaration_date_year.data
        session['application'] = save_progress()

        next_page = ('personalDetails.checkYourAnswers'
                     if ListStatus[session['application']['birthRegistration']['progress']] == ListStatus.IN_REVIEW
                     else 'personalDetails.previousNamesCheck')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.statutory_declaration_date_day.data = (
            session['application']['personalDetails']['statutory_declaration_date_day']
            if 'statutory_declaration_date_day' in session['application']['personalDetails'] else None
        )
        form.statutory_declaration_date_month.data = (
            session['application']['personalDetails']['statutory_declaration_date_month']
            if 'statutory_declaration_date_month' in session['application']['personalDetails'] else None
        )
        form.statutory_declaration_date_year.data = (
            session['application']['personalDetails']['statutory_declaration_date_year']
            if 'statutory_declaration_date_year' in session['application']['personalDetails'] else None
        )

    return render_template(
        'personal-details/statutory-declaration-date.html',
        form=form
    )


@personalDetails.route('/personal-details/previous-names-check', methods=['GET', 'POST'])
@LoginRequired
def previousNamesCheck():
    form = PreviousNamesCheck()

    if form.validate_on_submit():
        session['application']['personalDetails']['previousNamesCheck'] = form.previousNameCheck.data
        session['application'] = save_progress()

        next_page = ('personalDetails.checkYourAnswers'
                     if ListStatus[session['application']['birthRegistration']['progress']] == ListStatus.IN_REVIEW
                     else 'personalDetails.address')

        return local_redirect(url_for(next_page))

    if request.method == 'GET':
        form.previousNameCheck.data = (
            session['application']['personalDetails']['previousNamesCheck']
            if 'previousNamesCheck' in session['application']['personalDetails'] else None
        )

    return render_template(
        'personal-details/previous-names-check.html',
        form=form
    )


@personalDetails.route('/personal-details/address', methods=['GET', 'POST'])
@LoginRequired
def address():
    form = AddressForm()

    if form.validate_on_submit():
        if 'address' not in session['application']['personalDetails']:
            session['application']['personalDetails']['address'] = {}

        session['application']['personalDetails']['address']['address_line_one'] = form.address_line_one.data
        session['application']['personalDetails']['address']['address_line_two'] = form.address_line_two.data
        session['application']['personalDetails']['address']['town'] = form.town.data
        session['application']['personalDetails']['address']['postcode'] = form.postcode.data
        session['application'] = save_progress()

        next_page = ('personalDetails.checkYourAnswers'
                     if ListStatus[session['application']['birthRegistration']['progress']] == ListStatus.IN_REVIEW
                     else 'personalDetails.contactDates')

        return local_redirect(url_for(next_page))

    if request.method == 'GET'  and 'address' in session['application']['personalDetails']:
        form.address_line_one.data = (
            session['application']['personalDetails']['address']['address_line_one']
            if 'address_line_one' in session['application']['personalDetails']['address'] else None
        )
        form.address_line_two.data = (
            session['application']['personalDetails']['address']['address_line_two']
            if 'address_line_two' in session['application']['personalDetails']['address'] else None
        )
        form.town.data = (
            session['application']['personalDetails']['address']['town']
            if 'town' in session['application']['personalDetails']['address'] else None
        )
        form.postcode.data = (
            session['application']['personalDetails']['address']['postcode']
            if 'postcode' in session['application']['personalDetails']['address'] else None
        )

    return render_template(
        'personal-details/address.html',
        form=form
    )


@personalDetails.route('/personal-details/contact-preferences', methods=['GET', 'POST'])
@LoginRequired
def contactPreferences():
    form = ContactPreferencesForm()
    address = session['application']['personalDetails']['address']['address_line_one'] + ', ' + session['application']['personalDetails']['address']['address_line_two'] + ', ' + session['application']['personalDetails']['address']['town'] + ', ' +  session['application']['personalDetails']['address']['postcode']

    if request.method == 'POST':
        if 'EMAIL' not in form.contact_options.data:
            form.email.data = None
        if 'PHONE' not in form.contact_options.data:
            form.phone.data = None

        if form.validate_on_submit():
            if 'personalDetails' not in session['application']:
                session['application']['personalDetails'] = {}

            if 'contactPreferences' not in session['application']['personalDetails']:
                session['application']['personalDetails']['contactPreferences'] = {
                    'email': '',
                    'phone': '',
                    'post': ''
                }

            if 'EMAIL' in form.contact_options.data:
                session['application']['personalDetails']['contactPreferences']['email'] = form.email.data
            else:
                session['application']['personalDetails']['contactPreferences']['email'] = ''
            if 'PHONE' in form.contact_options.data:
                session['application']['personalDetails']['contactPreferences']['phone'] = form.phone.data
            else:
                session['application']['personalDetails']['contactPreferences']['phone'] = ''
            if 'POST' in form.contact_options.data:
                session['application']['personalDetails']['contactPreferences']['post'] = address
            else:
                session['application']['personalDetails']['contactPreferences']['post'] = ''

            session['application'] = save_progress()

            next_page = ('personalDetails.checkYourAnswers'
                         if ListStatus[session['application']['birthRegistration']['progress']] == ListStatus.IN_REVIEW
                         else 'personalDetails.hmrc')

            return local_redirect(url_for(next_page))

    if request.method == 'GET' and 'contactPreferences' in session['application']['personalDetails']:
        form.contact_options.data = []
        if session['application']['personalDetails']['contactPreferences']['email']:
            form.contact_options.data.append('EMAIL')
        if session['application']['personalDetails']['contactPreferences']['phone']:
            form.contact_options.data.append('PHONE')
        if session['application']['personalDetails']['contactPreferences']['post']:
            form.contact_options.data.append('POST')

        form.email.data = (
            session['application']['personalDetails']['contactPreferences']['email']
            if 'email' in session['application']['personalDetails']['contactPreferences'] else None
        )
        form.phone.data = (
            session['application']['personalDetails']['contactPreferences']['phone']
            if 'phone' in session['application']['personalDetails']['contactPreferences'] else None
        )


    return render_template(
        'personal-details/contact-preferences.html',
        form=form,
        address=address
    )


@personalDetails.route('/personal-details/contact-dates', methods=['GET', 'POST'])
@LoginRequired
def contactDates():
    form = ContactDatesForm()

    if request.method == 'POST':
        if form.contactDatesCheck.data != 'Yes':
            form.dates.data = ''

        if form.validate_on_submit():
            if 'personalDetails' not in session['application']:
                session['application']['personalDetails'] = {}

            if 'contactDates' not in session['application']['personalDetails']:
                session['application']['personalDetails']['contactDates'] = {
                    'answer': '',
                    'dates': ''
                }

            session['application']['personalDetails']['contactDates']['dates'] = form.dates.data
            session['application']['personalDetails']['contactDates']['answer'] = form.contactDatesCheck.data
            session['application'] = save_progress()

            next_page = ('personalDetails.checkYourAnswers'
                         if ListStatus[session['application']['birthRegistration']['progress']] == ListStatus.IN_REVIEW
                         else 'personalDetails.contactPreferences')

            return local_redirect(url_for(next_page))

    if request.method == 'GET' and 'contactDates' in session['application']['personalDetails']:
        form.contactDatesCheck.data = (
            session['application']['personalDetails']['contactDates']['answer']
            if 'answer' in session['application']['personalDetails']['contactDates'] else None
        )
        form.dates.data = (
            session['application']['personalDetails']['contactDates']['dates']
            if 'dates' in session['application']['personalDetails']['contactDates'] else None
        )

    return render_template(
        'personal-details/contact-dates.html',
        form=form
    )


@personalDetails.route('/personal-details/hmrc', methods=['GET', 'POST'])
@LoginRequired
def hmrc():
    form = HmrcForm()

    if request.method == 'POST':
        if form.tell_hmrc.data != 'Yes':
            form.national_insurance_number.data = None

        if form.validate_on_submit():
            if 'personalDetails' not in session['application']:
                session['application']['personalDetails'] = {}

            if 'hmrc' not in session['application']['personalDetails']:
                session['application']['personalDetails']['hmrc'] = {
                    'answer': '',
                    'national_insurance_number': ''
                }

            session['application']['personalDetails']['hmrc']['national_insurance_number'] = form.national_insurance_number.data
            session['application']['personalDetails']['hmrc']['answer'] = form.tell_hmrc.data
            session['application']['personalDetails']['progress'] = ListStatus.IN_REVIEW.name
            session['application'] = save_progress()

            return local_redirect(url_for('personalDetails.checkYourAnswers'))

    if request.method == 'GET' and 'hmrc' in session['application']['personalDetails']:
        form.tell_hmrc.data = (
            session['application']['personalDetails']['hmrc']['answer']
            if 'answer' in session['application']['personalDetails']['hmrc'] else None
        )
        form.national_insurance_number.data = (
            session['application']['personalDetails']['hmrc']['national_insurance_number']
            if 'national_insurance_number' in session['application']['personalDetails']['hmrc'] else None
        )

    return render_template(
        'personal-details/hmrc.html',
        form=form
    )


@personalDetails.route('/personal-details/check-your-answers', methods=['GET', 'POST'])
@LoginRequired
def checkYourAnswers():
    form = CheckYourAnswers()

    if 'personalDetails' not in session['application'] or (session['application']['personalDetails']['progress'] != ListStatus.IN_REVIEW.name and session['application']['personalDetails']['progress'] != ListStatus.COMPLETED.name):
        return local_redirect(url_for('taskList.index'))

    if request.method == 'POST':
        session['application']['personalDetails']['progress'] = ListStatus.COMPLETED.name
        session['application'] = save_progress()

        return local_redirect(url_for('taskList.index'))

    session['application']['personalDetails']['progress'] = ListStatus.IN_REVIEW.name
    session['application'] = save_progress()

    return render_template(
        'personal-details/check-your-answers.html',
        form=form,
        strptime=datetime.strptime
    )
