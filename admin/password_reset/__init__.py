import jwt
from datetime import datetime
from flask import Blueprint, render_template, request, current_app, session
from werkzeug.security import generate_password_hash
from admin.password_reset.forms import PasswordResetForm
from grc.models import db, AdminUser

password_reset = Blueprint('password_reset', __name__)


@password_reset.route('/password_reset', methods=['GET', 'POST'])
def index():
    form = PasswordResetForm()
    emailAddress = ""
    password = ""
    confirmPassword = ""
    if 'emailAddress' in session:
        emailAddress = session['emailAddress']
    message = ""

    if request.method == 'POST':
        password = form.password.data
        confirmPassword = form.confirmPassword.data
        if form.validate_on_submit():
            user = AdminUser.query.filter_by(
                email=emailAddress
            ).first()
            user.password = generate_password_hash(form.password.data)
            user.passwordResetRequired = False
            db.session.commit()

            password = ""
            confirmPassword = ""
            message = "Your password has been updated"

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
                    else:
                        user = AdminUser.query.filter_by(
                            id=login_token['id'], email=login_token['email']
                        ).first()
                        if user is None:
                            message = "Invalid user"
                        else:
                            emailAddress = login_token['email']
                            session['emailAddress'] = emailAddress
                else:
                    message = "Invalid token"
            except Exception as e:
                print(e, flush=True)

    return render_template(
        'password_reset.html',
        form=form,
        emailAddress=emailAddress,
        password=password,
        confirmPassword=confirmPassword,
        message=message
    )
