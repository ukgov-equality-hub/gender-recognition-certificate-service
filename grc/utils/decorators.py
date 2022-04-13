from functools import wraps
from flask import g, request, redirect, url_for, session

def EmailRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session or session['email'] is None:
            return redirect(url_for('startApplication.index'))
        return f(*args, **kwargs)
    return decorated_function


def ValidatedEmailRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'validatedEmail' not in session or session['validatedEmail'] is None:
            return redirect(url_for('startApplication.index'))
        return f(*args, **kwargs)
    return decorated_function


def LoginRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session or session['email'] is None:
            return redirect(url_for('startApplication.index'))
        return f(*args, **kwargs)
    return decorated_function


def AdminViewerRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'signedIn' not in session or session['signedIn'] is None:
            return redirect(url_for('admin.index'))
        return f(*args, **kwargs)
    return decorated_function


def AdminRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userType' not in session or session['userType'] is None:
            return redirect(url_for('admin.index'))
        elif session['userType'] != 'ADMIN':
            return redirect(url_for('admin.index'))
        return f(*args, **kwargs)
    return decorated_function


def Unauthorized(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'application' in session:
            return redirect(url_for('taskList.index'))
        return f(*args, **kwargs)
    return decorated_function
