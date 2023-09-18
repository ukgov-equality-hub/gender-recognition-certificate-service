import random
from datetime import datetime, timedelta
from dateutil import tz
from grc.external_services.gov_uk_notify import GovUkNotify
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
    validPastTime = datetime.now() - timedelta(hours=24)

    if code_record is None or validPastTime > code_record.created:
        print("The code has expired")
        return False
    else:
        print("The code is not older than 5 minutes")
        delete_all_user_codes(email)
        return True


def generate_security_code(email):
    security_code = security_code_generator(email)
    local = datetime.now().replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/London'))
    security_code_timeout = datetime.strftime(local + timedelta(hours=24), '%H:%M on %d %b %Y')
    return security_code, security_code_timeout


def send_security_code(email):
    security_code, security_code_timeout = generate_security_code(email)
    response = GovUkNotify().send_email_security_code(
        email_address=email,
        security_code=security_code,
        security_code_timeout=security_code_timeout
    )

    return response


def send_security_code_admin(email):
    security_code, expires = generate_security_code(email)

    response = GovUkNotify().send_email_admin_login_security_code(
        email_address=email,
        security_code=security_code,
        expires=expires
    )

    return response
