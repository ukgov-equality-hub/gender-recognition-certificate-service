from grc.external_services.aws_s3_client import AwsS3Client


class ApplicationFiles():
    def __init__(self):
        self.sections = ['medicalReports', 'genderEvidence', 'nameChange', 'marriageDocuments', 'overseasCertificate', 'statutoryDeclarations']


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


    def create_or_download_pdf(self, reference_number, application, download=False):
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
                html = render_template('applications/download.html', application=application)

                import io
                from xhtml2pdf import pisa
                data = io.BytesIO()
                pisa_status = pisa.CreatePDF(html, dest=data)
                data.seek(0)

                # Attach any PDF's
                def merge_pdfs(pdfs):
                    import io
                    import PyPDF2
                    merger = PyPDF2.PdfFileMerger()
                    for pdf_fileobj in pdfs:
                        merger.append(pdf_fileobj)

                    pdf = io.BytesIO()
                    merger.write(pdf)
                    merger.close()
                    pdf.seek(0)
                    return pdf

                def add_pdf(object_name):
                    file_type = ''
                    if '.' in object_name:
                        file_type = object_name[object_name.rindex('.') + 1:]
                        if file_type.lower() == 'pdf':
                            data = AwsS3Client().download_object(object_name)
                            pdfs.append(data)
                            print('Attaching ' + object_name)

                pdfs = []

                for section in self.sections:
                    if section in application and 'files' in application[section]:
                        for object_name in application[section]['files']:
                            add_pdf(object_name)

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
