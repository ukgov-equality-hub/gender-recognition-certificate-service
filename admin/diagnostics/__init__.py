import json

import jsonpickle
from flask import Blueprint, render_template
from grc.models import db, Application
from grc.utils.decorators import AdminViewerRequired
from grc.utils.logger import Logger

diagnostics = Blueprint('diagnostics', __name__)
logger = Logger()


@diagnostics.route('/diagnostics', methods=['GET'])
@AdminViewerRequired
def index():
    return render_template(
        'diagnostics/index.html'
    )


@diagnostics.route('/diagnostics/all-applications', methods=['GET'])
@AdminViewerRequired
def all_applications():
    get_all_applications_sql = "SELECT * FROM application ORDER BY id"
    get_all_applications_db_result = db.session.execute(get_all_applications_sql)
    db_rows = get_all_applications_db_result.mappings().all()

    application_rows = []

    for db_row in db_rows:
        application_row = {}
        application_rows.append(application_row)
        application_row['id'] = db_row.id
        application_row['status'] = db_row.status
        application_row['created'] = db_row.created
        application_row['updated'] = db_row.updated
        application_row['downloaded'] = db_row.downloaded
        application_row['downloadedBy'] = db_row.downloadedBy
        application_row['completed'] = db_row.completed
        application_row['completedBy'] = db_row.completedBy
        application_row['filesCreated'] = db_row.filesCreated
        application_row['number_sessions'] = db_row.number_sessions

        try:
            application = Application.query.filter_by(id=db_row.id).first()
            application_row['reference_number'] = application.reference_number
            application_row['email'] = application.email
            application_row['user_input'] = application.user_input

        except Exception as e:
            application_row['error'] = e

    return render_template(
        'diagnostics/all-applications.html',
        number_of_results = len(db_rows),
        application_rows = application_rows
    )


@diagnostics.route('/diagnostics/applications/<id>', methods=['GET'])
@AdminViewerRequired
def application_by_id(id):
    get_application_sql = "SELECT * FROM application WHERE id = :id"
    get_application_result = db.session.execute(get_application_sql, { 'id': id })
    db_row = get_application_result.mappings().first()

    application_row = {}
    application_row['id'] = db_row.id
    application_row['status'] = db_row.status
    application_row['created'] = db_row.created
    application_row['updated'] = db_row.updated
    application_row['downloaded'] = db_row.downloaded
    application_row['downloadedBy'] = db_row.downloadedBy
    application_row['completed'] = db_row.completed
    application_row['completedBy'] = db_row.completedBy
    application_row['filesCreated'] = db_row.filesCreated
    application_row['number_sessions'] = db_row.number_sessions

    try:
        application = Application.query.filter_by(id=db_row.id).first()
        application_row['reference_number'] = application.reference_number
        application_row['email'] = application.email
        application_row['user_input'] = application.user_input
        application_row['user_input_prettified'] = json.dumps(json.loads(application.user_input), indent=8)
        application_row['application_data'] = application.application_data()
        application_row['application_data_prettified'] = jsonpickle.encode(application.application_data(), indent=8)

    except Exception as e:
        application_row['error'] = e

    return render_template(
        'diagnostics/application.html',
        application_id = id,
        application_row = application_row
    )

