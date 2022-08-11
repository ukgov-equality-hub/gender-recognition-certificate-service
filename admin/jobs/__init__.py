import os
import io
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import Blueprint, request
from sqlalchemy.sql import extract
from grc.external_services.gov_uk_notify import GovUkNotify
from grc.models import db, Application, ApplicationStatus, SecurityCode
from grc.utils.decorators import JobTokenRequired
from grc.utils.application_files import ApplicationFiles
from grc.utils.config_helper import ConfigHelper

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
            application.application_data(),
            download=False
        )
        print('Creating pdf for application %s' % application.reference_number, flush=True)
        ApplicationFiles().create_or_download_pdf(
            application.reference_number,
            application.application_data(),
            is_admin=True,
            attach_files=True,
            download=False
        )

        application.filesCreated = True
        db.session.commit()

    return ('', 200)


#@jobs.route('/jobs/backup-db', methods=['GET'])
#@JobTokenRequired
def backup_db():
    import csv
    import io
    from sqlalchemy.inspection import inspect
    from cryptography.fernet import Fernet
    from grc.external_services.aws_s3_client import AwsS3Client

    def row2dict(row):
        return dict((col, getattr(row, col)) for col in row.__table__.columns.keys())

    def parse_datetime(dt):
        return str(dt)

    try:
        data = []
        secret_key = os.environ.get('EXTERNAL_BACKUP_ENCRYPTION_KEY', '')
        f = Fernet(secret_key)
        columns = get_columns()
        #data.append(columns)

        applications = Application.query.all()
        for application in applications:
            a = row2dict(application)
            record = []
            for idx, column in enumerate(columns):
                if column in ['status']:
                    record.append(application_status(a[column]) if a[column] is not None else '')
                elif column in ['created', 'updated', 'downloaded', 'completed']:
                    record.append(parse_datetime(a[column]) if a[column] is not None else '')
                else:
                    record.append(f.encrypt(str.encode(str(a[column]))))

            data.append(record)

        csv_buffer = io.StringIO()
        csv.writer(csv_buffer).writerows(data)
        csv_file = io.BytesIO(csv_buffer.getvalue().encode(encoding='utf-8'))

        space_name = (ConfigHelper.get_vcap_application().space_name.lower()
                      if ConfigHelper.get_vcap_application() is not None
                      else 'local')
        object_name = f"{space_name}/database/{datetime.now().strftime('%Y-%m-%d')}.csv"

        awsclient = AwsS3Client()
        awsclient.delete_object(object_name)
        awsclient.upload_fileobj(csv_file, object_name)

    except Exception as e:
        print(e, flush=True)

    return ('', 200)


#@jobs.route('/jobs/restore-db/<db_file>', methods=['GET'])
#@JobTokenRequired
def restore_db(db_file):
    from cryptography.fernet import Fernet
    from grc.external_services.aws_s3_client import AwsS3Client

    try:
        space_name = (ConfigHelper.get_vcap_application().space_name.lower()
                      if ConfigHelper.get_vcap_application() is not None
                      else 'local')
        data = AwsS3Client().download_object(f"{space_name}/database/{db_file}.csv")
        secret_key = os.environ.get('EXTERNAL_BACKUP_ENCRYPTION_KEY', '')
        f = Fernet(secret_key)
        columns = get_columns()

        applications = data.getvalue().splitlines()
        for application in applications:
            a = application.decode(encoding='utf-8').split(',')
            record = Application()
            for idx, column in enumerate(columns):
                if a[idx] != '':
                    if column in ['status']:
                        setattr(record, column, application_status(a[idx]))
                    elif column in ['created', 'updated', 'downloaded', 'completed']:
                        setattr(record, column, datetime.strptime(a[idx], '%Y-%m-%d  %H:%M:%S.%f'))
                    else:
                        val = str(f.decrypt(eval(a[idx])), 'utf-8')
                        if val == 'True':
                            val = True
                        elif val == 'False':
                            val = False
                        elif val == 'None':
                            val = None
                        if val != None:
                            setattr(record, column, val)

            db.session.add(record)
            db.session.commit()

    except Exception as e:
        print(e, flush=True)

    return ('', 200)


@jobs.route('/jobs/backup-files', methods=['GET'])
@JobTokenRequired
def backup_files():
    import time
    from zipstream import ZipStream
    import pyAesCrypt
    from grc.external_services.aws_s3_client import AwsS3Client

    tic = time.perf_counter()

    try:
        awsclient = AwsS3Client()
        awsclient_external = AwsS3Client(external=True)
        all_files = awsclient.list_objects()
        files = []

        for key in all_files:
            files.append({'stream': awsclient.stream_download_object(key), 'name': key})

        zip_buffer = ZipStream(files, chunksize=32768)

        fin = io.BytesIO()
        for data in zip_buffer.stream():
            fin.write(data)
        fin.seek(0)

        buffer_size = 64 * 1024
        secret_key = os.environ.get('EXTERNAL_BACKUP_ENCRYPTION_KEY', '')
        fout = io.BytesIO()
        pyAesCrypt.encryptStream(fin, fout, secret_key, buffer_size)
        fout.seek(0)

        space_name = (ConfigHelper.get_vcap_application().space_name.lower()
                      if ConfigHelper.get_vcap_application() is not None
                      else 'local')
        backup_file = f"{space_name}/files/{datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}.zip.encrypted"
        awsclient_external.stream_upload_object(fout, backup_file)  # or zip_buffer.stream() if we want unencrypted data

    except Exception as e:
        print(e, flush=True)

    toc = time.perf_counter()
    print(f"Finished in {toc - tic:0.4f} seconds", flush=True)

    return ('', 200)


