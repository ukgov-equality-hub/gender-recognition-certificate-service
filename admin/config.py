import logging
import os
from os.path import dirname


class Config:
    BASE_DIRECTORY = dirname(dirname(os.path.abspath(__file__)))
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "PRODUCTION")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_KEY = os.environ.get("SQLALCHEMY_KEY")
    LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL")) if "LOG_LEVEL" in os.environ else logging.INFO
    NOTIFY_OVERRIDE_EMAIL = os.environ.get("NOTIFY_OVERRIDE_EMAIL") if "NOTIFY_OVERRIDE_EMAIL" in os.environ else False
    NOTIFY_API = os.environ.get("NOTIFY_API")
    GOVUK_PAY_API = os.environ.get("GOVUK_PAY_API")
    GOVUK_PAY_API_KEY = os.environ.get("GOVUK_PAY_API_KEY")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = int(os.environ.get("PERMANENT_SESSION_LIFETIME"))
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # Stops the CSRF token expiring (before the lifetime of the session). This was an accessibility problem
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.environ.get("AWS_REGION")
    AWS_S3_REGION_NAME = os.environ.get("AWS_REGION")
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    BUCKET_NAME = os.environ.get("BUCKET_NAME")


class DevConfig(Config):
    DEBUG = True
    ENVIRONMENT = "DEVELOPMENT"
    LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL")) if "LOG_LEVEL" in os.environ else logging.DEBUG
    #SERVER_NAME = "localhost:5001"
    SESSION_COOKIE_DOMAIN = False
    SESSION_COOKIE_SECURE = False


class TestConfig(Config):
    SESSION_COOKIE_SECURE = False
    TESTING = True
    WTF_CSRF_ENABLED = False
