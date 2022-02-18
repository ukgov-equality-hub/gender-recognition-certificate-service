from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from flask import render_template

from grc.models import ListStatus
from grc.personal_details.forms import NameForm, PreviousNamesCheck, AddressForm, ContactPreferencesForm, ContactNameForm,ContactDatesForm, HmrcForm, CheckYourAnsewers

from grc.utils.decorators import LoginRequired
from grc.utils.application_progress import save_progress


personalDetails = Blueprint('personalDetails', __name__)

@personalDetails.route('/personal-details', methods=['GET', 'POST'])
@LoginRequired
def index():

    form = NameForm()

    if form.validate_on_submit():
        session["application"]["personalDetails"]["first_name"] = form.first_name.data
        session["application"]["personalDetails"]["last_name"] = form.last_name.data

        # set progress status
        if ListStatus[session["application"]["personalDetails"]["progress"]] == ListStatus.NOT_STARTED:
            session["application"]["personalDetails"]["progress"] = ListStatus.IN_PROGRESS.name
            # set current step in case user exits the app
            session["application"]["personalDetails"]["step"] = 'personalDetails.previousNamesCheck'

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["personalDetails"]["step"]))

    if request.method == 'GET':
        form.first_name.data = session["application"]["personalDetails"]["first_name"] if "first_name" in session["application"]["personalDetails"] else None
        form.last_name.data = session["application"]["personalDetails"]["last_name"] if "last_name" in session["application"]["personalDetails"] else None

    return render_template('personal-details/name.html', form=form)



@personalDetails.route('/personal-details/previous-names-check', methods=['GET', 'POST'])
@LoginRequired
def previousNamesCheck():

    form = PreviousNamesCheck()

    if form.validate_on_submit():
        session["application"]["personalDetails"]["previousNamesCheck"] = form.check.data

        # set current step in case user exits the app
        if ListStatus[session["application"]["personalDetails"]["progress"]] == ListStatus.IN_PROGRESS:
            session["application"]["personalDetails"]["step"] = 'personalDetails.address'

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["personalDetails"]["step"]))

    return render_template('personal-details/previous-names-check.html', form=form)


@personalDetails.route('/personal-details/address', methods=['GET', 'POST'])
@LoginRequired
def address():

    form = AddressForm()

    if form.validate_on_submit():
        if "address" not in session["application"]["personalDetails"]:
            session["application"]["personalDetails"]["address"] = {}

        session["application"]["personalDetails"]["address"]["address_line_one"] = form.address_line_one.data
        session["application"]["personalDetails"]["address"]["address_line_two"] = form.address_line_two.data
        session["application"]["personalDetails"]["address"]["town"] = form.town.data
        session["application"]["personalDetails"]["address"]["postcode"] = form.postcode.data
        # set current step in case user exits the app
        if ListStatus[session["application"]["personalDetails"]["progress"]] == ListStatus.IN_PROGRESS:
            session["application"]["personalDetails"]["step"] = 'personalDetails.contactPreferences'

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["personalDetails"]["step"]))

    if request.method == 'GET'  and "address" in session["application"]["personalDetails"]:
        form.address_line_one.data = session["application"]["personalDetails"]["address"]["address_line_one"] if "address_line_one" in session["application"]["personalDetails"]["address"] else None
        form.address_line_two.data = session["application"]["personalDetails"]["address"]["address_line_two"] if "address_line_two" in session["application"]["personalDetails"]["address"] else None
        form.town.data = session["application"]["personalDetails"]["address"]["town"] if "town" in session["application"]["personalDetails"]["address"] else None
        form.postcode.data = session["application"]["personalDetails"]["address"]["postcode"] if "postcode" in session["application"]["personalDetails"]["address"] else None

    return render_template('personal-details/address.html', form=form)


