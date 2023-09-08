from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import Blueprint
from flask.cli import with_appcontext
from sqlalchemy.sql import extract
from grc.external_services.gov_uk_notify import GovUkNotify
from grc.models import db, Application, ApplicationStatus, SecurityCode
from grc.utils.application_files import ApplicationFiles
from grc.utils.logger import Logger, LogLevel

notify_applicants_inactive_apps = Blueprint('notify_applicants_inactive_apps', __name__)


def application_notifications():
    days_between_last_update_and_deletion = 183  # approximately 6 months
    abandon_application_after_period_of_inactivity(days_between_last_update_and_deletion)
    send_reminder_emails_before_application_deletion(days_between_last_update_and_deletion)
    delete_completed_applications()
    delete_expired_security_codes()

    return 200


def abandon_application_after_period_of_inactivity(days_between_last_update_and_deletion):
    now = datetime.now()
    earliest_allowed_inactive_application_updated_date = calculate_earliest_allowed_inactive_application_updated_date(now, days_between_last_update_and_deletion)

    applications_to_anonymise = Application.query.filter(
        Application.status == ApplicationStatus.STARTED,
        Application.updated < earliest_allowed_inactive_application_updated_date
    )

    for application_to_anonymise in applications_to_anonymise:
        anonymise_application(application_to_anonymise, new_state=ApplicationStatus.ABANDONED)

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
        ).all()

        for application_to_remind in applications_to_remind:
            existing_application = Application.query.filter(
                Application.email == application_to_remind.email,
                ((Application.status == ApplicationStatus.SUBMITTED) | (Application.status == ApplicationStatus.DOWNLOADED) | (Application.status == ApplicationStatus.COMPLETED))
            ).first()
            if existing_application is None:
                GovUkNotify().send_email_unfinished_application(
                    email_address=application_to_remind.email,
                    expiry_days=period_of_time_until_deletion_phrase,
                    grc_return_link='https://apply-gender-recognition-certificate.service.gov.uk/'
                )


def calculate_last_updated_date(today, days_to_send_reminder_before_deletion, days_between_last_update_and_deletion):
    # If today is the day to send the reminder email, then the deletion date will be...
    deletion_date = today + relativedelta(days=days_to_send_reminder_before_deletion)

    # If that is the deletion date, then the application would have last been updated...
    last_updated_date = deletion_date - relativedelta(days=days_between_last_update_and_deletion)

    return last_updated_date


def delete_completed_applications():
    days_between_application_completion_and_anonymisation = 7

    now = datetime.now()
    earliest_allowed_application_completed_date = calculate_earliest_allowed_application_completed_date(now, days_between_application_completion_and_anonymisation)

    applications_to_anonymise = Application.query.filter(
        Application.status == ApplicationStatus.COMPLETED,
        Application.completed < earliest_allowed_application_completed_date
    )

    for application_to_anonymise in applications_to_anonymise:
        anonymise_application(application_to_anonymise, new_state=ApplicationStatus.DELETED)

    db.session.commit()


def calculate_earliest_allowed_application_completed_date(now, days_between_application_completion_and_anonymisation):
    return now - relativedelta(days=days_between_application_completion_and_anonymisation)


def anonymise_application(application_to_anonymise, new_state: ApplicationStatus):
    ApplicationFiles().delete_application_files(
        application_to_anonymise.reference_number,
        application_to_anonymise.application_data(),
    )
    application_to_anonymise.email = ''
    application_to_anonymise.user_input = ''
    application_to_anonymise.status = new_state


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


@notify_applicants_inactive_apps.cli.command('run')
@with_appcontext
def main():
    try:
        print('running notify applicants inactive apps job', flush=True)
        applicants_notified = application_notifications()
        assert applicants_notified == 200
        print('finished notify applicants inactive apps job', flush=True)
    except Exception as e:
        logger = Logger()
        logger.log(LogLevel.ERROR, f'Error notifying applicants cron, message = {e}')


if __name__ == '__main__':
    main()
