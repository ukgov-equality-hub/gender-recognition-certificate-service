import json
import os
from datetime import timedelta
from flask import Flask, g
from flask_migrate import Migrate
from flask_uuid import FlaskUUID
from grc.models import db
from grc.utils import filters
from dashboard.config import Config, DevConfig, TestConfig
from grc.utils.http_basic_authentication import HttpBasicAuthentication
from grc.utils.http_ip_whitelist import HttpIPWhitelist

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

    if app.config['IP_WHITELIST']:
        HttpIPWhitelist(app)

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
                                                        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; " \
                                                        "script-src-elem 'self' 'unsafe-inline' https://cdn.jsdelivr.net; " \
                                                        "script-src-attr 'self' 'unsafe-inline'; " \
                                                        "style-src 'self' 'unsafe-inline'; " \
                                                        "img-src 'self' blob: data:; " \
                                                        "font-src 'self' data:; " \
                                                        "connect-src 'self'; " \
                                                        "form-action 'self'"

        return response

    # Filters
    app.register_blueprint(filters.blueprint)

    # Dashboard page
    from dashboard.stats import stats
    app.register_blueprint(stats)

    # Feedback page
    from dashboard.feedback import feedback
    app.register_blueprint(feedback)

    # Health Check
    from dashboard.health_check import health_check
    app.register_blueprint(health_check)

    return app