@personalDetails.route('/personal-details/contact-preferences', methods=['GET', 'POST'])
@LoginRequired
def contactPreferences():

    form = ContactPreferencesForm()
    address = session["application"]["personalDetails"]["address"]["address_line_one"] + ", " + session["application"]["personalDetails"]["address"]["address_line_two"] + ", " + session["application"]["personalDetails"]["address"]["town"] + ", " +  session["application"]["personalDetails"]["address"]["postcode"]

    if request.method == 'POST':
        if 'email' not in form.options.data:
            form.email.data = None
        if 'phone' not in form.options.data:
            form.phone.data = None

        if form.validate_on_submit():

            if "personalDetails" not in session["application"]:
                session["application"]["personalDetails"] = {}

            if "contactPreferences" not in session["application"]["personalDetails"]:
                session["application"]["personalDetails"]["contactPreferences"] = {
                    "email": "",
                    "phone": "",
                    "post": ""
                }

            if 'email' in form.options.data:
                session["application"]["personalDetails"]["contactPreferences"]["email"] = form.email.data
            else:
                session["application"]["personalDetails"]["contactPreferences"]["email"] = ''
            if 'phone' in form.options.data:
                session["application"]["personalDetails"]["contactPreferences"]["phone"] = form.phone.data
            else:
                session["application"]["personalDetails"]["contactPreferences"]["phone"] = ''
            if 'post' in form.options.data:
                session["application"]["personalDetails"]["contactPreferences"]["post"] = address
            else:
                session["application"]["personalDetails"]["contactPreferences"]["post"] = ''
            # set current step in case user exits the app
            if ListStatus[session["application"]["personalDetails"]["progress"]] == ListStatus.IN_PROGRESS:
                session["application"]["personalDetails"]["step"] = 'personalDetails.contactName'

            session["application"] = save_progress()

            return redirect(url_for(session["application"]["personalDetails"]["step"]))

    if request.method == 'GET' and "contactPreferences" in session["application"]["personalDetails"]:
        form.options.data =[]
        if  len(session["application"]["personalDetails"]["contactPreferences"]["email"]) > 0:
            form.options.data.append('email')
        if  len(session["application"]["personalDetails"]["contactPreferences"]["phone"]) > 0:
            form.options.data.append('phone')
        if  len(session["application"]["personalDetails"]["contactPreferences"]["post"]) > 0:
            form.options.data.append('post')

        form.email.data = session["application"]["personalDetails"]["contactPreferences"]["email"]
        form.phone.data = session["application"]["personalDetails"]["contactPreferences"]["phone"]



    return render_template('personal-details/contact-preferences.html', form=form, address=address)


@personalDetails.route('/personal-details/contact-name', methods=['GET', 'POST'])
@LoginRequired
def contactName():

    form = ContactNameForm()
    # del session["application"]["personalDetails"]["contactName"]
    # session["application"] = save_progress()
    if request.method == 'POST':
        if form.check.data != 'Yes':
            form.name.data = None

        if form.validate_on_submit():
            if "personalDetails" not in session["application"]:
                session["application"]["personalDetails"] = {}

            if "contactName" not in session["application"]["personalDetails"]:
                session["application"]["personalDetails"]["contactName"] = {
                    "answer": "",
                    "name": "",
                }

            if 'Yes' in form.check.data:
                session["application"]["personalDetails"]["contactName"]["name"] = form.name.data
            else:
                session["application"]["personalDetails"]["contactName"]["name"] = ''

            session["application"]["personalDetails"]["contactName"]["answer"] = form.check.data
           # set current step in case user exits the app
            # print(url_for(session["application"]["personalDetails"]["step"]), session["application"]["personalDetails"]["step"], ListStatus[session["application"]["personalDetails"]["progress"]] == ListStatus.IN_PROGRESS)
            if ListStatus[session["application"]["personalDetails"]["progress"]] == ListStatus.IN_PROGRESS:
                session["application"]["personalDetails"]["step"] = 'personalDetails.contactDates'

            session["application"] = save_progress()

            return redirect(url_for(session["application"]["personalDetails"]["step"]))

    if request.method == 'GET' and "contactName" in session["application"]["personalDetails"]:
        form.check.data =[]

        form.check.data.append(session["application"]["personalDetails"]["contactName"]["answer"])
        form.name.data = session["application"]["personalDetails"]["contactName"]["name"]


    return render_template('personal-details/contact-name.html', form=form)


