from flask import Blueprint, redirect, url_for, session

signout = Blueprint('signout', __name__)


@signout.route('/signout', methods=['GET'])
def index():
    session.pop('signedIn', None)
    session.pop('emailAddress', None)
    session.pop('userType', None)
    return redirect(url_for('admin.index'))
