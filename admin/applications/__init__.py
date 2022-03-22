from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, session
)
from flask import render_template
from flask_weasyprint import HTML, render_pdf
from grc.utils.decorators import AdminViewerRequired
from grc.models import db, Application, ApplicationStatus

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


@applications.route('/applications/<emailAddress>/download', methods=['GET'])
@AdminViewerRequired
def download(emailAddress):
    message = ""

    application = Application.query.filter_by(
        email=emailAddress
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
        redirect(url_for('applications.index', _anchor='downloaded'))
        return render_pdf(HTML(string=html))

    session['message'] = message
    return redirect(url_for('applications.index', _anchor='downloaded'))


@applications.route('/applications/<emailAddress>/completed', methods=['GET'])
@AdminViewerRequired
def completed(emailAddress):
    message = ""

    application = Application.query.filter_by(
        email=emailAddress
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
