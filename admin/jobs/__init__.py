from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import Blueprint, request
from sqlalchemy.sql import extract
from grc.utils.decorators import JobTokenRequired
from grc.models import db, Application, ApplicationStatus, SecurityCode
from grc.utils.application_files import ApplicationFiles
from grc.external_services.gov_uk_notify import GovUkNotify

jobs = Blueprint('jobs', __name__)


@jobs.route('/jobs', methods=['GET'])
def index():
    return ('', 200)


@jobs.route('/jobs/create-files', methods=['GET'])
@JobTokenRequired
# https://stackoverflow.com/questions/70791034/how-to-ssh-into-a-container-in-which-a-task-is-running
def create_files():
    applications = Application.query.filter_by(
        status=ApplicationStatus.SUBMITTED,
        filesCreated=False
    )

    for application in applications:
        print('Creating attachments zipfile for application %s' % application.reference_number, flush=True)
        ApplicationFiles().create_or_download_attachments(
            application.reference_number,
            application.data(),
            download=False
        )
        print('Creating pdf for application %s' % application.reference_number, flush=True)
        ApplicationFiles().create_or_download_pdf(
            application.reference_number,
            application.data(),
            download=False
        )

        application.filesCreated = True
        db.session.commit()

    return ('', 200)


@jobs.route('/jobs/backup-db', methods=['GET'])
@JobTokenRequired
def backup_db():
    return ('', 200)


@jobs.route('/jobs/application-notifications', methods=['GET'])
@JobTokenRequired
def application_notifications():

    # Deletion after not logging in for six months
    updated = False
    dt = datetime.today() + relativedelta(days=-183)
    applications = Application.query.filter(
        Application.status == ApplicationStatus.STARTED,
        extract('day', Application.updated) == dt.day,
        extract('month', Application.updated) == dt.month,
        extract('year', Application.updated) == dt.year
    )

    for application in applications:
        ApplicationFiles().delete_application_files(
            application.reference_number,
            application.data(),
        )
        application.email = ''
        application.user_input = ''
        updated = True

    if updated:
        db.session.commit()

    # Reminders 3 months, 1 month & 1 week before deletion
    for expiry in ['3 months', '1 month', '1 week']:
        dt = datetime.today() + relativedelta(days=-(int(expiry[: expiry.index(' ')]) * 30))
        if expiry[expiry.index(' ') + 1:] == 'week':
            dt = datetime.today() + relativedelta(days=-7)

        applications = Application.query.filter(
            Application.status == ApplicationStatus.STARTED,
            extract('day', Application.updated) == dt.day,
            extract('month', Application.updated) == dt.month,
            extract('year', Application.updated) == dt.year
        )

        for application in applications:
            GovUkNotify().send_email_unfinished_application(
                email_address=application.email,
                expiry_days=expiry,
                grc_return_link=request.host_url
            )

    # Completed applications
    updated = False
    dt = datetime.today() + relativedelta(days=-7)
    applications = Application.query.filter(
        Application.status == ApplicationStatus.COMPLETED,
        extract('day', Application.completed) == dt.day,
        extract('month', Application.completed) == dt.month,
        extract('year', Application.completed) == dt.year
    )

    for application in applications:
        ApplicationFiles().delete_application_files(
            application.reference_number,
            application.data(),
        )
        application.email = ''
        application.user_input = ''
        updated = True

    if updated:
        db.session.commit()

    # Delete security codes
    dt = datetime.today() + relativedelta(days=-1)
    security_codes = SecurityCode.query.filter(
        extract('day', SecurityCode.created) == dt.day,
        extract('month', SecurityCode.created) == dt.month,
        extract('year', SecurityCode.created) == dt.year
    )

    for security_code in security_codes:
        db.session.delete(security_code)

    return ('', 200)
