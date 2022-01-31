from functools import wraps
from flask import g, request, redirect, url_for, session

def EmailRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session or session['email'] is None:
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

def Unauthorized(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'application' in session:
            return redirect(url_for('taskList.index'))
        return f(*args, **kwargs)
    return decorated_function
