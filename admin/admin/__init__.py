import jwt
import random, string
from datetime import datetime, timedelta
from dateutil import tz
from flask import Blueprint, render_template, request, url_for, current_app, session
from werkzeug.security import check_password_hash, generate_password_hash
from admin.admin.forms import LoginForm
from grc.external_services.gov_uk_notify import GovUkNotify
from grc.models import db, AdminUser
from grc.utils.redirect import local_redirect
from grc.utils.logger import LogLevel, Logger
from grc.utils.security_code import security_code_generator
from grc.start_application.forms import SecurityCodeForm

admin = Blueprint('admin', __name__)
logger = Logger()


@admin.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()

    if 'signedIn' in session:
        return local_redirect(url_for('applications.index'))

    if request.method == 'POST':
        if form.validate_on_submit():
            email_address: str = form.email_address.data
            email_address = email_address.lower()
            user = AdminUser.query.filter_by(
                email=email_address
            ).first()

            if user is not None:
                if check_password_hash(user.password, form.password.data):
                    print(f'\nemail address logging in = {email_address}\n', flush=True)
                    session['email'] = email_address
                    if user.passwordResetRequired:
                        logger.log(LogLevel.INFO, f"{logger.mask_email_address(email_address)} password reset required")

                        return local_redirect(url_for('password_reset.index'))
                    else:
                        # Email out 2FA link
                        try:
                            local = datetime.now().replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/London'))
                            expires = datetime.strftime(local + timedelta(hours=24), '%H:%M on %d %b %Y')
                            security_code = security_code_generator(email_address)
                            GovUkNotify().send_email_admin_login_security_code(
                                email_address=user.email,
                                expires=expires,
                                security_code=security_code
                            )
                            logger.log(LogLevel.INFO, f"login link sent to {logger.mask_email_address(user.email)}")

                            return local_redirect(url_for('admin.sign_in_with_security_code'))

                        except Exception as e:
                            print(e, flush=True)

                else:
                    form.password.errors.append("Your password was incorrect. Please try re-entering your password")
                    logger.log(LogLevel.INFO, f"{logger.mask_email_address(email_address)} entered incorrect password")

            else:
                form.email_address.errors.append("A user with this email address was not found")
                session.pop('signedIn', None)
                session.pop('email', None)
                session.pop('userType', None)
                logger.log(LogLevel.WARN, f"User {logger.mask_email_address(email_address)} not found")

    else:
        addDefaultAdminUserToDatabaseIfThereAreNoUsers()

    return render_template(
        'login/login.html',
        form=form
    )


@admin.route('/sign-in-with-security_code', methods=['GET', 'POST'])
def sign_in_with_security_code():
    form = SecurityCodeForm()
    email_address = session['email']

    # 2FA link
    if request.method == 'POST':
        if form.validate_on_submit():

            user = AdminUser.query.filter_by(
                email=email_address
            ).first()

            if user is None:
                message = "We could not find your user details for this login link. Please try logging in again"
                return render_template('login/login-link-sent.html', message=message)

            local = datetime.now().replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/London'))
            user.dateLastLogin = datetime.strftime(local, '%d/%m/%Y %H:%M:%S')
            db.session.commit()

            session['signedIn'] = email_address
            session['userType'] = user.userType

            logger.log(LogLevel.INFO, f"User {logger.mask_email_address(email_address)} logged in with security code")

            return local_redirect(url_for('applications.index'))

    return render_template(
        'login/login-link-sent.html',
        email_address=email_address,
        form=form
    )


def addDefaultAdminUserToDatabaseIfThereAreNoUsers():
    users = db.session.query(AdminUser).count()
    if users == 0:
        defaultEmailAddress: str = current_app.config['DEFAULT_ADMIN_USER']
        defaultEmailAddress = defaultEmailAddress.lower()
        temporary_password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
        record = AdminUser(email=defaultEmailAddress, password=generate_password_hash(temporary_password), userType='ADMIN')
        db.session.add(record)
        db.session.commit()

        try:
            GovUkNotify().send_email_admin_new_user(
                email_address=defaultEmailAddress,
                temporary_password=temporary_password,
                application_link=request.base_url
            )
        except Exception as e:
            print(e, flush=True)