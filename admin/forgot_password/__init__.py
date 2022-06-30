import jwt
from datetime import datetime, timedelta
from dateutil import tz
from flask import Blueprint, render_template, request, current_app, url_for
from admin.forgot_password.forms import ForgotPasswordForm
from grc.external_services.gov_uk_notify import GovUkNotify
from grc.models import AdminUser
from grc.utils.logger import LogLevel, Logger

forgot_password = Blueprint('forgot_password', __name__)
logger = Logger()


@forgot_password.route('/forgot_password', methods=['GET', 'POST'])
def index():
    form = ForgotPasswordForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            email_address: str = form.email_address.data
            email_address = email_address.lower()
            user = AdminUser.query.filter_by(
                email=email_address
            ).first()

            # Email out 2FA link
            if user is not None:
                try:
                    local = datetime.now().replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/London'))
                    expires = datetime.strftime(local + timedelta(hours=24), '%H:%M on %d %b %Y')
                    reset_link=request.host_url[:-1] + url_for('password_reset.reset_password_with_token') + '?token=' + jwt.encode({ 'id': user.id, 'email': user.email, 'expires': datetime.strftime(datetime.now() + timedelta(hours=24), '%d/%m/%Y %H:%M:%S') }, current_app.config['SECRET_KEY'], algorithm='HS256')
                    GovUkNotify().send_email_admin_forgot_password(
                        email_address=user.email,
                        expires=expires,
                        reset_link=reset_link
                    )

                    logger.log(LogLevel.INFO, f"Password reset link sent to {email_address}")

                except Exception as e:
                    print(e, flush=True)

                return render_template(
                    'forgot-password/forgot_password_sent_link.html',
                    form=form,
                    email_address=email_address
                )

            else:
                form.email_address.errors.append("A user with this email address was not found")
                logger.log(LogLevel.WARN, f"Password reset requested for unknown user {email_address}")

    return render_template(
        'forgot-password/forgot_password.html',
        form=form
    )
