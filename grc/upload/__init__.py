from typing import List, Callable
from flask import Blueprint, render_template, request, url_for, abort
from werkzeug.utils import secure_filename
import fitz
import uuid
from grc.business_logic.data_store import DataStore
from grc.business_logic.data_structures.application_data import any_duplicate_aws_file_names
from grc.business_logic.data_structures.uploads_data import UploadsData, EvidenceFile
from grc.upload.forms import UploadForm, DeleteForm
from grc.utils.decorators import LoginRequired
from grc.external_services.aws_s3_client import AwsS3Client
from grc.utils.redirect import local_redirect
from grc.utils.logger import LogLevel, Logger

logger = Logger()

upload = Blueprint('upload', __name__)


class UploadSection:
    def __init__(self, url: str, data_section: str, html_file: str, file_list: Callable[[UploadsData], List[EvidenceFile]]):
        self.url = url
        self.data_section = data_section
        self.html_file = html_file
        self.file_list = file_list


sections = [
    UploadSection(url='medical-reports', data_section='medicalReports', html_file='medical-reports.html', file_list=(lambda u: u.medical_reports)),
    UploadSection(url='gender-evidence', data_section='genderEvidence', html_file='evidence.html', file_list=(lambda u: u.evidence_of_living_in_gender)),
    UploadSection(url='name-change', data_section='nameChange', html_file='name-change.html', file_list=(lambda u: u.name_change_documents)),
    UploadSection(url='marriage-documents', data_section='marriageDocuments', html_file='marriage-documents.html', file_list=(lambda u: u.partnership_documents)),
    UploadSection(url='overseas-certificate', data_section='overseasCertificate', html_file='overseas-certificate.html', file_list=(lambda u: u.overseas_documents)),
    UploadSection(url='statutory-declarations', data_section='statutoryDeclarations', html_file='statutory-declarations.html', file_list=(lambda u: u.statutory_declarations))
]

def delete_file(application_data, file_name, section):
    try:
        AwsS3Client().delete_object(file_name)
    except:
        logger.log(LogLevel.ERROR, f"Could not delete file {file_name}")
        # We could not delete the file. Perhaps it doesn't exist.
        pass
    files = section.file_list(application_data.uploads_data)
    file_to_remove = next(filter(lambda file: file.aws_file_name == file_name, files), None)
    files.remove(file_to_remove)
    return application_data


@upload.route('/upload/<section_url>', methods=['GET', 'POST'])
@LoginRequired
def uploadInfoPage(section_url: str):
    section = next(filter(lambda section: section.url == section_url, sections), None)
    if section is None:
        abort(404)

    form = UploadForm()
    deleteform = DeleteForm()
    application_data = DataStore.load_application_by_session_reference_number()
    files = section.file_list(application_data.uploads_data)

    if form.validate_on_submit():
        if form.button_clicked.data.startswith('Upload '):
            for document in request.files.getlist('documents'):
                object_name = create_aws_file_name(application_data.reference_number, section.data_section, document.filename)
                password_required = False

                if document.filename.lower().endswith('.pdf'):
                    try:
                        doc = fitz.open(stream=document.read(), filetype='pdf')
                        if doc.needs_pass:
                            password_required = True
                        doc.close()
                    except:
                        logger.log(LogLevel.ERROR, f"User uploaded PDF attachment ({object_name}) which could not be opened")

                AwsS3Client().upload_fileobj(document, object_name)

                new_evidence_file = EvidenceFile()
                new_evidence_file.original_file_name = document.filename
                new_evidence_file.aws_file_name = object_name
                new_evidence_file.password_required = password_required
                files.append(new_evidence_file)

            DataStore.save_application(application_data)

            return local_redirect(url_for('upload.uploadInfoPage', section_url=section.url) + '#file-upload-section')

        elif form.button_clicked.data == 'Save and continue':
            if len(files) > 0:
                return local_redirect(url_for('taskList.index'))
            else:
                form.documents.errors.append('Select a JPG, BMP, PNG, TIF or PDF file smaller than 10MB')

    return render_template(
        f"upload/{section.html_file}",
        form=form,
        deleteform=deleteform,
        section_url=section.url,
        currently_uploaded_files=files,
        duplicate_aws_file_names=any_duplicate_aws_file_names(files)
    )


def create_aws_file_name(reference_number, section_name, original_file_name):
    filename = secure_filename(original_file_name)
    last_dot_position = filename.rfind('.')
    file_prefix = (filename[:last_dot_position]) if last_dot_position > -1 else filename
    file_extension = (filename[(last_dot_position + 1):]) if last_dot_position > -1 else ''
    aws_file_name = f"{reference_number}__{section_name}__{file_prefix}_{uuid.uuid4().hex}.{file_extension}"
    return aws_file_name


@upload.route('/upload/<section_url>/remove-file', methods=['POST'])
@LoginRequired
def removeFile(section_url: str):
    section = next(filter(lambda section: section.url == section_url, sections), None)
    if section is None:
        abort(404)

    form = DeleteForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        application_data = delete_file(application_data, form.file.data, section)
        DataStore.save_application(application_data)

    return local_redirect(url_for('upload.uploadInfoPage', section_url=section.url) + '#file-upload-section')


@upload.route('/upload/<section_url>/remove-all-files-in-section', methods=['POST'])
@LoginRequired
def removeAllFilesInSection(section_url: str):
    section = next(filter(lambda section: section.url == section_url, sections), None)
    if section is None:
        abort(404)

    application_data = DataStore.load_application_by_session_reference_number()

    files = section.file_list(application_data.uploads_data)
    aws_file_names = list(map(lambda file: file.aws_file_name, files))
    for aws_file_name in aws_file_names:
        application_data = delete_file(application_data, aws_file_name, section)

    DataStore.save_application(application_data)

    return local_redirect(url_for('upload.uploadInfoPage', section_url=section.url))
