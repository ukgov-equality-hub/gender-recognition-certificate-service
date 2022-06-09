from flask import Blueprint, render_template, request, url_for, session, abort
from werkzeug.utils import secure_filename
from grc.models import ListStatus
from grc.upload.forms import UploadForm, DeleteForm
from grc.utils.decorators import LoginRequired
from grc.utils.application_progress import save_progress
from grc.external_services.aws_s3_client import AwsS3Client
from grc.utils.redirect import local_redirect

upload = Blueprint('upload', __name__)


class UploadSection:
    def __init__(self, url: str, data_section: str, html_file: str):
        self.url = url
        self.data_section = data_section
        self.html_file = html_file


sections = [
    UploadSection(url='medical-reports', data_section='medicalReports', html_file='medical-reports.html'),
    UploadSection(url='gender-evidence', data_section='genderEvidence', html_file='evidence.html'),
    UploadSection(url='name-change', data_section='nameChange', html_file='name-change.html'),
    UploadSection(url='foo', data_section='foo', html_file='foo.html'),
    UploadSection(url='marriage-documents', data_section='marriageDocuments', html_file='marriage-documents.html'),
    UploadSection(url='overseas-certificate', data_section='overseasCertificate', html_file='overseas-certificate.html'),
    UploadSection(url='statutory-declarations', data_section='statutoryDeclarations', html_file='statutory-declarations.html')
]


@upload.route('/upload/<section_url>', methods=['GET', 'POST'])
@LoginRequired
def uploadInfoPage(section_url: str):
    section = next(filter(lambda section: section.url == section_url, sections), None)
    if section is None:
        abort(404)

    form = UploadForm()
    deleteform = DeleteForm()

    if form.validate_on_submit():
        if section.data_section not in session['application']:
            session['application'][section.data_section] = []

        if 'files' not in session['application'][section.data_section]:
            session['application'][section.data_section]['files'] = []

        for document in request.files.getlist('documents'):
            filename = secure_filename(document.filename)
            object_name = session['application']['reference_number'] + '__' + section.data_section + '__' + filename
            AwsS3Client().upload_fileobj(document, object_name)
            session['application'][section.data_section]['files'].append(object_name)

        session['application'][section.data_section]['progress'] = ListStatus.COMPLETED.name
        session['application'] = save_progress()

        if not form.more_files.data == True:
            return local_redirect(url_for('taskList.index'))
        else:
            return local_redirect(url_for('upload.uploadInfoPage', section_url=section.url) + '#file-upload-section')

    elif request.method == 'POST' and 'document' not in request.files and 'files' in session['application'][section.data_section] and len(session['application'][section.data_section]['files']) > 0:
        return local_redirect(url_for('taskList.index'))

    if request.method == 'GET' and 'files' in session['application'][section.data_section] and len(session['application'][section.data_section]['files']) == 0:
        session['application'][section.data_section]['progress'] = ListStatus.IN_PROGRESS.name
        session['application'] = save_progress()

    return render_template(
        f"upload/{section.html_file}",
        form=form,
        deleteform=deleteform,
        section=section
    )


@upload.route('/upload/<section_url>/remove-file', methods=['POST'])
@LoginRequired
def removeFile(section_url: str):
    section = next(filter(lambda section: section.url == section_url, sections), None)
    if section is None:
        abort(404)

    form = DeleteForm()

    if form.validate_on_submit():
        AwsS3Client().delete_object(form.file.data)
        session['application'][section.data_section]['files'].remove(form.file.data)
        session['application'] = save_progress()

    return local_redirect(url_for('upload.uploadInfoPage', section_url=section.url) + '#file-upload-section')
