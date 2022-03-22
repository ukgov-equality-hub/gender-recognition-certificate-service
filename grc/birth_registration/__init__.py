from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    session,
)
from werkzeug.exceptions import abort
from flask import render_template

from grc.models import ListStatus
from grc.birth_registration.forms import (
    NameForm,
    SexForm,
    DobForm,
    UkCheckForm,
    CountryForm,
    PlaceOfBirthForm,
    MothersNameForm,
    FatherNameCheckForm,
    AdoptedForm,
    ForcesForm,
    CheckYourAnsewers,
)

from grc.utils.decorators import LoginRequired
from grc.utils.application_progress import save_progress


birthRegistration = Blueprint("birthRegistration", __name__)


@birthRegistration.route("/birth-registration", methods=["GET", "POST"])
@LoginRequired
def index():

    form = NameForm()

    if form.validate_on_submit():
        session["application"]["birthRegistration"]["first_name"] = form.first_name.data
        session["application"]["birthRegistration"]["last_name"] = form.last_name.data

        # set progress status
        if (
            ListStatus[session["application"]["birthRegistration"]["progress"]]
            == ListStatus.NOT_STARTED
        ):
            session["application"]["birthRegistration"][
                "progress"
            ] = ListStatus.IN_PROGRESS.name
            # set current step in case user exits the app
            session["application"]["birthRegistration"][
                "step"
            ] = "birthRegistration.sexCheck"

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["birthRegistration"]["step"]))

    if request.method == "GET":
        form.first_name.data = (
            session["application"]["birthRegistration"]["first_name"]
            if "first_name" in session["application"]["birthRegistration"]
            else None
        )
        form.last_name.data = (
            session["application"]["birthRegistration"]["last_name"]
            if "last_name" in session["application"]["birthRegistration"]
            else None
        )

    return render_template("birth-registration/name.html", form=form)


@birthRegistration.route("/birth-registration/sex", methods=["GET", "POST"])
@LoginRequired
def sexCheck():

    form = SexForm()

    if form.validate_on_submit():
        session["application"]["birthRegistration"]["sex"] = form.check.data

        # set current step in case user exits the app
        if (
            ListStatus[session["application"]["birthRegistration"]["progress"]]
            == ListStatus.IN_PROGRESS
        ):
            session["application"]["birthRegistration"][
                "step"
            ] = "birthRegistration.dob"

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["birthRegistration"]["step"]))

    return render_template("birth-registration/sex.html", form=form)


@birthRegistration.route("/birth-registration/dob", methods=["GET", "POST"])
@LoginRequired
def dob():

    form = DobForm()

    if form.validate_on_submit():
        if "date" not in session["application"]["birthRegistration"]:
            session["application"]["birthRegistration"]["dob"] = {}

        session["application"]["birthRegistration"]["dob"]["day"] = form.day.data
        session["application"]["birthRegistration"]["dob"]["month"] = form.month.data
        session["application"]["birthRegistration"]["dob"]["year"] = form.year.data

        # set current step in case user exits the app
        if (
            ListStatus[session["application"]["birthRegistration"]["progress"]]
            == ListStatus.IN_PROGRESS
        ):
            session["application"]["birthRegistration"][
                "step"
            ] = "birthRegistration.ukCheck"

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["birthRegistration"]["step"]))

    if request.method == "GET" and "dob" in session["application"]["birthRegistration"]:
        form.day.data = (
            session["application"]["birthRegistration"]["dob"]["day"]
            if "day" in session["application"]["birthRegistration"]["dob"]
            else None
        )
        form.month.data = (
            session["application"]["birthRegistration"]["dob"]["month"]
            if "month" in session["application"]["birthRegistration"]["dob"]
            else None
        )
        form.year.data = (
            session["application"]["birthRegistration"]["dob"]["year"]
            if "year" in session["application"]["birthRegistration"]["dob"]
            else None
        )

    return render_template("birth-registration/dob.html", form=form)


