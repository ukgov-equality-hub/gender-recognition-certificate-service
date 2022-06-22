from flask import Blueprint, url_for, session
from grc.utils.redirect import local_redirect
from grc.utils.logger import LogLevel, Logger

signout = Blueprint('signout', __name__)
logger = Logger()


@signout.route('/signout', methods=['GET'])
def index():
    logger.log(LogLevel.INFO, f"{logger.mask_email_address(session['signedIn'])} logged out")
    session.pop('signedIn', None)
    session.pop('emailAddress', None)
    session.pop('userType', None)

    return local_redirect(url_for('admin.index'))
