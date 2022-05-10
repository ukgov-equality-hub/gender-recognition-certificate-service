import jwt
from datetime import datetime
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from werkzeug.security import generate_password_hash
from admin.password_reset.forms import PasswordResetForm
from grc.models import db, AdminUser

password_reset = Blueprint('password_reset', __name__)


@password_reset.route('/password_reset', methods=['GET', 'POST'])
def index():
    if 'emailAddress' not in session:
        return redirect(url_for('forgot_password.index'))

    form = PasswordResetForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = AdminUser.query.filter_by(
                email=session['emailAddress']
            ).first()
            user.password = generate_password_hash(form.password.data)
            user.passwordResetRequired = False
            db.session.commit()

            return render_template('password_reset/password-has-been-reset.html')

    return render_template(
        'password_reset/password_reset.html',
        form=form
    )


@password_reset.route('/reset-password-with-token', methods=['GET'])
def reset_password_with_token():
    message = ""

    token = request.args.get('token')
    if token is not None:
        try:
            login_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            if 'id' in login_token and 'email' in login_token and 'expires' in login_token:
                dt = datetime.strptime(login_token['expires'], '%d/%m/%Y %H:%M:%S')
                if datetime.now() > dt:
                    message="Your reset password link has expired. Please try resetting your password again"

                else:
                    user = AdminUser.query.filter_by(
                        id=login_token['id'], email=login_token['email']
                    ).first()
                    if user is None:
                        message="We could not find your user details for this password reset link. Please try resetting your password again"
                    else:
                        session['emailAddress'] = login_token['email']
                        return redirect(url_for('password_reset.index'))
        except Exception as e:
            print(e, flush=True)

    if message == "":
        message = "The password reset link was incorrect. If you pasted the web address, check you copied the entire address."

    return render_template(
        'password_reset/password-reset-link-error.html',
        message=message
    )
