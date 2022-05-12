from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, session, make_response
from grc.utils.decorators import AdminViewerRequired, AdminRequired
from grc.models import db, Application, ApplicationStatus
from grc.external_services.aws_s3_client import AwsS3Client
from grc.birth_registration.forms import AdoptedUKForm

applications = Blueprint('applications', __name__)


def get_radio_pretty_value(formName, fieldName, value):
    if formName == 'AdoptedUKForm':
        form = AdoptedUKForm()
    else:
        return None

    for choiceId, choiceLabel in form[fieldName].choices:
        if choiceId == value:
            return choiceLabel
    return None


@applications.route('/applications', methods=['GET'])
@AdminViewerRequired
def index():
    message = ""

    newApplications = Application.query.filter_by(
        status=ApplicationStatus.SUBMITTED
    )
    downloadedApplications = Application.query.filter_by(
        status=ApplicationStatus.DOWNLOADED
    )
    completedApplications = Application.query.filter_by(
        status=ApplicationStatus.COMPLETED
    )

    return render_template(
        'applications/applications.html',
        message=message,
        newApplications=newApplications,
        downloadedApplications=downloadedApplications,
        completedApplications=completedApplications
    )


@applications.route('/applications/<reference_number>', methods=['GET'])
@AdminViewerRequired
def view(reference_number):
    application = Application.query.filter_by(
        reference_number=reference_number
    ).first()

    return render_template(
        'applications/view-application.html',
        application=application,
        strptime=datetime.strptime,
        get_radio_pretty_value=get_radio_pretty_value
    )


@applications.route('/applications/<file_name>/downloadfile', methods=['GET'])
@AdminViewerRequired
def downloadfile(file_name):
    data = AwsS3Client().download_object(file_name)

    file_type = 'application/octet-stream'
    if '.' in file_name:
        file_type = file_name[file_name.rindex('.') + 1:]
        if file_type == 'pdf':
            file_type = 'application/pdf'
        elif file_type == 'jpg':
            file_type = 'image/jpeg'
        else:
            file_type = 'image/' + file_type

    response = make_response(data.getvalue())
    response.headers.set('Content-Type', file_type)
    return response


@applications.route('/applications/<reference_number>/download', methods=['GET'])
@AdminViewerRequired
def download(reference_number):
    message = ""

    application = Application.query.filter_by(
        reference_number=reference_number
    ).first()

    if application is None:
        message = "An application with that reference number cannot be found"
    else:
        application.status = ApplicationStatus.DOWNLOADED
        application.downloaded = datetime.now()
        application.downloadedBy = session['signedIn']
        db.session.commit()

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
        if 'medicalReports' in application.user_input and 'files' in application.user_input['medicalReports']:
            for object_name in application.user_input['medicalReports']['files']:
                add_pdf(object_name)

        if 'genderEvidence' in application.user_input and 'files' in application.user_input['genderEvidence']:
            for object_name in application.user_input['genderEvidence']['files']:
                add_pdf(object_name)

        if 'nameChange' in application.user_input and 'files' in application.user_input['nameChange']:
            for object_name in application.user_input['nameChange']['files']:
                add_pdf(object_name)

        if 'marriageDocuments' in application.user_input and 'files' in application.user_input['marriageDocuments']:
            for object_name in application.user_input['marriageDocuments']['files']:
                add_pdf(object_name)

        if 'overseasCertificate' in application.user_input and 'files' in application.user_input['overseasCertificate']:
            for object_name in application.user_input['overseasCertificate']['files']:
                add_pdf(object_name)

        if 'statutoryDeclarations' in application.user_input and 'files' in application.user_input['statutoryDeclarations']:
            for object_name in application.user_input['statutoryDeclarations']['files']:
                add_pdf(object_name)

        if len(pdfs) > 0:
            pdfs.insert(0, data)
            data = merge_pdfs(pdfs)

        response = make_response(data.read())
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'attachment', file_name=application.reference_number + '.pdf')
        return response

    session['message'] = message
    return redirect(url_for('applications.index', _anchor='downloaded'))


@applications.route('/applications/<reference_number>/completed', methods=['GET'])
@AdminRequired
def completed(reference_number):
    message = ""

    application = Application.query.filter_by(
        reference_number=reference_number
    ).first()

    if application is None:
        message = "An application with that reference number cannot be found"
    else:
        application.status = ApplicationStatus.COMPLETED
        application.completed = datetime.now()
        application.completedBy = session['signedIn']
        db.session.commit()
        message = "application updated"

    session['message'] = message
    return redirect(url_for('applications.index', _anchor='completed'))


@applications.route('/applications/<reference_number>/attachments', methods=['GET'])
@AdminViewerRequired
def attachments(reference_number):
    message = ""

    application = Application.query.filter_by(
        reference_number=reference_number
    ).first()

    if application is None:
        message = "An application with that reference number cannot be found"
    else:
        import io
        import zipfile

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'x', zipfile.ZIP_DEFLATED, False) as zipper:
            if 'medicalReports' in application.user_input and 'files' in application.user_input['medicalReports']:
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
                    zipper.writestr(object_name, data.getvalue())

        response = make_response(zip_buffer.getvalue())
        response.headers.set('Content-Type', 'application/zip')
        response.headers.set('Content-Disposition', 'attachment', filename=application.reference_number + '.zip')
        return response

    session['message'] = message
    return redirect(url_for('applications.index', _anchor='completed'))


@applications.route('/applications/<reference_number>/delete', methods=['GET'])
@AdminViewerRequired
def delete(reference_number):
    message = ""

    application = Application.query.filter_by(
        reference_number=reference_number
    ).first()

    if application is None:
        message = "An application with that reference number cannot be found"
    else:
        db.session.delete(application)
        db.session.commit()
        message = "application deleted"

    session['message'] = message
    return redirect(url_for('applications.index', _anchor='new'))
