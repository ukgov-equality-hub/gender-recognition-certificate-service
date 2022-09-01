from typing import List, Callable
from flask import Blueprint, render_template, request, url_for, abort, make_response
from werkzeug.utils import secure_filename
import fitz
import uuid
from grc.business_logic.data_store import DataStore
from grc.business_logic.data_structures.application_data import any_duplicate_aws_file_names
from grc.business_logic.data_structures.uploads_data import UploadsData, EvidenceFile
from grc.upload.forms import UploadForm, DeleteForm, PasswordsForm, DeleteAllFilesInSectionForm
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
    except Exception as e:
        logger.log(LogLevel.ERROR, f"Could not delete file ({file_name}). Error was {e}")
        # We could not delete the file. Perhaps it doesn't exist.
        pass
    files = section.file_list(application_data.uploads_data)
    file_to_remove = next(filter(lambda file: file.aws_file_name == file_name, files), None)
    files.remove(file_to_remove)
    return application_data

def create_pdf_from_doc(doc):
    import io

    merger = fitz.open()
    merger.insert_pdf(doc)
    pdf = io.BytesIO()
    merger.save(pdf, deflate=True)
    merger.close()
    pdf.seek(0)
    return pdf

def create_aws_file_name(reference_number, section_name, original_file_name):
    filename = secure_filename(original_file_name)
    last_dot_position = filename.rfind('.')
    file_prefix = (filename[:last_dot_position]) if last_dot_position > -1 else filename
    file_extension = (filename[(last_dot_position + 1):]) if last_dot_position > -1 else ''
    aws_file_name = f"{reference_number}__{section_name}__{file_prefix}_{uuid.uuid4().hex}.{file_extension}"
    return aws_file_name

def check_pdf_password(section, application_data, passwordForm):
    password_ok = False
    files = section.file_list(application_data.uploads_data)
    file_to_check = next(filter(lambda file: file.aws_file_name == passwordForm.aws_file_name.data, files), None)
    if file_to_check is not None:
        data = AwsS3Client().download_object(file_to_check.aws_file_name)
        if data is not None:
            doc = fitz.open(stream=data.getvalue(), filetype='pdf')
            if doc.needs_pass:
                if doc.authenticate(passwordForm.password.data):

                    # Generate a new PDF
                    pdf = create_pdf_from_doc(doc)

                    AwsS3Client().delete_object(file_to_check.aws_file_name)
                    AwsS3Client().upload_fileobj(pdf, file_to_check.aws_file_name)

                    file_to_check.password_required = False
                    DataStore.save_application(application_data)
                    password_ok = True

            doc.close()
    return application_data, password_ok

def clear_form_errors(form):
    for _form_field, form_error in form.errors.items():
        form_error.clear()

def delete_password_protected_files(section, application_data):
    password_protected_files = [file for file in section.file_list(application_data.uploads_data) if file.password_required]
    for file in password_protected_files:
        application_data = delete_file(application_data, file.aws_file_name, section)
    return application_data


@upload.route('/upload/<section_url>', methods=['GET', 'POST'])
@LoginRequired
def uploadInfoPage(section_url: str):
    section = next(filter(lambda section: section.url == section_url, sections), None)
    if section is None:
        abort(404)

    form = UploadForm()
    deleteform = DeleteForm()
    deleteAllFilesInSectionForm = DeleteAllFilesInSectionForm()
    application_data = DataStore.load_application_by_session_reference_number()
    files = section.file_list(application_data.uploads_data)

    if form.validate_on_submit():
        if form.button_clicked.data.startswith('Upload '):
            has_password = False
            for document in request.files.getlist('documents'):
                object_name = create_aws_file_name(application_data.reference_number, section.data_section, document.filename)
                password_required = False

                if document.filename.lower().endswith('.pdf'):
                    try:
                        doc = fitz.open(stream=document.read(), filetype='pdf')
                        if doc.needs_pass:
                            password_required = True
                            has_password = True
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

            if has_password:
                return local_redirect(url_for('upload.documentPassword', section_url=section.url))
            else:
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
        deleteAllFilesInSectionForm=deleteAllFilesInSectionForm,
        section_url=section.url,
        currently_uploaded_files=files,
        duplicate_aws_file_names=any_duplicate_aws_file_names(files)
    )


@upload.route('/upload/<section_url>/document-password', methods=['GET', 'POST'])
@LoginRequired
def documentPassword(section_url: str):
    section = next(filter(lambda section: section.url == section_url, sections), None)
    if section is None:
        abort(404)

    passwordsForm = PasswordsForm()
    application_data = DataStore.load_application_by_session_reference_number()
    error = ''
    file_index = -1


    if passwordsForm.validate_on_submit():

        # All password fields have been submitted
        errors = []
        for passwordForm in passwordsForm.files:
            application_data, password_ok = check_pdf_password(section, application_data, passwordForm)
            if not password_ok:
                errors.append(f'{passwordForm.original_file_name.data}: The password is incorrect')  # { 'password': ['The password is incorrect'] }

        passwordsForm.files.errors = errors

    elif request.method == 'POST':

        # EITHER remove has been clicked, OR not all passwords have been entered
        remove_file = False
        for passwordForm in passwordsForm.files:
            if passwordForm.button_clicked.data:
                application_data = delete_file(application_data, passwordForm.aws_file_name.data, section)
                DataStore.save_application(application_data)
                remove_file = True
                clear_form_errors(passwordsForm)

        if not remove_file:
            errors = []
            has_password = False
            for passwordForm in passwordsForm.files:
                if passwordForm.password.data:
                    has_password = True
                    application_data, password_ok = check_pdf_password(section, application_data, passwordForm)
                    if not password_ok:
                        errors.append(f'{passwordForm.original_file_name.data}: The password is incorrect')
                else:
                    errors.append('')

            if not has_password:
                errors = []
                for passwordForm in passwordsForm.files:
                    errors.append(f'{passwordForm.original_file_name.data}: The password is required')

            clear_form_errors(passwordsForm)
            for error in errors:
                if error != '':
                    passwordsForm.files.errors = errors

    files = [file for file in section.file_list(application_data.uploads_data) if file.password_required]
    if len(files) == 0:
        return local_redirect(url_for('upload.uploadInfoPage', section_url=section.url) + '#file-upload-section')
    passwordsForm.process(data={ 'files': files })

    return render_template(
        "upload/document-password.html",
        passwordsForm=passwordsForm,
        section_url=section.url,
        currently_uploaded_files=files,
        error=error,
        file_index=file_index
    )


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

    files = section.file_list(application_data.uploads_data)
    if request.referrer.endswith('/document-password') and len(files) > 0:
        return local_redirect(url_for('upload.documentPassword', section_url=section.url))
    else:
        return local_redirect(url_for('upload.uploadInfoPage', section_url=section.url) + '#file-upload-section')


@upload.route('/upload/<section_url>/remove-all-files-in-section', methods=['POST'])
@LoginRequired
def removeAllFilesInSection(section_url: str):
    # The following line looks pointless, but it validates the CSRF token
    #   Without this, we get an HTTP 405 Method Not Allowed error on the following page
    form = DeleteAllFilesInSectionForm()

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
