from datetime import datetime
from flask import Blueprint, abort, render_template, url_for, session, make_response, request
from admin.applications.forms import SearchForm, ReferenceNumberForm
from grc.business_logic.data_store import DataStore
from grc.utils.decorators import AdminViewerRequired, AdminRequired
from grc.models import db, Application, ApplicationStatus
from grc.external_services.aws_s3_client import AwsS3Client
from grc.utils.redirect import local_redirect
from grc.utils.logger import LogLevel, Logger
from grc.utils.reference_number import validate_reference_number
from sqlalchemy import or_

applications = Blueprint('applications', __name__)
logger = Logger()


@applications.route('/applications', methods=['GET'])
@AdminViewerRequired
def index():
    message = ""

    newApplications = Application.query.filter_by(
        status=ApplicationStatus.SUBMITTED
    ).order_by(Application.updated.desc())

    downloadedApplications = Application.query.filter_by(
        status=ApplicationStatus.DOWNLOADED
    ).order_by(Application.updated.desc())

    downloaded_apps_references = [application.reference_number for application in downloadedApplications]

    completedApplications = Application.query.filter_by(
        status=ApplicationStatus.COMPLETED
    ).order_by(Application.updated.desc())

    logger.log(LogLevel.INFO, f"{logger.mask_email_address(session['signedIn'])} accessed all applications")

    return render_template(
        'applications/applications.html',
        message=message,
        newApplications=newApplications,
        downloadedApplications=downloadedApplications,
        downloaded_apps_references=downloaded_apps_references,
        completedApplications=completedApplications
    )


@applications.route('/applications/search', methods=['GET', 'POST'])
@AdminViewerRequired
def search():
    form = SearchForm()
    message = ""
    search = ""
    applications = []

    if request.method == 'POST' and form.search.data:
        search = form.search.data.lower()
        all_applications = db.session.query(Application).filter(or_(
            Application.status == ApplicationStatus.COMPLETED, Application.status == ApplicationStatus.SUBMITTED,
            Application.status == ApplicationStatus.DOWNLOADED
        ))
        for application in all_applications:
            if search in application.reference_number.lower():
                applications.append(application)
            elif search in application.email.lower():
                applications.append(application)
            else:
                data = application.application_data()
                try:
                    add_application = False

                    if hasattr(data, 'personal_details_data'):
                        if hasattr(data.personal_details_data, 'first_name') and search in data.personal_details_data.first_name.lower():
                            add_application = True
                        elif hasattr(data.personal_details_data, 'middle_names_or_empty_string') and search in data.personal_details_data.middle_names_or_empty_string.lower():
                            add_application = True
                        elif hasattr(data.personal_details_data, 'last_name') and search in data.personal_details_data.last_name.lower():
                            add_application = True

                    if hasattr(data, 'birth_registration_data'):
                        if hasattr(data.birth_registration_data,'first_name' ) and search in data.birth_registration_data.first_name.lower():
                            add_application = True
                        elif hasattr(data.birth_registration_data, 'middle_names') and search in data.birth_registration_data.middle_names.lower():
                            add_application = True
                        elif hasattr(data.birth_registration_data, 'last_name') and search in data.birth_registration_data.last_name.lower():
                            add_application = True

                    if add_application:
                        applications.append(application)

                except TypeError as e:
                    pass

    return render_template(
        'applications/search.html',
        form=form,
        message=message,
        search=search,
        applications=applications
    )


@applications.route('/applications/search-by-reference-number', methods=['POST'])
@AdminViewerRequired
def search_by_reference_number():
    form = ReferenceNumberForm()

    if form.reference_number.data:
        if validate_reference_number(form.reference_number.data):
            reference_number = form.reference_number.data.replace('-', '').replace(' ', '').upper()
            return local_redirect(url_for('applications.view', reference_number=reference_number))

    return render_template(
        'applications/reference-number-not-found.html',
        reference_number_text=form.reference_number.data
    )


@applications.route('/applications/<reference_number>', methods=['GET'])
@AdminViewerRequired
def view(reference_number):
    application_data = DataStore.load_application(reference_number)

    logger.log(LogLevel.INFO, f"{logger.mask_email_address(session['signedIn'])} accessed application {reference_number}")

    return render_template(
        'applications/view-application.html',
        application_data=application_data
    )


