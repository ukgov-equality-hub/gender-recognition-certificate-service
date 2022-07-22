from functools import wraps
from flask import g, request, abort, url_for, current_app, request, session
from grc.utils.redirect import local_redirect
from grc.utils.logger import LogLevel, Logger

logger = Logger()


def get_signedin_user():
    user = 'An unknown user'
    if 'signedIn' in session:
        user = logger.mask_email_address(session['signedIn'])
    elif 'email' in session:
        user = logger.mask_email_address(session['email'])

    return user


def EmailRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session or session['email'] is None:
            logger.log(LogLevel.WARN, f"(EmailRequired) An unknown user has attempted to access {request.host_url}")
            return local_redirect(url_for('startApplication.index'))
        return f(*args, **kwargs)
    return decorated_function


def ValidatedEmailRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'validatedEmail' not in session or session['validatedEmail'] is None:
            logger.log(LogLevel.WARN, f"(ValidatedEmailRequired) {get_signedin_user()} has attempted to access {request.host_url}")
            return local_redirect(url_for('startApplication.index'))
        return f(*args, **kwargs)
    return decorated_function


def LoginRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'reference_number' not in session or session['reference_number'] is None:
            logger.log(LogLevel.WARN, f"(LoginRequired) {get_signedin_user()} has attempted to access {request.host_url}")
            return local_redirect(url_for('startApplication.index'))
        return f(*args, **kwargs)
    return decorated_function


def AdminViewerRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'signedIn' not in session or session['signedIn'] is None:
            logger.log(LogLevel.WARN, f"(AdminViewerRequired) An unknown user has attempted to access {request.host_url}")
            return local_redirect(url_for('admin.index'))
        return f(*args, **kwargs)
    return decorated_function


def AdminRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userType' not in session or session['userType'] is None:
            logger.log(LogLevel.WARN, f"(AdminRequired) {get_signedin_user()} type has attempted to access {request.host_url}")
            return local_redirect(url_for('admin.index'))
        elif session['userType'] != 'ADMIN':
            logger.log(LogLevel.WARN, f"(AdminRequired) {get_signedin_user()} has attempted to access {request.host_url}")
            return local_redirect(url_for('admin.index'))
        return f(*args, **kwargs)
    return decorated_function


def Unauthorized(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'reference_number' in session:
            logger.log(LogLevel.WARN, f"(Unauthorized) {get_signedin_user()} has attempted to access {request.host_url}")
            return local_redirect(url_for('taskList.index'))
        return f(*args, **kwargs)
    return decorated_function


def JobTokenRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.args.get('token') != current_app.config['JOB_TOKEN']:
            logger.log(LogLevel.WARN, f"(JobTokenRequired) An unknown user has attempted to access {request.host_url}")
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function
