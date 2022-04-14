from flask import Blueprint, redirect, render_template, request, url_for, session
from werkzeug.utils import secure_filename
from grc.models import ListStatus
from grc.upload.forms import UploadForm, DeleteForm
from grc.utils.decorators import LoginRequired
from grc.utils.application_progress import save_progress
from grc.utils.s3 import upload_fileobj, delete_object

upload = Blueprint('upload', __name__)


@upload.route('/upload/medical-reports', methods=['GET', 'POST'])
@LoginRequired
def medicalReports():
    form = UploadForm()
    deleteform = DeleteForm()

    if form.validate_on_submit():
        if 'medicalReports' not in session['application']:
            session['application']['medicalReports'] = []

        if 'files' not in session['application']['medicalReports']:
            session['application']['medicalReports']['files'] = []

        for document in request.files.getlist('documents'):
            filename = secure_filename(document.filename)
            object_name = session['application']['reference_number'] + '__' + 'medicalReports' + '__' + filename
            upload_fileobj(document, object_name)
            session['application']['medicalReports']['files'].append(object_name)

        session['application']['medicalReports']['progress'] = ListStatus.COMPLETED.name
        session['application'] = save_progress()

        if not form.more_files.data == True:
            return redirect(url_for('taskList.index'))

    if request.method == 'GET' and 'files' in session['application']['medicalReports'] and len(session['application']['medicalReports']['files']) == 0:
        session['application']['medicalReports']['progress'] = ListStatus.IN_PROGRESS.name
        session['application'] = save_progress()

    return render_template(
        'upload/medical-reports.html',
        form=form,
        deleteform=deleteform
    )


@upload.route('/upload/gender-evidence', methods=['GET', 'POST'])
@LoginRequired
def genderEvidence():
    form = UploadForm()
    deleteform = DeleteForm()

    if form.validate_on_submit():
        if 'genderEvidence' not in session['application']:
            session['application']['genderEvidence'] = []

        if 'files' not in session['application']['genderEvidence']:
            session['application']['genderEvidence']['files'] = []

        for document in request.files.getlist('documents'):
            filename = secure_filename(document.filename)
            object_name = session['application']['reference_number'] + '__' + 'genderEvidence' + '__' + filename
            upload_fileobj(document, object_name)
            session['application']['genderEvidence']['files'].append(object_name)

        session['application']['genderEvidence']['progress'] = ListStatus.COMPLETED.name
        session['application'] = save_progress()

        if not form.more_files.data == True:
            return redirect(url_for('taskList.index'))

    if request.method == 'GET' and 'files' in session['application']['genderEvidence'] and len(session['application']['genderEvidence']['files']) == 0:
        session['application']['genderEvidence']['progress'] = ListStatus.IN_PROGRESS.name
        session['application'] = save_progress()

    return render_template(
        'upload/evidence.html',
        form=form,
        deleteform=deleteform
    )


@upload.route('/upload/name-change', methods=['GET', 'POST'])
@LoginRequired
def nameChange():
    form = UploadForm()
    deleteform = DeleteForm()

    if form.validate_on_submit():
        if 'nameChange' not in session['application']:
            session['application']['nameChange'] = []

        if 'files' not in session['application']['nameChange']:
            session['application']['nameChange']['files'] = []

        for document in request.files.getlist('documents'):
            filename = secure_filename(document.filename)
            object_name = session['application']['reference_number'] + '__' + 'nameChange' + '__' + filename
            upload_fileobj(document, object_name)
            session['application']['nameChange']['files'].append(object_name)

        session['application']['nameChange']['progress'] = ListStatus.COMPLETED.name
        session['application'] = save_progress()

        if not form.more_files.data == True:
            return redirect(url_for('taskList.index'))

    if request.method == 'GET' and 'files' in session['application']['nameChange'] and len(session['application']['nameChange']['files']) == 0:
        session['application']['nameChange']['progress'] = ListStatus.IN_PROGRESS.name
        session['application'] = save_progress()

    return render_template(
        'upload/name-change.html',
        form=form,
        deleteform=deleteform
    )


