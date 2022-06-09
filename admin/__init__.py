import json
import os
from datetime import timedelta
from flask import Flask, g
from flask_migrate import Migrate
from flask_uuid import FlaskUUID
from grc.models import db
from grc.utils import filters
from admin.config import Config, DevConfig, TestConfig
from grc.utils.http_basic_authentication import HttpBasicAuthentication

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

    # Require HTTP Basic Authentication if both the username and password are set
    if app.config['BASIC_AUTH_USERNAME'] and app.config['BASIC_AUTH_PASSWORD']:
        HttpBasicAuthentication(app)

    # Load build info from JSON file
    f = open('build-info.json')
    build_info_string = f.read()
    f.close()
    build_info = json.loads(build_info_string)

    # database
    db.init_app(app)
    migrate.init_app(app, db)

    flask_uuid.init_app(app)

    # update session timeout time
    @app.before_request
    def make_before_request():
        app.permanent_session_lifetime = timedelta(hours=24)
        g.build_info = build_info

    @app.after_request
    def add_header(response):
        response.headers['X-Frame-Options'] = 'deny'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Content-Security-Policy'] = "default-src 'self'; " \
                                                        "script-src 'self' 'unsafe-inline'; " \
                                                        "script-src-elem 'self' 'unsafe-inline'; " \
                                                        "script-src-attr 'self' 'unsafe-inline'; " \
                                                        "style-src 'self' 'unsafe-inline'; " \
                                                        "img-src 'self'; " \
                                                        "font-src 'self'; " \
                                                        "connect-src 'self'; " \
                                                        "form-action 'self'"

        return response

    # Filters
    app.register_blueprint(filters.blueprint)

    # Admin page
    from admin.admin import admin
    app.register_blueprint(admin)
    app.add_url_rule('/', endpoint='index')

    # Signout
    from admin.signout import signout
    app.register_blueprint(signout)
    app.add_url_rule('/signout', endpoint='index')

    # Password reset
    from admin.password_reset import password_reset
    app.register_blueprint(password_reset)
    app.add_url_rule('/password_reset', endpoint='index')

    # Forgot password
    from admin.forgot_password import forgot_password
    app.register_blueprint(forgot_password)
    app.add_url_rule('/forgot_password', endpoint='index')

    # Applications
    from admin.applications import applications
    app.register_blueprint(applications)
    app.add_url_rule('/applications', endpoint='index')

    # Manage users
    from admin.users import users
    app.register_blueprint(users)
    app.add_url_rule('/users', endpoint='index')

    # System jobs
    from admin.jobs import jobs
    app.register_blueprint(jobs)
    app.add_url_rule('/jobs', endpoint='index')

    return app
