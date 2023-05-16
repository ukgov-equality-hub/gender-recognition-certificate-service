from io import BytesIO
import os
import zipfile
from flask import render_template
from typing import Callable, List, Dict, Tuple
from grc.business_logic.data_structures.application_data import ApplicationData
from grc.business_logic.data_structures.uploads_data import UploadsData, EvidenceFile
from grc.external_services.aws_s3_client import AwsS3Client
from grc.utils.logger import LogLevel, Logger
from grc.utils.pdf_utils import PDFUtils

logger = Logger()


class ApplicationFiles():
    sections = ['medicalReports', 'genderEvidence', 'nameChange', 'marriageDocuments', 'overseasCertificate', 'statutoryDeclarations', 'birthOrAdoptionCertificate']
    section_names = ['Medical Reports', 'Gender Evidence', 'Name Change', 'Marriage Documents', 'Overseas Certificate', 'Statutory Declarations', 'Birth or adoption certificate']
    section_files:  Dict[str, Callable[[UploadsData], List[EvidenceFile]]] = {
        'medicalReports': (lambda u: u.medical_reports),
        'genderEvidence': (lambda u: u.evidence_of_living_in_gender),
        'nameChange': (lambda u: u.name_change_documents),
        'marriageDocuments': (lambda u: u.partnership_documents),
        'overseasCertificate': (lambda u: u.overseas_documents),
        'statutoryDeclarations': (lambda u: u.statutory_declarations),
        'birthOrAdoptionCertificate': (lambda u: u.birth_or_adoption_certificates),
    }


    def __init__(self):
        pass


    def get_files_for_section(self, section: str, application_data: ApplicationData) -> list:
        return self.section_files[section](application_data.uploads_data)


    def get_section_name(self, section: str) -> str:
        return self.section_names[self.sections.index(section)]


    def create_or_download_attachments(self, reference_number: str, application_data: ApplicationData, download: bool = False) -> Tuple[BytesIO, str]:
        bytes = None
        zip_file_file_name = ''

        try:
            zip_file_file_name = reference_number + '.zip'

            data = None if os.getenv('FLASK_ENV', '') == 'development' else AwsS3Client().download_object(zip_file_file_name)
            if data:
                if download:
                    bytes = data.getvalue()
            else:
                zip_buffer = BytesIO()

                with zipfile.ZipFile(zip_buffer, 'x', zipfile.ZIP_DEFLATED, False) as zipper:
                    for section in self.sections:
                        files = self.get_files_for_section(section, application_data)
                        for file_index, evidence_file in enumerate(files):
                            data = AwsS3Client().download_object(evidence_file.aws_file_name)
                            if data is not None:
                                attachment_file_name = f"{reference_number}__{section}__{(file_index + 1)}_{evidence_file.original_file_name}"
                                zipper.writestr(attachment_file_name, data.getvalue())

                            file_name, file_ext = self.get_filename_and_extension(evidence_file.aws_file_name)
                            if file_ext.lower() in ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp']:
                                data = AwsS3Client().download_object(f'{file_name}_original{file_ext}')
                                if data is not None:
                                    file_name, file_ext = self.get_filename_and_extension(evidence_file.original_file_name)
                                    attachment_file_name = f"{reference_number}__{section}__{(file_index + 1)}_{file_name}_original{file_ext}"
                                    zipper.writestr(attachment_file_name, data.getvalue())

                    data, _ = self.create_or_download_pdf(
                        reference_number,
                        application_data,
                        attach_files=False,
                        download=True,
                        create_toc=False,
                        paginate=False
                    )
                    zipper.writestr('application.pdf', data)

                bytes = zip_buffer.getvalue()
                AwsS3Client().upload_fileobj(zip_buffer, attachment_file_name)
                if not download:
                    bytes = None

        except Exception as e:
            logger.log(LogLevel.ERROR, e)

        return bytes, zip_file_file_name


    def create_or_download_pdf(self, reference_number: str, application_data: ApplicationData, is_admin: bool = True, attach_files: bool = True, download: bool = False, create_toc: bool = False, paginate: bool = False) -> Tuple[BytesIO, str]:
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
                all_sections = self.sections
                if is_admin:
                    all_sections = ['statutoryDeclarations', 'marriageDocuments', 'nameChange', 'medicalReports', 'genderEvidence', 'overseasCertificate']

                pdfs = []
                application_pdf = self.create_application_cover_sheet_pdf(application_data, is_admin)
                pdfs.append(application_pdf)

                if attach_files:
                    self.attach_all_files(pdfs, all_sections, application_data)

                else:
                    attachments_pdf = self.create_attachment_names_pdf(all_sections, application_data)
                    if attachments_pdf:
                        pdfs.append(attachments_pdf)

                output_pdf_document = PDFUtils().merge_pdfs(pdfs)
                if create_toc:
                    output_pdf_document = PDFUtils().create_pdf_toc(output_pdf_document)
                if paginate:
                    output_pdf_document = PDFUtils().paginate_pdf(output_pdf_document)

                bytes = output_pdf_document.read()
                if is_admin and not attach_files:
                    AwsS3Client().upload_fileobj(output_pdf_document, file_name)
                if not download:
                    bytes = None

        except Exception as e:
            logger.log(LogLevel.ERROR, e)

        return bytes, file_name


    def delete_application_files(self, reference_number: str, application_data: ApplicationData) -> None:
        AwsS3Client().delete_object(reference_number + '.zip')
        AwsS3Client().delete_object(reference_number + '.pdf')

        for section in self.sections:
            files = self.get_files_for_section(section, application_data)
            for evidence_file in files:
                AwsS3Client().delete_object(evidence_file.aws_file_name)


    def create_application_cover_sheet_pdf(self, application_data: ApplicationData, is_admin: bool) -> BytesIO:
        html_template = ('applications/download.html' if is_admin else 'applications/download_user.html')
        html = render_template(html_template, application_data=application_data)
        return PDFUtils().create_pdf_from_html(html, title='Application')


    def create_attachment_names_pdf(self, all_sections: list, application_data: ApplicationData) -> BytesIO:
        attachments_html = ''
        for section in all_sections:
            files = self.get_files_for_section(section, application_data)
            if len(files) > 0:
                attachments_html += f'<h3 style="font-size: 14px;">{self.get_section_name(section)}</h3>'
                for file_index, evidence_file in enumerate(files):
                    attachments_html += f'<p style="font-size: 12px;">Attachment {file_index + 1} of {len(files)}: {evidence_file.aws_file_name}</p>'

        if attachments_html != '':
            logger.log(LogLevel.INFO, "Adding attachments pdf")
            return PDFUtils().create_pdf_from_html(attachments_html, title='Attachments')


    def attach_all_files(self, pdfs: list, all_sections: list, application_data: ApplicationData) -> None:
        for section in all_sections:
            files = self.get_files_for_section(section, application_data)
            for file_index, evidence_file in enumerate(files):
                self.add_object(pdfs, section, evidence_file.aws_file_name, evidence_file.original_file_name)


    def add_object(self, pdfs, section: str, aws_file_name: str, original_file_name: str) -> None:
        if '.' in aws_file_name:
            file_type = aws_file_name[aws_file_name.rindex('.') + 1:].lower()

            if file_type == 'pdf':
                try:
                    data = AwsS3Client().download_object(aws_file_name)
                    if data is not None:
                        if PDFUtils().is_pdf_password_protected(data):
                            # We can check the type of password (user/owner):
                            # doc.authenticate('') == 2
                            # https://pymupdf.readthedocs.io/en/latest/document.html#Document.authenticate
                            html = f'<h3 style="font-size: 14px; color: red;">Unable to add {original_file_name}. A password is required.</h3>'
                            pdfs.append(PDFUtils().create_pdf_from_html(html, title=f'{self.get_section_name(section)}:{original_file_name}'))
                            logger.log(LogLevel.ERROR, f"file {aws_file_name} needs a password!")
                        else:
                            pdfs.append(PDFUtils().add_pdf_toc(data, f'{self.get_section_name(section)}:{original_file_name}'))
                            logger.log(LogLevel.INFO, f"Attaching {aws_file_name}")
                    else:
                        pdfs.append(self.create_pdf_for_attachment_error(section, original_file_name))
                        logger.log(LogLevel.ERROR, f"Error attaching {aws_file_name}")

                except Exception as e:
                    pdfs.append(self.create_pdf_for_attachment_error(section, original_file_name))
                    logger.log(LogLevel.ERROR, f"Error attaching {aws_file_name} ({e})")
            else:
                try:
                    data, width, height = AwsS3Client().download_object_data(aws_file_name)
                    if data is not None:
                        html = f'<img src="{data}" width="{width}" height="{height}" style="max-width: 90%;">'
                        pdfs.append(PDFUtils().create_pdf_from_html(html, title=f'{self.get_section_name(section)}:{original_file_name}'))
                        logger.log(LogLevel.INFO, f"Adding image {aws_file_name}")
                    else:
                        pdfs.append(self.create_pdf_for_attachment_error(section, original_file_name))
                        logger.log(LogLevel.ERROR, f"Error downloading {aws_file_name}")

                except Exception as e:
                    self.create_pdf_for_attachment_error(section, original_file_name)
                    logger.log(LogLevel.ERROR, f"Error attaching {aws_file_name} ({e})")
        else:
            logger.log(LogLevel.ERROR, f"Error attaching {aws_file_name}")
            self.create_pdf_for_attachment_error(section, original_file_name)


    def create_pdf_for_attachment_error(self, section: str, file_name: str) -> BytesIO:
        html = f'<h3 style="font-size: 14px; color: red;">WARNING: Could not attach file ({file_name})</h3>'
        return PDFUtils().create_pdf_from_html(html, title=f'{self.get_section_name(section)}:{file_name}')


    def get_filename_and_extension(self, file_name: str) -> str:
        file_ext = ''
        if '.' in file_name:
            file_ext = file_name[file_name.rindex('.'):]
            file_name = file_name[0: file_name.rindex('.')]

        return file_name, file_ext