@birthRegistration.route("/birth-registration/uk-check", methods=["GET", "POST"])
@LoginRequired
def ukCheck():

    form = UkCheckForm()

    if form.validate_on_submit():
        session["application"]["birthRegistration"]["ukCheck"] = form.check.data

        # set current step in case user exits the app
        if form.check.data == "Yes":
            session["application"]["birthRegistration"][
                "step"
            ] = "birthRegistration.placeOfBirth"
        else:
            session["application"]["birthRegistration"][
                "step"
            ] = "birthRegistration.country"

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["birthRegistration"]["step"]))

    return render_template("birth-registration/uk-check.html", form=form)


@birthRegistration.route("/birth-registration/country", methods=["GET", "POST"])
@LoginRequired
def country():
    form = CountryForm()

    if form.validate_on_submit():
        session["application"]["birthRegistration"]["country"] = form.country.data

        session["application"]["birthRegistration"][
            "progress"
        ] = ListStatus.IN_REVIEW.name
        session["application"]["birthRegistration"][
            "step"
        ] = "birthRegistration.checkYourAnswers"

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["birthRegistration"]["step"]))

    if request.method == "GET":
        form.country.data = (
            session["application"]["birthRegistration"]["country"]
            if "country" in session["application"]["birthRegistration"]
            else None
        )

    return render_template("birth-registration/country.html", form=form)


@birthRegistration.route("/birth-registration/place-of-birth", methods=["GET", "POST"])
@LoginRequired
def placeOfBirth():

    form = PlaceOfBirthForm()

    if form.validate_on_submit():
        session["application"]["birthRegistration"][
            "place_of_birth"
        ] = form.place_of_birth.data

        # set current step in case user exits the app
        if (
            ListStatus[session["application"]["birthRegistration"]["progress"]]
            == ListStatus.IN_PROGRESS
        ):
            session["application"]["birthRegistration"][
                "step"
            ] = "birthRegistration.mothersName"
        else:
            session["application"]["birthRegistration"][
                "step"
            ] = "birthRegistration.checkYourAnswers"

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["birthRegistration"]["step"]))

    if request.method == "GET":
        form.place_of_birth.data = (
            session["application"]["birthRegistration"]["place_of_birth"]
            if "place_of_birth" in session["application"]["birthRegistration"]
            else None
        )

    return render_template("birth-registration/place-of-birth.html", form=form)


@birthRegistration.route("/birth-registration/mothers-name", methods=["GET", "POST"])
@LoginRequired
def mothersName():

    form = MothersNameForm()

    if form.validate_on_submit():
        session["application"]["birthRegistration"][
            "mothers_first_name"
        ] = form.first_name.data
        session["application"]["birthRegistration"][
            "mothers_last_name"
        ] = form.last_name.data
        session["application"]["birthRegistration"][
            "mothers_maiden_name"
        ] = form.maiden_name.data

        # set current step in case user exits the app
        if (
            ListStatus[session["application"]["birthRegistration"]["progress"]]
            == ListStatus.IN_PROGRESS
        ):
            session["application"]["birthRegistration"][
                "step"
            ] = "birthRegistration.fathersNameCheck"

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["birthRegistration"]["step"]))

    if request.method == "GET":
        form.first_name.data = (
            session["application"]["birthRegistration"]["mothers_first_name"]
            if "mothers_first_name" in session["application"]["birthRegistration"]
            else None
        )
        form.last_name.data = (
            session["application"]["birthRegistration"]["mothers_last_name"]
            if "mothers_last_name" in session["application"]["birthRegistration"]
            else None
        )
        form.maiden_name.data = (
            session["application"]["birthRegistration"]["mothers_maiden_name"]
            if "mothers_maiden_name" in session["application"]["birthRegistration"]
            else None
        )

    return render_template("birth-registration/mothers-name.html", form=form)


@birthRegistration.route(
    "/birth-registration/fathers-name-check", methods=["GET", "POST"]
)
@LoginRequired
def fathersNameCheck():

    form = FatherNameCheckForm()

    if form.validate_on_submit():
        session["application"]["birthRegistration"][
            "fathersNameCheck"
        ] = form.check.data

        # set current step in case user exits the app
        if (
            ListStatus[session["application"]["birthRegistration"]["progress"]]
            == ListStatus.IN_PROGRESS
        ):
            if form.check.data == "Yes":
                session["application"]["birthRegistration"][
                    "step"
                ] = "birthRegistration.fathersName"
            else:
                session["application"]["birthRegistration"][
                    "step"
                ] = "birthRegistration.adopted"
        elif form.check.data == "Yes":
            session["application"]["birthRegistration"][
                "step"
            ] = "birthRegistration.fathersName"

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["birthRegistration"]["step"]))

    return render_template("birth-registration/fathers-name-check.html", form=form)


