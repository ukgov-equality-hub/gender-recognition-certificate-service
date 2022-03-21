import jwt
from datetime import datetime, timedelta
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, session
)
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash
from flask import render_template
from notifications_python_client.notifications import NotificationsAPIClient
from admin.forgot_password.forms import ForgotPasswordForm
from grc.models import db, AdminUser

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
                    notifications_client = NotificationsAPIClient(current_app.config['NOTIFY_API'])
                    notifications_client.send_email_notification(
                        email_address=user.email,
                        template_id=current_app.config['NOTIFY_ADMIN_FORGOT_PASSWORD_TEMPLATE_ID'],
                        personalisation={
                            'expires': datetime.strftime(datetime.now() + timedelta(minutes=30), '%d/%m/%Y %H:%M:%S'),
                            'reset_link': 'http://localhost:5001/password_reset?token=' + jwt.encode({ 'id': user.id, 'email': user.email, 'expires': datetime.strftime(datetime.now() + timedelta(hours=1), '%d/%m/%Y %H:%M:%S') }, current_app.config['SECRET_KEY'], algorithm='HS256')
                        }
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
