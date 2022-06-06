from flask import Blueprint, url_for, session
from grc.utils.redirect import local_redirect

signout = Blueprint('signout', __name__)


@signout.route('/signout', methods=['GET'])
def index():
    session.pop('signedIn', None)
    session.pop('emailAddress', None)
    session.pop('userType', None)
    return local_redirect(url_for('admin.index'))
