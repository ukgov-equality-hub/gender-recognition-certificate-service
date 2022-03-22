import os
from flask import Flask
from flask_migrate import Migrate
from flask_uuid import FlaskUUID
from datetime import datetime, timedelta
from grc.models import db
from grc.config import Config, DevConfig, TestConfig

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

    # database
    db.init_app(app)
    migrate.init_app(app, db)

    flask_uuid.init_app(app)

    # update session timeout time
    @app.before_request
    def make_before_request():
        app.permanent_session_lifetime = timedelta(minutes=int(config_object.PERMANENT_SESSION_LIFETIME))

    # Filters
    @app.template_filter('format_date')
    def format_date_filter(dt):
        return datetime.strftime(dt, '%d/%m/%Y %H:%M')

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

    return app
