import jwt
from datetime import datetime, timedelta
from dateutil import tz
from flask import Blueprint, render_template, request, current_app
from admin.forgot_password.forms import ForgotPasswordForm
from grc.external_services.gov_uk_notify import GovUkNotify
from grc.models import AdminUser

forgot_password = Blueprint('forgot_password', __name__)


@forgot_password.route('/forgot_password', methods=['GET', 'POST'])
def index():
    form = ForgotPasswordForm()
    emailAddress = ""
    message = ""

    if request.method == 'POST':
        emailAddress = form.email.data
        if form.validate_on_submit():
            user = AdminUser.query.filter_by(
                email=emailAddress
            ).first()

            # Email out 2FA link
            if user is not None:
                try:
                    local = datetime.now().replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/London'))
                    expires = datetime.strftime(local + timedelta(hours=1), '%d/%m/%Y %H:%M:%S')
                    reset_link=request.base_url[: request.base_url.rindex('/') + 1]    + 'password_reset?token=' + jwt.encode({ 'id': user.id, 'email': user.email, 'expires': datetime.strftime(datetime.now() + timedelta(hours=1), '%d/%m/%Y %H:%M:%S') }, current_app.config['SECRET_KEY'], algorithm='HS256')
                    GovUkNotify().send_email_admin_forgot_password(
                        email_address=user.email,
                        expires=expires,
                        reset_link=reset_link
                    )
                except Exception as e:
                    print(e, flush=True)

            message = "If an account matches the email address you entered, a password reset link will be sent"

    return render_template(
        'forgot_password.html',
        form=form,
        emailAddress=emailAddress,
        message=message
    )
