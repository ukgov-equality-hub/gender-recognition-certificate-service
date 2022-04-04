from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, session, make_response
)
from flask import render_template
from grc.utils.decorators import AdminViewerRequired
from grc.models import db, Application, ApplicationStatus
from grc.utils.s3 import download_object

applications = Blueprint('applications', __name__)


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
        'applications.html',
        message=message,
        newApplications=newApplications,
        downloadedApplications=downloadedApplications,
        completedApplications=completedApplications
    )


@applications.route('/applications/<file_name>/downloadfile', methods=['GET'])
@AdminViewerRequired
def downloadfile(file_name):
    data = download_object(file_name)

    file_type = 'application/octet-stream'
    if '.' in file_name:
        file_type = file_name[file_name.rindex('.') + 1:]
        if file_type == 'pdf':
            file_type = 'application/pdf'
        elif file_type == 'jpg':
            file_type == 'image/jpeg'
        else:
            file_type = 'image/' + file_type

    response = make_response(data.getvalue())
    response.headers.set('Content-Type', file_type)
    # response.headers.set('Content-Disposition', 'attachment', file_name=file_name)
    return response


@applications.route('/applications/<email_address>/download', methods=['GET'])
@AdminViewerRequired
def download(email_address):
    message = ""

    application = Application.query.filter_by(
        email=email_address
    ).first()

    if application is None:
        message = "An application with that email address cannot be found"
    else:
        application.status = ApplicationStatus.DOWNLOADED
        application.downloaded = datetime.now()
        application.downloadedBy = session['signedIn']
        db.session.commit()
        message = "application updated"

        html = render_template('download.html', application=application)
        #import pdfkit
        #from flask_weasyprint import HTML, render_pdf
        #redirect(url_for('applications.index', _anchor='downloaded'))
        #return render_pdf(HTML(string=html))  # pdfkit.from_string(html)

        import io
        from xhtml2pdf import pisa
        data = io.BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=data)
        data.seek(0)
        #return data.read()

        response = make_response(data.read())
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'attachment', file_name=application.reference_number + '.pdf')
        return response

    session['message'] = message
    return redirect(url_for('applications.index', _anchor='downloaded'))


@applications.route('/applications/<email_address>/completed', methods=['GET'])
@AdminViewerRequired
def completed(email_address):
    message = ""

    application = Application.query.filter_by(
        email=email_address
    ).first()

    if application is None:
        message = "An application with that email address cannot be found"
    else:
        application.status = ApplicationStatus.COMPLETED
        application.completed = datetime.now()
        application.completedBy = session['signedIn']
        db.session.commit()
        message = "application updated"

    session['message'] = message
    return redirect(url_for('applications.index', _anchor='completed'))


@applications.route('/applications/<email_address>/delete', methods=['GET'])
@AdminViewerRequired
def delete(email_address):
    message = ""

    application = Application.query.filter_by(
        email=email_address
    ).first()

    if application is None:
        message = "An application with that email address cannot be found"
    else:
        db.session.delete(application)
        db.session.commit()
        message = "application deleted"

    session['message'] = message
    return redirect(url_for('applications.index', _anchor='new'))