@jobs.route('/jobs/application-notifications', methods=['GET'])
@JobTokenRequired
def application_notifications():
    days_between_last_update_and_deletion = 183  # approximately 6 months

    anonymise_application_after_period_of_inactivity(days_between_last_update_and_deletion)

    send_reminder_emails_before_application_deletion(days_between_last_update_and_deletion)

    anonymise_completed_applications()

    delete_expired_security_codes()

    return ('', 200)


def anonymise_application_after_period_of_inactivity(days_between_last_update_and_deletion):
    now = datetime.now()
    earliest_allowed_inactive_application_updated_date = calculate_earliest_allowed_inactive_application_updated_date(now, days_between_last_update_and_deletion)

    applications_to_anonymise = Application.query.filter(
        Application.status == ApplicationStatus.STARTED,
         Application.updated < earliest_allowed_inactive_application_updated_date
    )

    for application_to_anonymise in applications_to_anonymise:
        anonymise_application(application_to_anonymise)

    db.session.commit()


def calculate_earliest_allowed_inactive_application_updated_date(now, days_between_last_update_and_deletion):
    return now - relativedelta(days=days_between_last_update_and_deletion)


def send_reminder_emails_before_application_deletion(days_between_last_update_and_deletion):
    deletion_reminder_days_and_phrases = {
        # days: 'phrase'
        90: '3 months',
        30: '1 month',
        7: '1 week',
    }

    for days_to_send_reminder_before_deletion in deletion_reminder_days_and_phrases.keys():
        period_of_time_until_deletion_phrase = deletion_reminder_days_and_phrases[days_to_send_reminder_before_deletion]

        today = datetime.today()
        last_updated_date = calculate_last_updated_date(today, days_to_send_reminder_before_deletion, days_between_last_update_and_deletion)

        applications_to_remind = Application.query.filter(
            Application.status == ApplicationStatus.STARTED,
            extract('day', Application.updated) == last_updated_date.day,
            extract('month', Application.updated) == last_updated_date.month,
            extract('year', Application.updated) == last_updated_date.year
        )

        for application_to_remind in applications_to_remind:
            GovUkNotify().send_email_unfinished_application(
                email_address=application_to_remind.email,
                expiry_days=period_of_time_until_deletion_phrase,
                grc_return_link=request.host_url
            )


def calculate_last_updated_date(today, days_to_send_reminder_before_deletion, days_between_last_update_and_deletion):
    # If today is the day to send the reminder email, then the deletion date will be...
    deletion_date = today + relativedelta(days=days_to_send_reminder_before_deletion)

    # If that is the deletion date, then the application would have last been updated...
    last_updated_date = deletion_date - relativedelta(days=days_between_last_update_and_deletion)

    return last_updated_date


def anonymise_completed_applications():
    days_between_application_completion_and_anonymisation = 7

    now = datetime.now()
    earliest_allowed_application_completed_date = calculate_earliest_allowed_application_completed_date(now, days_between_application_completion_and_anonymisation)

    applications_to_anonymise = Application.query.filter(
        Application.status == ApplicationStatus.COMPLETED,
        Application.completed < earliest_allowed_application_completed_date
    )

    for application_to_anonymise in applications_to_anonymise:
        anonymise_application(application_to_anonymise)

    db.session.commit()


def calculate_earliest_allowed_application_completed_date(now, days_between_application_completion_and_anonymisation):
    return now - relativedelta(days=days_between_application_completion_and_anonymisation)


def anonymise_application(application_to_anonymise):
    ApplicationFiles().delete_application_files(
        application_to_anonymise.reference_number,
        application_to_anonymise.application_data(),
    )
    application_to_anonymise.email = ''
    application_to_anonymise.user_input = ''
    application_to_anonymise.status = ApplicationStatus.DELETED


def delete_expired_security_codes():
    hours_between_security_code_creation_and_expiry = 24

    now = datetime.now()
    earliest_allowed_security_code_creation_time = calculate_earliest_allowed_security_code_creation_time(now, hours_between_security_code_creation_and_expiry)

    security_codes_to_delete = SecurityCode.query.filter(
        SecurityCode.created < earliest_allowed_security_code_creation_time
    )

    for security_code_to_delete in security_codes_to_delete:
        db.session.delete(security_code_to_delete)

    db.session.commit()


def calculate_earliest_allowed_security_code_creation_time(now, hours_between_security_code_creation_and_expiry):
    return now - relativedelta(hours=hours_between_security_code_creation_and_expiry)


def get_columns():
    return ['reference_number', 'email', 'user_input', 'status', 'created', 'updated', 'downloaded', 'downloadedBy', 'completed', 'completedBy', 'filesCreated']


def application_status(status):
    if status == ApplicationStatus.COMPLETED:
        return 'COMPLETED'
    elif status == ApplicationStatus.DELETED:
        return 'DELETED'
    elif status == ApplicationStatus.STARTED:
        return 'STARTED'
    elif status == ApplicationStatus.SUBMITTED:
        return 'SUBMITTED'
    elif status == ApplicationStatus. DOWNLOADED:
        return 'DOWNLOADED'

    if status == 'COMPLETED':
        return ApplicationStatus.COMPLETED
    elif status == 'DELETED':
        return ApplicationStatus.DELETED
    elif status == 'STARTED':
        return ApplicationStatus.STARTED
    elif status == 'SUBMITTED':
        return ApplicationStatus.SUBMITTED
    elif status == 'DOWNLOADED':
        return ApplicationStatus. DOWNLOADED

    return ''
