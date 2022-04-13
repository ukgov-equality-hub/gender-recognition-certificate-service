import random
from datetime import datetime, timedelta
from dateutil import tz
from flask import current_app
from notifications_python_client.notifications import NotificationsAPIClient
from grc.models import db, SecurityCode


def delete_all_user_codes(email):
    delete_q = SecurityCode.__table__.delete().where(SecurityCode.email == email)
    db.session.execute(delete_q)
    db.session.commit()


def security_code_generator(email):
    delete_all_user_codes(email)

    try:
        code = ''.join(random.sample('0123456789', 5))
        record = SecurityCode(code=code, email=email)
        db.session.add(record)
        db.session.commit()
        return code

    except ValueError:
        print("Oops!  That was no valid code.  Try again...")


def validate_security_code(email, code):
    code_record = SecurityCode.query.filter_by(code=code, email=email).first()
    validPastTime = datetime.now() - timedelta(minutes=5)

    if code_record is None or validPastTime > code_record.created:
        print("The code has expired")
        return False
    else:
        print("The code is not older than 5 minutes")
        delete_all_user_codes(email)
        return True


def send_security_code(email):
    security_code = security_code_generator(email)

    if current_app.config['NOTIFY_OVERRIDE_EMAIL']:
        send_to = current_app.config['NOTIFY_OVERRIDE_EMAIL']
    else:
        send_to = email

    local = datetime.now().replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/London'))
    notifications_client = NotificationsAPIClient(current_app.config['NOTIFY_API'])
    response = notifications_client.send_email_notification(
        email_address=send_to,
        template_id=current_app.config['NOTIFY_SECURITY_CODE_EMAIL_TEMPLATE_ID'],
        personalisation={
            'security_code': security_code,
            'security_code_timeout': datetime.strftime(local + timedelta(minutes=5), '%d/%m/%Y %H:%M:%S')
        }
    )

    return response