@personalDetails.route('/personal-details/contact-dates', methods=['GET', 'POST'])
@LoginRequired
def contactDates():

    form = ContactDatesForm()

    if request.method == 'POST':
        if form.check.data != 'Yes':
            form.dates.data = None

        if form.validate_on_submit():
            if "personalDetails" not in session["application"]:
                session["application"]["personalDetails"] = {}

            if "contactDates" not in session["application"]["personalDetails"]:
                session["application"]["personalDetails"]["contactDates"] = {
                    "answer": "",
                    "dates": "",
                }

            if 'Yes' in form.check.data:
                session["application"]["personalDetails"]["contactDates"]["dates"] = form.dates.data
            else:
                session["application"]["personalDetails"]["contactDates"]["dates"] = ''

            session["application"]["personalDetails"]["contactDates"]["answer"] = form.check.data
            # set current step in case user exits the app
            if ListStatus[session["application"]["personalDetails"]["progress"]] == ListStatus.IN_PROGRESS:
                session["application"]["personalDetails"]["step"] = 'personalDetails.hmrc'

            session["application"] = save_progress()

            return redirect(url_for(session["application"]["personalDetails"]["step"]))

    if request.method == 'GET' and "contactDates" in session["application"]["personalDetails"]:
        form.check.data =[]

        form.check.data.append(session["application"]["personalDetails"]["contactDates"]["answer"])
        form.dates.data = session["application"]["personalDetails"]["contactDates"]["dates"]


    return render_template('personal-details/contact-dates.html', form=form)



@personalDetails.route('/personal-details/hmrc', methods=['GET', 'POST'])
@LoginRequired
def hmrc():

    form = HmrcForm()
    # del session["application"]["personalDetails"]["hmrc"]
    # session["application"] = save_progress()
    if request.method == 'POST':
        if form.check.data != 'Yes':
            form.nino.data = None

        if form.validate_on_submit():
            if "personalDetails" not in session["application"]:
                session["application"]["personalDetails"] = {}

            if "hmrc" not in session["application"]["personalDetails"]:
                session["application"]["personalDetails"]["hmrc"] = {
                    "answer": "",
                    "nino": "",
                }

            if 'Yes' in form.check.data:
                session["application"]["personalDetails"]["hmrc"]["nino"] = form.nino.data
            else:
                session["application"]["personalDetails"]["hmrc"]["nino"] = ''

            session["application"]["personalDetails"]["hmrc"]["answer"] = form.check.data

            # update progress status
            session["application"]["personalDetails"]["progress"] = ListStatus.IN_REVIEW.name

            # set current step in case user exits the app
            session["application"]["personalDetails"]["step"] = 'personalDetails.checkYourAnswers'

            session["application"] = save_progress()

            return redirect(url_for(session["application"]["personalDetails"]["step"]))

    if request.method == 'GET' and "hmrc" in session["application"]["personalDetails"]:
        form.check.data =[]

        form.check.data.append(session["application"]["personalDetails"]["hmrc"]["answer"])
        form.nino.data = session["application"]["personalDetails"]["hmrc"]["nino"]


    return render_template('personal-details/hmrc.html', form=form)


@personalDetails.route('/personal-details/check-your-answers', methods=['GET', 'POST'])
@LoginRequired
def checkYourAnswers():

    form = CheckYourAnsewers()

    if "personalDetails" not in session["application"] or (session["application"]["personalDetails"]["progress"] != ListStatus.IN_REVIEW.name and session["application"]["personalDetails"]["progress"] != ListStatus.COMPLETED.name):
        return redirect(url_for('taskList.index'))

    if request.method == 'POST':
        # update progress status on Save and Continue
        session["application"]["personalDetails"]["progress"] = ListStatus.COMPLETED.name
        session["application"]["personalDetails"]["step"] = 'personalDetails.checkYourAnswers'
        session["application"] = save_progress()
        return redirect(url_for('taskList.index'))

    # update progress status
    session["application"]["personalDetails"]["progress"] = ListStatus.IN_REVIEW.name
    session["application"] = save_progress()

    return render_template('personal-details/check-your-answers.html', form=form)