import datetime
import io
from typing import List, Callable
from dateutil.relativedelta import relativedelta
from flask import Blueprint, render_template, request, url_for, abort, make_response
from werkzeug.utils import secure_filename
import uuid
from PIL import Image
from grc.business_logic.data_store import DataStore
from grc.business_logic.data_structures.application_data import any_duplicate_aws_file_names
from grc.business_logic.data_structures.uploads_data import UploadsData, EvidenceFile
from grc.upload.forms import UploadForm, DeleteForm, PasswordsForm, DeleteAllFilesInSectionForm
from grc.utils.decorators import LoginRequired
from grc.external_services.aws_s3_client import AwsS3Client
from grc.utils.flask_child_form_add_custom_errors import add_error_for_child_form
from grc.utils.pdf_utils import PDFUtils
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


def create_aws_file_name(reference_number, section_name, original_file_name):
    filename = secure_filename(original_file_name)
    last_dot_position = filename.rfind('.')
    file_prefix = (filename[:last_dot_position]) if last_dot_position > -1 else filename
    file_extension = (filename[(last_dot_position + 1):]) if last_dot_position > -1 else ''
    aws_file_name = f"{reference_number}__{section_name}__{file_prefix}_{uuid.uuid4().hex}.{file_extension}"
    return aws_file_name


def check_pdf_password(section, application_data, passwordForm):
    files = section.file_list(application_data.uploads_data)
    file_to_check = next(filter(lambda file: file.aws_file_name == passwordForm.aws_file_name.data, files), None)
    if file_to_check is not None:
        data = AwsS3Client().download_object(file_to_check.aws_file_name)
        if data is not None:
            input_pdf_stream = io.BytesIO(data.getvalue())
            if not PDFUtils().is_pdf_password_protected(input_pdf_stream):
                return True

            if PDFUtils().is_pdf_password_correct(input_pdf_stream, passwordForm.password.data):

                # Generate a new PDF
                output_pdf_stream = PDFUtils().remove_pdf_password_protection(input_pdf_stream, passwordForm.password.data)

                AwsS3Client().delete_object(file_to_check.aws_file_name)
                AwsS3Client().upload_fileobj(output_pdf_stream, file_to_check.aws_file_name)

                file_to_check.password_required = False
                DataStore.save_application(application_data)
                return True
    return False


def clear_form_errors(form):
    for _form_field, form_error in form.errors.items():
        form_error.clear()


def delete_password_protected_files(section, application_data):
    password_protected_files = [file for file in section.file_list(application_data.uploads_data) if file.password_required]
    for file in password_protected_files:
        application_data = delete_file(application_data, file.aws_file_name, section)
    return application_data


def resize_image(document):
    try:
        img = Image.open(document)
        file_name = document.filename

        width, height = img.size
        ratio = 1.
        if height >= width:
            if width > 1000:
                ratio = 1000 / width
            elif height > 1500:
                ratio = 1500 / height
        else:
            if width > 1500:
                ratio = 1500 / width
            elif height > 1000:
                ratio = 1000 / height
        if ratio != 1.:
            img = img.resize((int(width * ratio), int(height * ratio)), Image.ANTIALIAS)
            image_type = file_name[file_name.rindex('.') + 1:].lower()
            if image_type == 'tif': image_type = 'tiff'
            if image_type == 'jpg': image_type = 'jpeg'

            bytes_buffer = io.BytesIO()
            img.save(bytes_buffer, image_type)
            bytes_buffer.seek(0)
            #import pathlib
            #new_file_name = f'{pathlib.Path(__file__).parent.absolute()}/RESIZED__{file_name}'
            #img.save(new_file_name, image_type)

            return True, bytes_buffer

    except Exception as e:
        logger.log(LogLevel.ERROR, f"Could not resize image ({file_name}). Error was {e}")

    return False, document


