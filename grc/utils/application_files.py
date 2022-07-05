from grc.external_services.aws_s3_client import AwsS3Client


class ApplicationFiles():
    def __init__(self):
        self.sections = ['medicalReports', 'genderEvidence', 'nameChange', 'marriageDocuments', 'overseasCertificate', 'statutoryDeclarations']
        self.section_names = ['Medical Reports', 'Gender Evidence', 'Name Change', 'Marriage Documents', 'Overseas Certificate', 'Statutory Declarations']


    def create_or_download_attachments(self, reference_number, application, download=False):
        bytes = None
        file_name = ''

        try:
            file_name = reference_number + '.zip'

            data = AwsS3Client().download_object(file_name)
            if data:
                if download:
                    bytes = data.getvalue()
            else:
                import io
                import zipfile

                zip_buffer = io.BytesIO()

                with zipfile.ZipFile(zip_buffer, 'x', zipfile.ZIP_DEFLATED, False) as zipper:
                    for section in self.sections:
                        if section in application and 'files' in application[section]:
                            for object_name in application[section]['files']:
                                data = AwsS3Client().download_object(object_name)
                                zipper.writestr(object_name, data.getvalue())

                bytes = zip_buffer.getvalue()
                AwsS3Client().upload_fileobj(zip_buffer, file_name)
                if not download:
                    bytes = None

        except Exception as e:
            print(e, flush=True)

        return bytes, file_name


    def create_or_download_pdf(self, reference_number, application, is_admin=True, download=False):
        bytes = None
        file_name = ''

        try:
            file_name = reference_number + '.pdf'

            data = AwsS3Client().download_object(file_name)
            if data:
                if download:
                    bytes = data.getvalue()
            else:
                from flask import render_template
                html_template = 'applications/download.html' if is_admin else 'applications/download_user.html'
                html = render_template(html_template, application=application)

                import io
                import PyPDF2
                from xhtml2pdf import pisa
                data = io.BytesIO()
                pisa.CreatePDF(html, dest=data)
                data.seek(0)

                # Attach any PDF's
                def merge_pdfs(pdfs):
                    import io
                    merger = PyPDF2.PdfFileMerger()
                    for pdf_fileobj in pdfs:
                        merger.append(pdf_fileobj)

                    pdf = io.BytesIO()
                    merger.write(pdf)
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
                            pdf = io.BytesIO()
                            html = f'<p style="font-size: 12px;">Next page: Attachment {idx} of {num} - {clean_object_name()}</p>'
                            if idx == 1:
                                html = f'<h3 style="font-size: 14px;">Your {section_name()}</h3>{html}'

                            pisa.CreatePDF(html, dest=pdf)
                            pdf.seek(0)
                            pdfs.append(pdf)

                            data = AwsS3Client().download_object(object_name)
                            pdfs.append(data)
                            print('Attaching ' + object_name)
                        else:
                            data, width, height = AwsS3Client().download_object_data(object_name)
                            pdf = io.BytesIO()
                            html = f'<p style="font-size: 12px;">Attachment {idx} of {num} - {clean_object_name()}</p><p>&nbsp;</p><p>&nbsp;</p><img src="{data}" width="{width}" height="{height}" style="max-width: 90%;">'
                            if idx == 1:
                                html = f'<h3 style="font-size: 14px;">Your {section_name()}</h3>{html}'

                            pisa.CreatePDF(html, dest=pdf)
                            pdf.seek(0)
                            pdfs.append(pdf)
                            print('Adding image ' + object_name)

                pdfs = []

                for section in self.sections:
                    if section in application and 'files' in application[section]:
                        for idx, object_name in enumerate(application[section]['files']):
                            add_object(section, object_name, idx + 1, len(application[section]['files']))

                if len(pdfs) > 0:
                    pdfs.insert(0, data)
                    data = merge_pdfs(pdfs)

                bytes = data.read()
                AwsS3Client().upload_fileobj(data, file_name)
                if not download:
                    bytes = None

        except Exception as e:
            print(e, flush=True)

        return bytes, file_name


    def delete_application_files(self, reference_number, application):
        AwsS3Client().delete_object(reference_number + '.zip')
        AwsS3Client().delete_object(reference_number + '.pdf')

        for section in self.sections:
            if section in application and 'files' in application[section]:
                for object_name in application[section]['files']:
                    AwsS3Client().delete_object(object_name)
