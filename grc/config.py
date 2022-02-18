import logging
import os
from os.path import dirname

class Config:
    BASE_DIRECTORY = dirname(dirname(os.path.abspath(__file__)))
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "PRODUCTION")
    SQLALCHEMY_DATABASE_URI  = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL")) if "LOG_LEVEL" in os.environ else logging.INFO
    NOTIFY_API = os.environ.get("NOTIFY_API")
    NOTIFY_SECURITY_CODE_EMAIL_TEMPLATE_ID = os.environ.get("NOTIFY_SECURITY_CODE_EMAIL_TEMPLATE_ID")
    NOTIFY_UNFINISHED_APPLICATION_EMAIL_TEMPLATE_ID = os.environ.get("NOTIFY_UNFINISHED_APPLICATION_EMAIL_TEMPLATE_ID")
    NOTIFY_COMPLETED_APPLICATION_EMAIL_TEMPLATE_ID = os.environ.get("NOTIFY_COMPLETED_APPLICATION_EMAIL_TEMPLATE_ID")
    GOVUK_PAY_API = os.environ.get("GOVUK_PAY_API")
    GOVUK_PAY_API_KEY = os.environ.get("GOVUK_PAY_API_KEY")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = int(os.environ.get("PERMANENT_SESSION_LIFETIME"))
    WTF_CSRF_ENABLED = True
    AWS_ACCESS_KEY_ID=os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY=os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_REGION=os.environ.get("AWS_REGION")
    AWS_S3_REGION_NAME=os.environ.get("AWS_REGION")
    AWS_S3_SIGNATURE_VERSION="s3v4"
    BUCKET_NAME=os.environ.get("BUCKET_NAME")



class DevConfig(Config):
    DEBUG = True
    ENVIRONMENT = "DEVELOPMENT"
    LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL")) if "LOG_LEVEL" in os.environ else logging.DEBUG
    SERVER_NAME = "localhost:5000"
    SESSION_COOKIE_DOMAIN = False
    SESSION_COOKIE_SECURE = False


class TestConfig(Config):
    SESSION_COOKIE_SECURE = False
    TESTING = True
    WTF_CSRF_ENABLED = False

