import json
import os
from datetime import timedelta
from flask import Flask, g
from flask_migrate import Migrate
from flask_uuid import FlaskUUID
from grc.models import db
from grc.utils import filters
from grc.config import Config, DevConfig, TestConfig
from grc.utils.http_basic_authentication import HttpBasicAuthentication
from grc.utils.maintenance_mode import Maintenance
from grc.utils.custom_error_handlers import CustomErrorHandlers

migrate = Migrate()
flask_uuid = FlaskUUID()


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if os.environ['FLASK_ENV'] == 'production':
        config_object = Config
    elif os.environ['FLASK_ENV'] == 'development':
        config_object = DevConfig
    else:
        config_object = TestConfig

    app.config.from_object(config_object)

    if os.environ['FLASK_ENV'] != 'development':
        CustomErrorHandlers(app)

    # Show "Service unavailable" page if the config setting it set
    if app.config['MAINTENANCE_MODE'] == 'ON':
        Maintenance(app)
        return app

    # Require HTTP Basic Authentication if both the username and password are set
    if app.config['BASIC_AUTH_USERNAME'] and app.config['BASIC_AUTH_PASSWORD']:
        HttpBasicAuthentication(app)

    # Load build info from JSON file
    f = open('build-info.json')
    build_info_string = f.read()
    f.close()
    build_info = json.loads(build_info_string)

    # Database
    db.init_app(app)
    migrate.init_app(app, db)

    flask_uuid.init_app(app)

    # Update session timeout time
    @app.before_request
    def make_before_request():
        app.permanent_session_lifetime = timedelta(hours=3)
        g.build_info = build_info

    @app.after_request
    def add_header(response):
        response.headers['X-Frame-Options'] = 'deny'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Content-Security-Policy'] = "default-src 'self'; " \
                                                        "script-src 'self' 'unsafe-inline'; " \
                                                        "script-src-elem 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com; " \
                                                        "script-src-attr 'self' 'unsafe-inline'; " \
                                                        "style-src 'self' 'unsafe-inline'; " \
                                                        "img-src 'self'; " \
                                                        "font-src 'self'; " \
                                                        "connect-src 'self' https://www.google-analytics.com; " \
                                                        f"form-action 'self' https://www.payments.service.gov.uk;"

        return response

    # Filters
    app.register_blueprint(filters.blueprint)

    # Homepage
    from grc.start_application import startApplication
    app.register_blueprint(startApplication)

    # Save And Return
    from grc.save_and_return import saveAndReturn
    app.register_blueprint(saveAndReturn)

    # Task List
    from grc.task_list import taskList
    app.register_blueprint(taskList)

    # Personal details
    from grc.personal_details import personalDetails
    app.register_blueprint(personalDetails)

    # Birth registration
    from grc.birth_registration import birthRegistration
    app.register_blueprint(birthRegistration)

    # Partnership details
    from grc.partnership_details import partnershipDetails
    app.register_blueprint(partnershipDetails)

    # Upload
    from grc.upload import upload
    app.register_blueprint(upload)

    # Submit and pay
    from grc.submit_and_pay import submitAndPay
    app.register_blueprint(submitAndPay)

    # Policies
    from grc.policies import policies
    app.register_blueprint(policies)

    # Feedback
    from grc.feedback import feedback
    app.register_blueprint(feedback)

    # Document checker
    from grc.document_checker import documentChecker
    app.register_blueprint(documentChecker)

    return app
