from flask import Blueprint
from .notify_applicants_inactive_apps import notify_applicants_inactive_apps

jobs = Blueprint('jobs', __name__)
jobs.register_blueprint(notify_applicants_inactive_apps)