@upload.route('/upload/<section_url>', methods=['GET', 'POST'])
@LoginRequired
def uploadInfoPage(section_url: str):
    section = next(filter(lambda section: section.url == section_url, sections), None)
    if section is None:
        return abort(404)

    form = UploadForm()
    deleteform = DeleteForm()
    deleteAllFilesInSectionForm = DeleteAllFilesInSectionForm()
    application_data = DataStore.load_application_by_session_reference_number()
    files = section.file_list(application_data.uploads_data)

    if form.validate_on_submit():
        if form.button_clicked.data.startswith('Upload '):
            has_password = False
            for document in request.files.getlist('documents'):
                original_file_name = document.filename
                object_name = create_aws_file_name(application_data.reference_number, section.data_section, original_file_name)
                password_required = False
                file_type = ''
                if '.' in original_file_name:
                    file_type = original_file_name[original_file_name.rindex('.') + 1:].lower()

                if file_type == 'pdf':
                    try:
                        data = io.BytesIO(document.read())
                        if PDFUtils().is_pdf_form(data):
                            document = PDFUtils().flatten_form_pdf_stream(data)

                        if PDFUtils().is_pdf_password_protected(data):
                            password_required = True
                            has_password = True

                        AwsS3Client().upload_fileobj(document, object_name)
                    except:
                        logger.log(LogLevel.ERROR, f"User uploaded PDF attachment ({object_name}) which could not be opened")

                elif file_type in ['jpg', 'jpeg', 'png', 'tif', 'tiff', 'bmp']:
                    resized, resized_document = resize_image(document)
                    AwsS3Client().upload_fileobj(resized_document, object_name)
                    if resized:
                        file_ext = ''
                        original_object_name = object_name
                        if '.' in original_object_name:
                            file_ext = original_object_name[original_object_name.rindex('.'):]
                            original_object_name = original_object_name[0: original_object_name.rindex('.')]
                        AwsS3Client().upload_fileobj(document, f'{original_object_name}_original{file_ext}')

                else:
                    AwsS3Client().upload_fileobj(document, object_name)

                new_evidence_file = EvidenceFile()
                new_evidence_file.original_file_name = original_file_name
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
        duplicate_aws_file_names=any_duplicate_aws_file_names(files),
        date_now=datetime.datetime.now(),
        date_two_years_ago=(datetime.datetime.now() - relativedelta(years=2))
    )


@upload.route('/upload/<section_url>/document-password', methods=['GET', 'POST'])
@LoginRequired
def documentPassword(section_url: str):
    section = next(filter(lambda section: section.url == section_url, sections), None)
    if section is None:
        return abort(404)

    passwordsForm = PasswordsForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if request.method == 'POST':
        remove_file_button_was_clicked = False
        for password_form in passwordsForm.files:
            if password_form.button_clicked.data:
                remove_file_button_was_clicked = True

        if remove_file_button_was_clicked:
            for password_form in passwordsForm.files:
                if password_form.button_clicked.data:
                    delete_file(application_data, password_form.aws_file_name.data, section)
                    DataStore.save_application(application_data)
        else:
            passwordsForm.validate()

            for passwordForm in passwordsForm.files:
                if passwordForm.password.data:
                    password_ok = check_pdf_password(section, application_data, passwordForm)
                    if not password_ok:
                        wrong_password_error_message = f"{passwordForm.original_file_name.data}: The password is incorrect"
                        add_error_for_child_form(passwordsForm.files, passwordForm, 'password', wrong_password_error_message)
                else:
                    no_password_error_message = f"{passwordForm.original_file_name.data}: Enter the password for this document"
                    add_error_for_child_form(passwordsForm.files, passwordForm, 'password', no_password_error_message)

    files = [file for file in section.file_list(application_data.uploads_data) if file.password_required]
    if len(files) == 0:
        return local_redirect(url_for('upload.uploadInfoPage', section_url=section.url) + '#file-upload-section')

    files_before = len(passwordsForm.files)
    passwordsForm.process(data={ 'files': files })
    files_after = len(passwordsForm.files)

    if files_before != files_after:
        clear_form_errors(passwordsForm)

    return render_template(
        "upload/document-password.html",
        passwordsForm=passwordsForm,
        section_url=section.url,
        currently_uploaded_files=files
    )


@upload.route('/upload/<section_url>/remove-file', methods=['POST'])
@LoginRequired
def removeFile(section_url: str):
    section = next(filter(lambda section: section.url == section_url, sections), None)
    if section is None:
        return abort(404)

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
        return abort(404)

    application_data = DataStore.load_application_by_session_reference_number()

    files = section.file_list(application_data.uploads_data)
    aws_file_names = list(map(lambda file: file.aws_file_name, files))
    for aws_file_name in aws_file_names:
        application_data = delete_file(application_data, aws_file_name, section)

    DataStore.save_application(application_data)

    return local_redirect(url_for('upload.uploadInfoPage', section_url=section.url))


@upload.route('/upload/<section_url>/download', methods=['GET'])
@LoginRequired
def download(section_url):
    section = next(filter(lambda section: section.url == section_url, sections), None)
    if section is None:
        return abort(404)

    file_name = request.args.get('file', default=None)
    if file_name is not None:
        application_data = DataStore.load_application_by_session_reference_number()
        files = [file for file in section.file_list(application_data.uploads_data) if file.aws_file_name == file_name]
        if '_original.' in file_name:
            pass
        elif len(files) == 0:
            return abort(403)

        data = AwsS3Client().download_object(file_name)
        if data:
            file_type = 'application/octet-stream'
            if '.' in file_name:
                file_type = file_name[file_name.rindex('.') + 1:].lower()
                if file_type == 'pdf':
                    file_type = 'application/pdf'
                elif file_type == 'jpg':
                    file_type = 'image/jpeg'
                else:
                    file_type = 'image/' + file_type

            bytes = data.getvalue()
            if bytes is None:
                return abort(406)

            response = make_response(bytes)
            response.headers.set('Content-Type', file_type)
            response.headers.set('Content-Disposition', 'attachment', filename=file_name)
            return response

    abort(404)
