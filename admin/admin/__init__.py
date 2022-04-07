import jwt
import string
import random
from datetime import datetime, timedelta
from flask import Blueprint, redirect, render_template, request, url_for, current_app, session
from werkzeug.security import check_password_hash, generate_password_hash
from notifications_python_client.notifications import NotificationsAPIClient
from admin.admin.forms import LoginForm
from grc.models import db, AdminUser

admin = Blueprint('admin', __name__)


@admin.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    signedIn = ""
    emailAddress = ""
    password = ""
    if 'signedIn' in session:
        return redirect(url_for('applications.index'))

    message = ""

    if request.method == 'POST':
        if form.action.data == 'signin':
            emailAddress = form.email.data
            password = form.password.data
            if form.validate_on_submit():
                user = AdminUser.query.filter_by(
                    email=emailAddress
                ).first()

                if user is not None:
                    password_ok = check_password_hash(user.password, form.password.data)
                    if password_ok:
                        if user.passwordResetRequired:
                            session['emailAddress'] = emailAddress
                            return redirect(url_for('password_reset.index'))
                        else:
                            message = "A login link has been sent to your email address, please click on this link to login"

                            # Email out 2FA link
                            try:
                                notifications_client = NotificationsAPIClient(current_app.config['NOTIFY_API'])
                                notifications_client.send_email_notification(
                                    email_address=user.email,
                                    template_id=current_app.config['NOTIFY_ADMIN_LOGIN_TEMPLATE_ID'],
                                    personalisation={
                                        'expires': datetime.strftime(datetime.now() + timedelta(minutes=30), '%d/%m/%Y %H:%M:%S'),
                                        'login_link': request.base_url + '?token=' + jwt.encode({ 'id': user.id, 'email': user.email, 'expires': datetime.strftime(datetime.now() + timedelta(hours=1), '%d/%m/%Y %H:%M:%S') }, current_app.config['SECRET_KEY'], algorithm='HS256')
                                    }
                                )
                            except Exception as e:
                                print(e, flush=True)
                    else:
                        message = "NOT OK"
                else:
                    message = "User not found"
                    signedIn = ""
                    session.pop('signedIn', None)
                    session.pop('emailAddress', None)
                    session.pop('userType', None)

        elif form.action.data == 'signout':
            emailAddress = ""
            password = ""
            signedIn = ""
            session.pop('signedIn', None)
            session.pop('emailAddress', None)
            session.pop('userType', None)
            message = "You have been logged out"

    else:
        # 2FA link
        token = request.args.get('token')
        if token is not None:
            try:
                login_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                if 'id' in login_token and 'email' in login_token and 'expires' in login_token:
                    dt = datetime.strptime(login_token['expires'], '%d/%m/%Y %H:%M:%S')
                    if datetime.now() > dt:
                        message = "Your token has expired, please try again"
                        signedIn = ""
                        session.pop('signedIn', None)
                        session.pop('emailAddress', None)
                        session.pop('userType', None)
                    else:
                        user = AdminUser.query.filter_by(
                            id=login_token['id'], email=login_token['email']
                        ).first()
                        if user is None:
                            message = "Invalid user"
                            signedIn = ""
                            session.pop('signedIn', None)
                            session.pop('emailAddress', None)
                            session.pop('userType', None)
                        else:
                            signedIn = login_token['email']
                            user.dateLastLogin = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
                            db.session.commit()

                            session['signedIn'] = signedIn
                            session['userType'] = user.userType

                            return redirect(url_for('applications.index'))
                else:
                    message = "Invalid token"
            except Exception as e:
                print(e, flush=True)

        else:
            users = db.session.query(AdminUser).count()
            if users == 0:
                defaultEmailAddress = current_app.config['DEFAULT_ADMIN_USER']
                temporary_password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
                record = AdminUser(email=defaultEmailAddress, password=generate_password_hash(temporary_password), userType='ADMIN')
                db.session.add(record)
                db.session.commit()

                try:
                    notifications_client = NotificationsAPIClient(current_app.config['NOTIFY_API'])
                    notifications_client.send_email_notification(
                        email_address=defaultEmailAddress,
                        template_id=current_app.config['NOTIFY_ADMIN_NEW_USER_TEMPLATE_ID'],
                        personalisation={
                            'temporary_password': temporary_password,
                            'application_link': request.base_url
                        }
                    )
                except Exception as e:
                    print(e, flush=True)

    return render_template(
        'admin.html',
        form=form,
        signedIn=signedIn,
        emailAddress=emailAddress,
        password=password,
        message=message
    )
