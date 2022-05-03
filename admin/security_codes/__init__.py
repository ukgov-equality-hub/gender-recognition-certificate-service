from flask import Blueprint, render_template
from grc.utils.decorators import AdminRequired
from grc.models import db, SecurityCode

codes = Blueprint('codes', __name__)


@codes.route('/security_codes', methods=['GET'])
@AdminRequired
def index():
    message = ""
    security_codes = SecurityCode.query.all()

    return render_template(
        'security_codes.html',
        message=message,
        codes=security_codes
    )


@codes.route('/security_codes/<securityCode>/delete', methods=['GET'])
@AdminRequired
def delete(securityCode):
    message = ""

    code = SecurityCode.query.filter_by(
        code=securityCode
    ).first()

    if code is None:
        message = "Security code cannot be found"
    else:
        db.session.delete(code)
        db.session.commit()
        message = "code deleted"

    security_codes = SecurityCode.query.all()

    return render_template(
        'security_codes.html',
        message=message,
        codes=security_codes
    )