@applications.route('/applications/<file_name>/downloadfile', methods=['GET'])
@AdminViewerRequired
def downloadfile(file_name):
    data = AwsS3Client().download_object(file_name)
    if data is None:
        return abort(503)

    file_type = 'application/octet-stream'
    if '.' in file_name:
        file_type = file_name[file_name.rindex('.') + 1:].lower()
        if file_type == 'pdf':
            file_type = 'application/pdf'
        elif file_type == 'jpg':
            file_type = 'image/jpeg'
        else:
            file_type = 'image/' + file_type

    logger.log(LogLevel.INFO, f"{logger.mask_email_address(session['signedIn'])} downloaded file {file_name}")

    bytes = data.getvalue()
    if bytes is None:
        return abort(404)

    response = make_response(bytes)
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
        logger.log(LogLevel.INFO, f"{logger.mask_email_address(session['signedIn'])} attempted to download application {reference_number} which cannot be found")
    else:
        application.status = ApplicationStatus.DOWNLOADED
        application.downloaded = datetime.now()
        application.downloadedBy = session['signedIn']
        db.session.commit()

        from grc.utils.application_files import ApplicationFiles
        bytes, file_name = ApplicationFiles().create_or_download_pdf(
            application.reference_number,
            application.application_data(),
            download=True,
            create_toc=False,
            paginate=False
        )

        logger.log(LogLevel.INFO, f"{logger.mask_email_address(session['signedIn'])} downloaded application {reference_number}")

        if bytes is None:
            return abort(404)

        response = make_response(bytes)
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'attachment', filename=file_name)
        return response

    session['message'] = message
    return local_redirect(url_for('applications.index', _anchor='downloaded'))


@applications.route('/applications/completed', methods=['POST'])
@AdminRequired
def completed():
    if request.form:
        references = [reference for reference in request.form]
        applications_to_mark_as_completed = db.session.query(Application).filter(
            Application.reference_number.in_(references)).all()

        if applications_to_mark_as_completed:
            for application in applications_to_mark_as_completed:
                application.status = ApplicationStatus.COMPLETED
                application.completed = datetime.now()
                application.completedBy = session['signedIn']
                db.session.commit()
                message = "application updated"
                logger.log(LogLevel.INFO,
                           f"{logger.mask_email_address(session['signedIn'])}"
                           f" completed application {application.reference_number}")
                session['message'] = message
            return local_redirect(url_for('applications.index', _anchor='completed'))

    print('No applications to mark as completed', flush=True)
    return local_redirect(url_for('applications.index', _anchor='downloaded'))


@applications.route('/applications/<reference_number>/attachments', methods=['GET'])
@AdminViewerRequired
def attachments(reference_number):
    message = ""

    application = Application.query.filter_by(
        reference_number=reference_number
    ).first()

    if application is None:
        message = "An application with that reference number cannot be found"
        logger.log(LogLevel.INFO, f"{logger.mask_email_address(session['signedIn'])} attempted to download files for application {reference_number} which cannot be found")
    else:
        from grc.utils.application_files import ApplicationFiles
        bytes, file_name = ApplicationFiles().create_or_download_attachments(
            application.reference_number,
            application.application_data(),
            download=True
        )

        logger.log(LogLevel.INFO, f"{logger.mask_email_address(session['signedIn'])} downloaded files for application {reference_number}")

        session['message'] = "attachments zipped"
        if bytes is None:
            return abort(404)

        response = make_response(bytes)
        response.headers.set('Content-Type', 'application/zip')
        response.headers.set('Content-Disposition', 'attachment', filename=file_name)
        return response

    session['message'] = message
    return local_redirect(url_for('applications.index', _anchor='completed'))


@applications.route('/applications/<reference_number>/delete', methods=['GET'])
@AdminViewerRequired
def delete(reference_number):
    message = ""

    application = Application.query.filter_by(
        reference_number=reference_number
    ).first()

    if application is None:
        message = "An application with that reference number cannot be found"
        logger.log(LogLevel.INFO, f"{logger.mask_email_address(session['signedIn'])} attempted to delete application {reference_number} which cannot be found")
    else:
        db.session.delete(application)
        db.session.commit()
        message = "application deleted"

        logger.log(LogLevel.INFO, f"{logger.mask_email_address(session['signedIn'])} deleted application {reference_number}")

    session['message'] = message
    return local_redirect(url_for('applications.index', _anchor='new'))
