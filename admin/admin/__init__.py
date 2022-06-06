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

admin = Blueprint('admin', __name__)


@admin.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if 'signedIn' in session:
        return local_redirect(url_for('applications.index'))

    if request.method == 'POST':
        if form.validate_on_submit():
            user = AdminUser.query.filter_by(
                email=form.email_address.data
            ).first()

            if user is not None:
                password_ok = check_password_hash(user.password, form.password.data)
                if password_ok:
                    if user.passwordResetRequired:
                        session['emailAddress'] = form.email_address.data
                        return local_redirect(url_for('password_reset.index'))
                    else:
                        # Email out 2FA link
                        try:
                            local = datetime.now().replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/London'))
                            expires = datetime.strftime(local + timedelta(hours=24), '%H:%M on %d %b %Y')
                            login_link = request.host_url[:-1] + url_for('admin.sign_in_with_token') + '?token=' + jwt.encode({'id': user.id, 'email': user.email, 'expires': datetime.strftime(datetime.now() + timedelta(hours=24), '%d/%m/%Y %H:%M:%S')}, current_app.config['SECRET_KEY'], algorithm='HS256')
                            GovUkNotify().send_email_admin_login_link(
                                email_address=user.email,
                                expires=expires,
                                login_link=login_link
                            )
                            return render_template('login/login-link-sent.html', email_address=user.email)

                        except Exception as e:
                            print(e, flush=True)
                else:
                    form.password.errors.append("Your password was incorrect. Please try re-entering your password")

            else:
                form.email_address.errors.append("A user with this email address was not found")
                session.pop('signedIn', None)
                session.pop('emailAddress', None)
                session.pop('userType', None)

    else:
        addDefaultAdminUserToDatabaseIfThereAreNoUsers()

    return render_template(
        'login/login.html',
        form=form
    )


@admin.route('/sign-in-with-token', methods=['GET'])
def sign_in_with_token():
    message = ""

    # 2FA link
    token = request.args.get('token')
    if token is not None:
        try:
            login_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            if 'id' in login_token and 'email' in login_token and 'expires' in login_token:
                dt = datetime.strptime(login_token['expires'], '%d/%m/%Y %H:%M:%S')
                if datetime.now() > dt:
                    message = "Your login link has expired. Please try logging in again"
                    session.pop('signedIn', None)
                    session.pop('emailAddress', None)
                    session.pop('userType', None)
                else:
                    user = AdminUser.query.filter_by(
                        id=login_token['id'], email=login_token['email']
                    ).first()
                    if user is None:
                        message = "We could not find your user details for this login link. Please try logging in again"
                        session.pop('signedIn', None)
                        session.pop('emailAddress', None)
                        session.pop('userType', None)
                    else:
                        signedIn = login_token['email']
                        local = datetime.now().replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/London'))
                        user.dateLastLogin = datetime.strftime(local, '%d/%m/%Y %H:%M:%S')
                        db.session.commit()

                        session['signedIn'] = signedIn
                        session['userType'] = user.userType

                        return local_redirect(url_for('applications.index'))
            else:
                message = "The login link was incorrect. If you pasted the web address, check you copied the entire address."

        except Exception as e:
            print(e, flush=True)


    return render_template(
        'login/login-link-error.html',
        message=message
    )


def addDefaultAdminUserToDatabaseIfThereAreNoUsers():
    users = db.session.query(AdminUser).count()
    if users == 0:
        defaultEmailAddress = current_app.config['DEFAULT_ADMIN_USER']
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