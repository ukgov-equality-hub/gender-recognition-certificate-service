import string
import random
from flask import Blueprint, redirect, render_template, request, url_for, current_app, session
from werkzeug.security import generate_password_hash
from notifications_python_client.notifications import NotificationsAPIClient
from grc.utils.decorators import AdminRequired
from admin.users.forms import UsersForm
from grc.models import db, AdminUser

users = Blueprint('users', __name__)


@users.route('/users', methods=['GET', 'POST'])
@AdminRequired
def index():
    form = UsersForm()
    emailAddress = ""
    message = ""

    if request.method == 'POST':
        emailAddress = form.email.data
        if form.validate_on_submit():
            user = AdminUser.query.filter_by(
                email=emailAddress
            ).first()

            if user is not None:
                message = "A user account with that email address already exists"
            else:
                temporary_password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
                userType = 'ADMIN' if form.userType.data else 'VIEWER'
                record = AdminUser(email=emailAddress, password=generate_password_hash(temporary_password), userType=userType)
                db.session.add(record)
                db.session.commit()

                try:
                    notifications_client = NotificationsAPIClient(current_app.config['NOTIFY_API'])
                    notifications_client.send_email_notification(
                        email_address=emailAddress,
                        template_id=current_app.config['NOTIFY_ADMIN_NEW_USER_TEMPLATE_ID'],
                        personalisation={
                            'temporary_password': temporary_password,
                            'application_link': request.base_url
                        }
                    )
                except Exception as e:
                    print(e, flush=True)

                message = "An invitation email has been sent"
    else:
        if 'message' in session and session['message'] != "":
            message = session['message']
            session['message'] = ""

    users = AdminUser.query.all()

    return render_template(
        'users.html',
        form=form,
        emailAddress=emailAddress,
        message=message,
        users=users
    )


@users.route('/users/<emailAddress>/delete', methods=['GET'])
@AdminRequired
def delete(emailAddress):
    message = ""

    users = AdminUser.query.filter_by(
        userType='ADMIN'
    ).count()

    if users == 1:
        message = "Cannot delete the last admin user in the database"
    else:
        user = AdminUser.query.filter_by(
            email=emailAddress
        ).first()

        if user is None:
            message = "A user account with that email address cannot be found"
        else:
            db.session.delete(user)
            db.session.commit()
            message = "user deleted"

    session['message'] = message
    return redirect(url_for('users.index'))


@users.route('/users/<emailAddress>/resend', methods=['GET'])
@AdminRequired
def resend(emailAddress):
    message = ""

    user = AdminUser.query.filter_by(
        email=emailAddress
    ).first()

    if user is None:
        message = "A user account with that email address cannot be found"
    elif user.dateLastLogin is not None:
        message = "Can't resent this users password"
    else:
        temporary_password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
        user.password = generate_password_hash(temporary_password)
        db.session.commit()

        try:
            notifications_client = NotificationsAPIClient(current_app.config['NOTIFY_API'])
            notifications_client.send_email_notification(
                email_address=user.email,
                template_id=current_app.config['NOTIFY_ADMIN_NEW_USER_TEMPLATE_ID'],
                personalisation={
                    'temporary_password': temporary_password,
                    'application_link': request.base_url
                }
            )
        except Exception as e:
            print(e, flush=True)

        message = "An invitation email has been resent"

    session['message'] = message
    return redirect(url_for('users.index'))
