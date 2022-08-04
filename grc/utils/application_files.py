import fitz  # PyPDF2
import io
import os
import zipfile
from flask import render_template
from xhtml2pdf import pisa
from typing import Callable, List, Dict
from grc.business_logic.data_structures.application_data import ApplicationData
from grc.business_logic.data_structures.uploads_data import UploadsData, EvidenceFile
from grc.external_services.aws_s3_client import AwsS3Client
from grc.utils.logger import LogLevel, Logger

logger = Logger()


class ApplicationFiles():
    def __init__(self):
        self.sections = ['medicalReports', 'genderEvidence', 'nameChange', 'marriageDocuments', 'overseasCertificate', 'statutoryDeclarations']
        self.section_names = ['Medical Reports', 'Gender Evidence', 'Name Change', 'Marriage Documents', 'Overseas Certificate', 'Statutory Declarations']
        self.section_files:  Dict[str, Callable[[UploadsData], List[EvidenceFile]]] = {
            'medicalReports': (lambda u: u.medical_reports),
            'genderEvidence': (lambda u: u.evidence_of_living_in_gender),
            'nameChange': (lambda u: u.name_change_documents),
            'marriageDocuments': (lambda u: u.partnership_documents),
            'overseasCertificate': (lambda u: u.overseas_documents),
            'statutoryDeclarations': (lambda u: u.statutory_declarations),
        }

    def create_or_download_attachments(self, reference_number, application_data: ApplicationData, download=False):
        bytes = None
        zip_file_file_name = ''

        try:
            zip_file_file_name = reference_number + '.zip'

            data = None if os.getenv('FLASK_ENV', '') == 'development' else AwsS3Client().download_object(zip_file_file_name)
            if data:
                if download:
                    bytes = data.getvalue()
            else:
                zip_buffer = io.BytesIO()

                with zipfile.ZipFile(zip_buffer, 'x', zipfile.ZIP_DEFLATED, False) as zipper:
                    for section in self.sections:
                        files = self.section_files[section](application_data.uploads_data)
                        for file_index, evidence_file in enumerate(files):
                            data = AwsS3Client().download_object(evidence_file.aws_file_name)
                            if data is not None:
                                file_name_parts = evidence_file.aws_file_name.split('__')
                                file_name_parts[2] = f"{(file_index + 1)}_{file_name_parts[2]}"
                                attachment_file_name = '__'.join(file_name_parts)
                                zipper.writestr(attachment_file_name, data.getvalue())

                    data, _ = self.create_or_download_pdf(reference_number, application_data, attach_files=False, download=True)
                    zipper.writestr('application.pdf', data)

                bytes = zip_buffer.getvalue()
                AwsS3Client().upload_fileobj(zip_buffer, attachment_file_name)
                if not download:
                    bytes = None

        except Exception as e:
            logger.log(LogLevel.ERROR, e)

        return bytes, zip_file_file_name


    def create_or_download_pdf(self, reference_number, application_data: ApplicationData, is_admin=True, attach_files=True, download=False):
        bytes = None
        file_name = ''

        try:
            file_name = reference_number + '.pdf' if is_admin else 'grc_' + str(application_data.email_address).replace('@', '_').replace('.', '_') + '.pdf'

            data = None
            if is_admin and not attach_files:
                data = None if os.getenv('FLASK_ENV', '') == 'development' else AwsS3Client().download_object(file_name)
            if data:
                if download:
                    bytes = data.getvalue()
            else:
                html_template = 'applications/download_user.html'
                all_sections = self.sections
                if is_admin:
                    html_template = 'applications/download.html'
                    all_sections = ['statutoryDeclarations', 'marriageDocuments', 'nameChange', 'medicalReports', 'genderEvidence', 'overseasCertificate']

                html = render_template(html_template, application_data=application_data)
                pdfs = []
                object_names = []
                attachments_html = ''

                data = io.BytesIO()
                pisa.CreatePDF(html, dest=data)
                data.seek(0)

                # Attach any PDF's
                def html_to_pdf(html):
                    pdf = io.BytesIO()
                    pisa.CreatePDF(html, dest=pdf)
                    pdf.seek(0)
                    return pdf

                def merge_pdfs(pdfs):
                    #merger = PyPDF2.PdfFileMerger(strict=False)
                    #for pdf_fileobj in pdfs:
                    #    merger.append(pdf_fileobj)

                    merger = fitz.open()
                    for pdf_fileobj in pdfs:
                        doc = fitz.open(stream=pdf_fileobj, filetype='pdf')
                        merger.insert_pdf(doc)

                    pdf = io.BytesIO()
                    merger.save(pdf, deflate=True)
                    merger.close()
                    pdf.seek(0)
                    return pdf

                def add_object(section, object_name, idx, num):
                    file_type = ''

                    def section_name():
                        return self.section_names[self.sections.index(section)]

                    def clean_object_name():
                        new_name = object_name
                        new_name = new_name[len(reference_number):]
                        new_name = str(new_name).replace(f'__{section}__', '')
                        return new_name

                    if '.' in object_name:
                        file_type = object_name[object_name.rindex('.') + 1:]

                        if file_type.lower() == 'pdf':
                            html = f'<p style="font-size: 12px;">Next page: Attachment {idx} of {num} - {clean_object_name()}</p>'
                            if idx == 1:
                                html = f'<h3 style="font-size: 14px;">Your {section_name()}</h3>{html}'
                            object_names.append(f'{object_name} header file')

                            data = AwsS3Client().download_object(object_name)
                            if data is not None:
                                doc = fitz.open(stream=data, filetype='pdf')
                                if doc.needs_pass:

                                    # We can check the type of password (user/owner):
                                    # doc.authenticate('') == 2
                                    # https://pymupdf.readthedocs.io/en/latest/document.html#Document.authenticate
                                    html += f'<h3 style="font-size: 14px; color: red;">Unable to add {clean_object_name()}. A password is required.</h3>'
                                    pdf = html_to_pdf(html)
                                    pdfs.append(pdf)
                                    logger.log(LogLevel.ERROR, f"file {object_name} needs a password!")
                                else:
                                    pdf = html_to_pdf(html)
                                    pdfs.append(pdf)
                                    pdfs.append(data)
                                    object_names.append(object_name)
                                    logger.log(LogLevel.INFO, f"Attaching {object_name}")
                            else:
                                logger.log(LogLevel.ERROR, f"Error attaching {object_name}")
                        else:
                            data, width, height = AwsS3Client().download_object_data(object_name)
                            pdf = io.BytesIO()
                            if data is not None:
                                html = f'<p style="font-size: 12px;">Attachment {idx} of {num} - {clean_object_name()}</p><p>&nbsp;</p><p>&nbsp;</p><img src="{data}" width="{width}" height="{height}" style="max-width: 90%;">'
                            else:
                                html = f'<p style="font-size: 12px;">Attachment {idx} of {num} - {clean_object_name()}</p><p>&nbsp;</p><p>&nbsp;</p><p>Error downloading file, please try again later</p>'
                                logger.log(LogLevel.ERROR, f"Error downloading {object_name}")

                            if idx == 1:
                                html = f'<h3 style="font-size: 14px;">Your {section_name()}</h3>{html}'

                            pisa.CreatePDF(html, dest=pdf)
                            pdf.seek(0)
                            pdfs.append(pdf)
                            object_names.append(object_name)
                            logger.log(LogLevel.INFO, f"Adding image {object_name}")

                for section in all_sections:
                    files = self.section_files[section](application_data.uploads_data)
                    title = False
                    num_attachments = len(files)
                    for file_index, evidence_file in enumerate(files):
                        if attach_files:
                            add_object(section, evidence_file.aws_file_name, file_index + 1, num_attachments)
                        else:
                            if not title:
                                attachments_html += f'<h3 style="font-size: 14px;">{self.section_names[self.sections.index(section)]}</h3>'
                                title = True
                            attachments_html += f'<p style="font-size: 12px;">Attachment {file_index + 1} of {num_attachments}: {evidence_file.aws_file_name}</p>'

                if attachments_html != '':
                    pdf = io.BytesIO()
                    pisa.CreatePDF(attachments_html, dest=pdf)
                    pdf.seek(0)
                    pdfs.append(pdf)
                    object_names.append('')
                    logger.log(LogLevel.INFO, "Adding attachments pdf")

                if len(pdfs) > 0:
                    pdfs.insert(0, data)
                    object_names.insert(0, '')
                    data = merge_pdfs(pdfs)

                bytes = data.read()
                if is_admin and not attach_files:
                    AwsS3Client().upload_fileobj(data, file_name)
                if not download:
                    bytes = None

        except Exception as e:
            logger.log(LogLevel.ERROR, e)

        return bytes, file_name


    def delete_application_files(self, reference_number, application_data: ApplicationData):
        AwsS3Client().delete_object(reference_number + '.zip')
        AwsS3Client().delete_object(reference_number + '.pdf')

        for section in self.sections:
            files = self.section_files[section](application_data.uploads_data)
            for evidence_file in files:
                AwsS3Client().delete_object(evidence_file.aws_file_name)
