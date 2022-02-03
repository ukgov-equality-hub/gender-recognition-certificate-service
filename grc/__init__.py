import os

from flask import Flask
from flask_migrate import Migrate

from grc.models import db
from grc.config import Config, DevConfig,TestConfig


migrate = Migrate()

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
    # # if test_config is None:
    # #     # load the instance config, if it exists, when not testing
    # #     app.config.from_pyfile('config.py', silent=True)
    # # else:
    # #     # load the test config if passed in
    # #     app.config.from_mapping(test_config)

    # # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # database
    db.init_app(app)
    migrate.init_app(app, db)

    # Homepage
    from grc.start_application import startApplication
    app.register_blueprint(startApplication)
    app.add_url_rule('/', endpoint='index')

    # Save And Return
    from grc.save_and_return import saveAndReturn
    app.register_blueprint(saveAndReturn)
    app.add_url_rule('/save-and-return', endpoint='index')


    # Task List
    from grc.task_list import taskList
    app.register_blueprint(taskList)
    app.add_url_rule('/task-list', endpoint='index')

    return app
