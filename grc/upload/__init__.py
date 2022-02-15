from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, send_file
)
from werkzeug.exceptions import abort
from flask import render_template
from werkzeug.utils import secure_filename

from grc.models import ListStatus
from grc.upload.forms import UploadForm

from grc.utils.decorators import LoginRequired
from grc.utils.application_progress import save_progress
from grc.utils.s3 import upload_fileobj, create_presigned_url


upload = Blueprint('upload', __name__)

@upload.route('/upload/medical-reports', methods=['GET', 'POST'])
@LoginRequired
def medicalReports():

    form = UploadForm()

    if form.validate_on_submit():
        if "files" not in session["application"]["medicalReports"]:
            session["application"]["medicalReports"]["files"] = []

        for document in request.files.getlist("documents"):
            print(document.filename)
            print(document)
            filename = secure_filename(document.filename)
            object_name = session["application"]["reference_number"] + '/' +filename
            print(upload_fileobj(document, object_name))
            session["application"]["medicalReports"]["files"].append(object_name)

        # set progress status
        session["application"]["medicalReports"]["progress"] = ListStatus.COMPLETED.name

        session["application"] = save_progress()

        return redirect(url_for('taskList.index'))

    return render_template('upload/medical-reports.html', form=form)


@upload.route('/upload/gender-evidence', methods=['GET', 'POST'])
@LoginRequired
def genderEvidence():

    form = UploadForm()

    if form.validate_on_submit():
        if "files" not in session["application"]["genderEvidence"]:
            session["application"]["genderEvidence"]["files"] = []

        for document in request.files.getlist("documents"):
            print(document.filename)
            print(document)
            filename = secure_filename(document.filename)
            object_name = session["application"]["reference_number"] + '/' +filename
            print(upload_fileobj(document, object_name))
            session["application"]["genderEvidence"]["files"].append(object_name)

        # set progress status
        session["application"]["genderEvidence"]["progress"] = ListStatus.COMPLETED.name

        session["application"] = save_progress()

        return redirect(url_for('taskList.index'))

    return render_template('upload/evidence.html', form=form)


# @upload.route('/upload/get-file', methods=['GET'])
# @LoginRequired
# def downloadFile():
#     file = create_presigned_url('WSRHYP0C/3by2.jpeg')
#     return redirect(file)