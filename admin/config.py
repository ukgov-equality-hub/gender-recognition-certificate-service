import logging
import os
from os.path import dirname


class Config:
    BASE_DIRECTORY = dirname(dirname(os.path.abspath(__file__)))
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "PRODUCTION")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL")) if "LOG_LEVEL" in os.environ else logging.INFO
    NOTIFY_OVERRIDE_EMAIL = os.environ.get("NOTIFY_OVERRIDE_EMAIL") if "NOTIFY_OVERRIDE_EMAIL" in os.environ else False
    NOTIFY_API = os.environ.get("NOTIFY_API")
    NOTIFY_SECURITY_CODE_EMAIL_TEMPLATE_ID = 'd93108b9-4a5b-4268-91ee-2bb59686e702'
    NOTIFY_UNFINISHED_APPLICATION_EMAIL_TEMPLATE_ID = '151fce32-1f66-4efd-a875-28026e8d8d70'
    NOTIFY_COMPLETED_APPLICATION_EMAIL_TEMPLATE_ID = 'd3a252f7-5580-4299-8889-01ac235e8de7'
    NOTIFY_ADMIN_LOGIN_TEMPLATE_ID = 'ddfa69ca-e89d-49d1-8311-b487732860ec'
    NOTIFY_ADMIN_FORGOT_PASSWORD_TEMPLATE_ID = '7e2ed682-d120-4937-9154-1966976e0144'
    NOTIFY_ADMIN_NEW_USER_TEMPLATE_ID = '0ff48a4c-601e-4cc1-b6c6-30bac012c259'
    NOTIFY_DOCUMENT_CHECKER_LIST_TEMPLATE_ID = 'cd90e372-4b0f-4904-a0c9-5335c735ff88'
    GOVUK_PAY_API = os.environ.get("GOVUK_PAY_API")
    GOVUK_PAY_API_KEY = os.environ.get("GOVUK_PAY_API_KEY")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = int(os.environ.get("PERMANENT_SESSION_LIFETIME"))
    WTF_CSRF_ENABLED = True
    AWS_ACCESS_KEY_ID = "FDIA3GOLL9JYJ4XTGPFD" #os.environ.get("AWS_ACCESS_KEY_ID")
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
