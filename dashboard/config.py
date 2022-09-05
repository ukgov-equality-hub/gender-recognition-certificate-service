import logging
import os
from os.path import dirname
from grc.utils.config_helper import ConfigHelper


def get_connection_string() -> str:
    if ConfigHelper.get_vcap_services() is not None:
        creds = ConfigHelper.get_vcap_services().postgres[0].credentials
        return f"postgresql://{creds.username}:{creds.password}@{creds.host}:{creds.port}/{creds.database_name}"
    else:
        return os.environ.get("SQLALCHEMY_DATABASE_URI")


class Config:
    BASE_DIRECTORY = dirname(dirname(os.path.abspath(__file__)))
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "PRODUCTION")
    SQLALCHEMY_DATABASE_URI = get_connection_string()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_KEY = os.environ.get("SQLALCHEMY_KEY")
    LOG_LEVEL = (
        logging.getLevelName(os.environ.get("LOG_LEVEL"))
        if "LOG_LEVEL" in os.environ
        else logging.INFO
    )
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Strict"
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # Stops the CSRF token expiring (before the lifetime of the session). This was an accessibility problem
    BASIC_AUTH_USERNAME = os.environ.get("BASIC_AUTH_USERNAME")
    BASIC_AUTH_PASSWORD = os.environ.get("BASIC_AUTH_PASSWORD")
    IP_WHITELIST = os.environ.get("IP_WHITELIST")


class DevConfig(Config):
    DEBUG = True
    ENVIRONMENT = "DEVELOPMENT"
    LOG_LEVEL = (
        logging.getLevelName(os.environ.get("LOG_LEVEL"))
        if "LOG_LEVEL" in os.environ
        else logging.DEBUG
    )
    #SERVER_NAME = "localhost:5002"


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