@birthRegistration.route("/birth-registration/fathers-name", methods=["GET", "POST"])
@LoginRequired
def fathersName():

    form = NameForm()

    if form.validate_on_submit():
        session["application"]["birthRegistration"][
            "fathers_first_name"
        ] = form.first_name.data
        session["application"]["birthRegistration"][
            "fathers_last_name"
        ] = form.last_name.data

        # set current step in case user exits the app
        if (
            ListStatus[session["application"]["birthRegistration"]["progress"]]
            == ListStatus.IN_PROGRESS
        ):
            session["application"]["birthRegistration"][
                "step"
            ] = "birthRegistration.adopted"
        else:
            # go to summary
            session["application"]["birthRegistration"][
                "step"
            ] = "birthRegistration.checkYourAnswers"

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["birthRegistration"]["step"]))

    if request.method == "GET":
        form.first_name.data = (
            session["application"]["birthRegistration"]["fathers_first_name"]
            if "fathers_first_name" in session["application"]["birthRegistration"]
            else None
        )
        form.last_name.data = (
            session["application"]["birthRegistration"]["fathers_last_name"]
            if "fathers_last_name" in session["application"]["birthRegistration"]
            else None
        )

    return render_template("birth-registration/fathers-name.html", form=form)


@birthRegistration.route("/birth-registration/adopted", methods=["GET", "POST"])
@LoginRequired
def adopted():

    form = AdoptedForm()
    if session["application"]["birthRegistration"]["fathersNameCheck"] == "Yes":
        back = "birthRegistration.fathersName"
    else:
        back = "birthRegistration.fathersNameCheck"

    print(form.check.data)

    if form.validate_on_submit():
        session["application"]["birthRegistration"]["adopted"] = form.check.data
        if session["application"]["birthRegistration"]["adopted"] == "Yes":
            session["application"]["birthRegistration"][
                "adopted_uk"
            ] = form.adopted_uk.data

        # set current step in case user exits the app
        if (
            ListStatus[session["application"]["birthRegistration"]["progress"]]
            == ListStatus.IN_PROGRESS
        ):
            session["application"]["birthRegistration"][
                "step"
            ] = "birthRegistration.forces"

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["birthRegistration"]["step"]))

    return render_template("birth-registration/adopted.html", form=form, back=back)


@birthRegistration.route("/birth-registration/forces", methods=["GET", "POST"])
@LoginRequired
def forces():

    form = ForcesForm()
    if form.validate_on_submit():
        session["application"]["birthRegistration"]["forces"] = form.check.data

        # update progress status
        session["application"]["birthRegistration"][
            "progress"
        ] = ListStatus.IN_REVIEW.name

        # set current step in case user exits the app
        session["application"]["birthRegistration"][
            "step"
        ] = "birthRegistration.checkYourAnswers"

        session["application"] = save_progress()

        return redirect(url_for(session["application"]["birthRegistration"]["step"]))

    return render_template("birth-registration/forces.html", form=form)


@birthRegistration.route(
    "/birth-registration/check-your-answers", methods=["GET", "POST"]
)
@LoginRequired
def checkYourAnswers():

    form = CheckYourAnsewers()

    if "birthRegistration" not in session["application"] or (
        session["application"]["birthRegistration"]["progress"]
        != ListStatus.IN_REVIEW.name
        and session["application"]["birthRegistration"]["progress"]
        != ListStatus.COMPLETED.name
    ):
        return redirect(url_for("taskList.index"))

    if request.method == "POST":
        # update progress status on Save and Continue
        session["application"]["birthRegistration"][
            "progress"
        ] = ListStatus.COMPLETED.name
        session["application"]["birthRegistration"][
            "step"
        ] = "birthRegistration.checkYourAnswers"
        session["application"] = save_progress()
        return redirect(url_for("taskList.index"))

    # update progress status
    session["application"]["birthRegistration"]["progress"] = ListStatus.IN_REVIEW.name
    session["application"] = save_progress()

    return render_template("birth-registration/check-your-answers.html", form=form)