@upload.route('/upload/marriage-documents', methods=['GET', 'POST'])
@LoginRequired
def marriageDocuments():
    form = UploadForm()
    deleteform = DeleteForm()

    if form.validate_on_submit():
        if 'marriageDocuments' not in session['application']:
            session['application']['marriageDocuments'] = []

        if 'files' not in session['application']['marriageDocuments']:
            session['application']['marriageDocuments']['files'] = []

        for document in request.files.getlist('documents'):
            filename = secure_filename(document.filename)
            object_name = session['application']['reference_number'] + '__' + 'marriageDocuments' + '__' + filename
            upload_fileobj(document, object_name)
            session['application']['marriageDocuments']['files'].append(object_name)

        session['application']['marriageDocuments']['progress'] = ListStatus.COMPLETED.name
        session['application'] = save_progress()

        if not form.more_files.data == True:
            return redirect(url_for('taskList.index'))

    if request.method == 'GET' and 'files' in session['application']['marriageDocuments'] and len(session['application']['marriageDocuments']['files']) == 0:
        session['application']['marriageDocuments']['progress'] = ListStatus.IN_PROGRESS.name
        session['application'] = save_progress()

    return render_template(
        'upload/marriage-documents.html',
        form=form,
        deleteform=deleteform
    )


@upload.route('/upload/overseas-certificate', methods=['GET', 'POST'])
@LoginRequired
def overseasCertificate():
    form = UploadForm()
    deleteform = DeleteForm()

    if form.validate_on_submit():
        if 'overseasCertificate' not in session['application']:
            session['application']['overseasCertificate'] = []

        if 'files' not in session['application']['overseasCertificate']:
            session['application']['overseasCertificate']['files'] = []

        for document in request.files.getlist('documents'):
            filename = secure_filename(document.filename)
            object_name = session['application']['reference_number'] + '__' + 'overseasCertificate' + '__' + filename
            upload_fileobj(document, object_name)
            session['application']['overseasCertificate']['files'].append(object_name)

        session['application']['overseasCertificate']['progress'] = ListStatus.COMPLETED.name
        session['application'] = save_progress()

        if not form.more_files.data == True:
            return redirect(url_for('taskList.index'))

    if request.method == 'GET' and 'files' in session['application']['overseasCertificate'] and len(session['application']['overseasCertificate']['files']) == 0:
        session['application']['overseasCertificate']['progress'] = ListStatus.IN_PROGRESS.name
        session['application'] = save_progress()

    return render_template(
        'upload/overseas-certificate.html',
        form=form,
        deleteform=deleteform
    )


@upload.route('/upload/statutory-declarations', methods=['GET', 'POST'])
@LoginRequired
def statutoryDeclarations():
    form = UploadForm()
    deleteform = DeleteForm()

    if form.validate_on_submit():
        if 'statutoryDeclarations' not in session['application']:
            session['application']['statutoryDeclarations'] = []

        if 'files' not in session['application']['statutoryDeclarations']:
            session['application']['statutoryDeclarations']['files'] = []

        for document in request.files.getlist('documents'):
            filename = secure_filename(document.filename)
            object_name = session['application']['reference_number'] + '__' + 'statutoryDeclarations' + '__' + filename
            upload_fileobj(document, object_name)
            session['application']['statutoryDeclarations']['files'].append(object_name)

        session['application']['statutoryDeclarations']['progress'] = ListStatus.COMPLETED.name
        session['application'] = save_progress()

        if not form.more_files.data == True:
            return redirect(url_for('taskList.index'))

    if request.method == 'GET' and 'files' in session['application']['statutoryDeclarations'] and len(session['application']['statutoryDeclarations']['files']) == 0:
        session['application']['statutoryDeclarations']['progress'] = ListStatus.IN_PROGRESS.name
        session['application'] = save_progress()

    return render_template(
        'upload/statutory-declarations.html',
        form=form,
        deleteform=deleteform
    )


@upload.route('/upload/remove-file', methods=['POST'])
@LoginRequired
def removeFile():
    form = DeleteForm()

    if form.validate_on_submit():
        delete_object(form.file.data)
        session['application'][form.section.data]['files'].remove(form.file.data)
        session['application'] = save_progress()

    return redirect(form.redirect_route.data)


# @upload.route('/upload/get-file', methods=['GET'])
# @LoginRequired
# def downloadFile():
#     file = create_presigned_url('')
#     return redirect(file)
