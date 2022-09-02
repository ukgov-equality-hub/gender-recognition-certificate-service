import fitz
import io
from flask import Blueprint, render_template, make_response, request
from admin.tools.forms import UnlockFileForm
from grc.utils.decorators import AdminViewerRequired
from grc.utils.logger import Logger, LogLevel

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
        try:
            input_pdf_file = fitz.open(stream=file.read(), filetype='pdf')

            if input_pdf_file.needs_pass:
                if form.pdf_password.data:
                    if not input_pdf_file.authenticate(form.pdf_password.data):
                        form.pdf_password.errors.append('The password was incorrect. You will also need to select the file again')
                else:
                    form.file.errors.append("This file is password protected. Enter the password. You will also need to select the file again")

            if not form.errors:
                pdf_bytes = unlock_pdf(input_pdf_file)

                input_file_name_prefix = get_filename_without_extension(file.filename)
                output_file_name = f"{input_file_name_prefix} (unlocked).pdf"

                return make_pdf_download_response(pdf_bytes, output_file_name)

        except Exception as e:
            logger.log(LogLevel.ERROR, f"File could not be converted. Error was {e}")
            form.file.errors.append(f"The file could not be converted. The error was: {e}")

    return render_template(
        'tools/unlock-file-locked-for-editing.html',
        form=form
    )


def unlock_pdf(input_pdf_file):
    output_pdf_file = fitz.open()
    output_pdf_file.insert_pdf(input_pdf_file)

    pdf_stream = io.BytesIO()
    output_pdf_file.save(pdf_stream, deflate=True)
    output_pdf_file.close()

    pdf_stream.seek(0)
    pdf_bytes = pdf_stream.read()
    return pdf_bytes


def get_filename_without_extension(input_file_name):
    last_dot_in_input_filename = input_file_name.rindex('.')
    input_file_name_prefix = input_file_name[:last_dot_in_input_filename]
    return input_file_name_prefix


def make_pdf_download_response(pdf_bytes, output_file_name):
    response = make_response(pdf_bytes)
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename=output_file_name)
    return response
