from flask import (
    Blueprint, flash, g, redirect, render_template, current_app, request, url_for, session, send_file
)
from werkzeug.exceptions import abort
from flask import render_template
from werkzeug.utils import secure_filename

from grc.models import ListStatus
from grc.upload.forms import UploadForm, DeleteForm

from grc.utils.decorators import LoginRequired
from grc.utils.application_progress import save_progress
from grc.utils.s3 import upload_fileobj, create_presigned_url, delete_object

import boto3
#boto3.set_stream_logger('')
from botocore.client import Config


upload = Blueprint('upload', __name__)

@upload.route('/upload/medical-reports', methods=['GET', 'POST'])
@LoginRequired
def medicalReports():
    form = UploadForm()
    deleteform = DeleteForm()

    if form.validate_on_submit():
        if "files" not in session["application"]["medicalReports"]:
            session["application"]["medicalReports"]["files"] = []

        for document in request.files.getlist("documents"):
            filename = secure_filename(document.filename)
            object_name = session["application"]["reference_number"] + '__' + 'medicalReports' + '__' + filename
            upload_fileobj(document, object_name)
            session["application"]["medicalReports"]["files"].append(object_name)

        # set progress status
        session["application"]["medicalReports"]["progress"] = ListStatus.COMPLETED.name
        session["application"] = save_progress()

        return redirect(url_for('taskList.index'))

    if request.method == 'GET' and "files" in session["application"]["medicalReports"] and len(session["application"]["medicalReports"]["files"]) == 0:
         # set progress status
        session["application"]["medicalReports"]["progress"] = ListStatus.IN_PROGRESS.name
        session["application"] = save_progress()

    return render_template('upload/medical-reports.html', form=form, deleteform=deleteform)


@upload.route('/upload/gender-evidence', methods=['GET', 'POST'])
@LoginRequired
def genderEvidence():
    form = UploadForm()
    deleteform = DeleteForm()

    if form.validate_on_submit():
        if "files" not in session["application"]["genderEvidence"]:
            session["application"]["genderEvidence"]["files"] = []

        for document in request.files.getlist("documents"):
            filename = secure_filename(document.filename)
            object_name = session["application"]["reference_number"] + '__' + 'genderEvidence' + '__' + filename
            upload_fileobj(document, object_name)
            session["application"]["genderEvidence"]["files"].append(object_name)

        # set progress status
        session["application"]["genderEvidence"]["progress"] = ListStatus.COMPLETED.name
        session["application"] = save_progress()

        return redirect(url_for('taskList.index'))

    if request.method == 'GET' and "files" in session["application"]["genderEvidence"] and len(session["application"]["genderEvidence"]["files"]) == 0:
         # set progress status
        session["application"]["genderEvidence"]["progress"] = ListStatus.IN_PROGRESS.name
        session["application"] = save_progress()

    return render_template('upload/evidence.html', form=form, deleteform=deleteform)


@upload.route('/upload/name-change', methods=['GET', 'POST'])
@LoginRequired
def nameChange():
    form = UploadForm()
    deleteform = DeleteForm()

    if form.validate_on_submit():
        if "files" not in session["application"]["nameChange"]:
            session["application"]["nameChange"]["files"] = []

        for document in request.files.getlist("documents"):
            filename = secure_filename(document.filename)
            object_name = session["application"]["reference_number"] + '__' + 'nameChange' + '__' + filename
            upload_fileobj(document, object_name)
            session["application"]["nameChange"]["files"].append(object_name)

        # set progress status
        session["application"]["nameChange"]["progress"] = ListStatus.COMPLETED.name
        session["application"] = save_progress()

        return redirect(url_for('taskList.index'))

    if request.method == 'GET' and "files" in session["application"]["nameChange"] and len(session["application"]["nameChange"]["files"]) == 0:
         # set progress status
        session["application"]["nameChange"]["progress"] = ListStatus.IN_PROGRESS.name
        session["application"] = save_progress()

    return render_template('upload/name-change.html', form=form, deleteform=deleteform)

@upload.route('/upload/remove-file', methods=['POST'])
@LoginRequired
def removeFile():
    form = DeleteForm()

    if form.validate_on_submit():
        delete_object(form.file.data)
        session["application"][form.section.data]["files"].remove(form.file.data)
        session["application"] = save_progress()

    return redirect(form.redirect_route.data)

# @upload.route('/upload/get-file', methods=['GET'])
# @LoginRequired
# def downloadFile():
#     file = create_presigned_url('')
#     return redirect(file)