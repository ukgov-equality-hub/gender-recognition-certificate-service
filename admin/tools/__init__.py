import io
from flask import Blueprint, render_template, make_response, request
from admin.tools.forms import UnlockFileForm
from grc.utils.decorators import AdminViewerRequired
from grc.utils.logger import Logger, LogLevel
from grc.utils.pdf_utils import is_pdf_password_correct, is_pdf_password_protected, remove_pdf_password_protection, \
    remove_pdf_edit_protection

tools = Blueprint('tools', __name__)
logger = Logger()


@tools.route('/tools', methods=['GET'])
@AdminViewerRequired
def index():
    return render_template('tools/tools.html')


@tools.route('/tools/unlock-pdfs', methods=['GET', 'POST'])
@AdminViewerRequired
def unlock_pdfs():
    form = UnlockFileForm()

    if form.validate_on_submit():
        file = request.files.getlist('file')[0]
        output_pdf_stream: io.BytesIO = io.BytesIO()
        try:
            input_pdf_stream = io.BytesIO(file.read())

            if is_pdf_password_protected(input_pdf_stream):
                if form.pdf_password.data:
                    if is_pdf_password_correct(input_pdf_stream, form.pdf_password.data):
                        output_pdf_stream = remove_pdf_password_protection(input_pdf_stream, form.pdf_password.data)
                    else:
                        form.pdf_password.errors.append('The password was incorrect. You will also need to select the file again')
                else:
                    form.file.errors.append("This file is password protected. Enter the password. You will also need to select the file again")
            else:
                output_pdf_stream = remove_pdf_edit_protection(input_pdf_stream)

            if not form.errors:
                pdf_bytes = output_pdf_stream.read()

                input_file_name_prefix = get_filename_without_pdf_extension(file.filename)
                output_file_name = f"{input_file_name_prefix} (unlocked).pdf"

                return make_pdf_download_response(pdf_bytes, output_file_name)

        except Exception as e:
            logger.log(LogLevel.ERROR, f"File could not be converted. Error was {e}")
            form.file.errors.append(f"The file could not be converted. The error was: {e}")

    return render_template(
        'tools/unlock-file-locked-for-editing.html',
        form=form
    )


def get_filename_without_pdf_extension(input_file_name):
    if input_file_name.endswith('.pdf'):
        input_file_name_prefix = input_file_name[:(len(input_file_name) - 4)]
        return input_file_name_prefix
    else:
        return input_file_name

def make_pdf_download_response(pdf_bytes, output_file_name):
    response = make_response(pdf_bytes)
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename=output_file_name)
    return response
