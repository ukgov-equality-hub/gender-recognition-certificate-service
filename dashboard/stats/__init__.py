from flask import Blueprint, render_template
from sqlalchemy import func
from grc.models import db, Application

stats = Blueprint('stats', __name__)


@stats.route('/', methods=['GET'])
def index():
    message = ""
    stats = dict()

    applications_by_status = db.session.query(
        Application.status,
        func.count(Application.status)
    ).group_by(Application.status).all()

    stats['applications_by_status'] = applications_by_status

    return render_template(
        'stats/stats.html',
        message=message,
        stats=stats
    )
