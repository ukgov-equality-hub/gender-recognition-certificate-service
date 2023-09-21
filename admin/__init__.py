import json
import os
from datetime import timedelta
from flask import Flask, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
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
        app.permanent_session_lifetime = timedelta(hours=3)
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

    memory_storage_uri = os.environ.get('MEMORY_STORAGE_URL', 'memory://')
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri=memory_storage_uri
    )

    # Filters
    app.register_blueprint(filters.blueprint)

    # Admin page
    from admin.admin import admin
    limiter.limit('2 per minute')(admin)
    app.register_blueprint(admin)

    # Signout
    from admin.signout import signout
    app.register_blueprint(signout)

    # Password reset
    from admin.password_reset import password_reset

    limiter.limit('2 per minute')(password_reset)
    app.register_blueprint(password_reset)

    # Forgot password
    from admin.forgot_password import forgot_password
    app.register_blueprint(forgot_password)

    # Applications
    from admin.applications import applications
    app.register_blueprint(applications)

    # Manage users
    from admin.users import users
    app.register_blueprint(users)

    # System jobs
    from admin.jobs import jobs
    app.register_blueprint(jobs)

    # Tools
    from admin.tools import tools
    app.register_blueprint(tools)

    # Tech Diagnostic pages
    from admin.diagnostics import diagnostics
    app.register_blueprint(diagnostics)

    # Health Check
    from admin.health_check import health_check
    app.register_blueprint(health_check)

    return app
