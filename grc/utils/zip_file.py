from grc.external_services.aws_s3_client import AwsS3Client

def create_or_download_attachments(application, download=False):
    print('')
    bytes = None
    file_name = ''

    try:
        file_name = application.reference_number + '.zip'

        data = AwsS3Client().download_object(file_name)
        if data:
            if download:
               bytes = data.getvalue()
        else:
            import io
            import zipfile

            zip_buffer = io.BytesIO()
            sections = ['medicalReports', 'genderEvidence', 'nameChange', 'marriageDocuments', 'overseasCertificate', 'statutoryDeclarations']

            with zipfile.ZipFile(zip_buffer, 'x', zipfile.ZIP_DEFLATED, False) as zipper:
                for section in sections:
                    if section in application.user_input and 'files' in application.user_input[section]:
                        for object_name in application.user_input[section]['files']:
                            data = AwsS3Client().download_object(object_name)
                            zipper.writestr(object_name, data.getvalue())

                '''if 'medicalReports' in application.user_input and 'files' in application.user_input['medicalReports']:
                    for object_name in application.user_input['medicalReports']['files']:
                        data = AwsS3Client().download_object(object_name)
                        zipper.writestr(object_name, data.getvalue())

                if 'genderEvidence' in application.user_input and 'files' in application.user_input['genderEvidence']:
                    for object_name in application.user_input['genderEvidence']['files']:
                        data = AwsS3Client().download_object(object_name)
                        zipper.writestr(object_name, data.getvalue())

                if 'nameChange' in application.user_input and 'files' in application.user_input['nameChange']:
                    for object_name in application.user_input['nameChange']['files']:
                        data = AwsS3Client().download_object(object_name)
                        zipper.writestr(object_name, data.getvalue())

                if 'marriageDocuments' in application.user_input and 'files' in application.user_input['marriageDocuments']:
                    for object_name in application.user_input['marriageDocuments']['files']:
                        data = AwsS3Client().download_object(object_name)
                        zipper.writestr(object_name, data.getvalue())

                if 'overseasCertificate' in application.user_input and 'files' in application.user_input['overseasCertificate']:
                    for object_name in application.user_input['overseasCertificate']['files']:
                        data = AwsS3Client().download_object(object_name)
                        zipper.writestr(object_name, data.getvalue())

                if 'statutoryDeclarations' in application.user_input and 'files' in application.user_input['statutoryDeclarations']:
                    for object_name in application.user_input['statutoryDeclarations']['files']:
                        data = AwsS3Client().download_object(object_name)
                        zipper.writestr(object_name, data.getvalue())'''

                bytes = zip_buffer.getvalue()
                AwsS3Client().upload_fileobj(bytes, file_name)
                if not download:
                    bytes = None

    except Exception as e:
        print(e, flush=True)

    return bytes, file_name
