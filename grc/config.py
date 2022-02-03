import logging
import os
from dotenv import load_dotenv
from os.path import join, dirname
from pathlib import Path


# Note this will fail with warnings, not exception
# if file does not exist. Therefore the config classes
# below will break.
# CI env variables are set in Heroku.

# app_base_path = Path(dirname(__file__))
# dotenv_path = join(str(app_base_path.parent), ".env")
# load_dotenv(dotenv_path)


class Config:
    BASE_DIRECTORY = dirname(dirname(os.path.abspath(__file__)))
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "PRODUCTION")
    SQLALCHEMY_DATABASE_URI  = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL")) if "LOG_LEVEL" in os.environ else logging.INFO
    NOTIFY_API = os.environ.get("NOTIFY_API")
    NOTIFY_SECURITY_CODE_EMAIL_TEMPLATE_ID = os.environ.get("NOTIFY_SECURITY_CODE_EMAIL_TEMPLATE_ID")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = int(os.environ.get("PERMANENT_SESSION_LIFETIME"))
    WTF_CSRF_ENABLED = True


class DevConfig(Config):
    DEBUG = True
    ENVIRONMENT = "DEVELOPMENT"
    LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL")) if "LOG_LEVEL" in os.environ else logging.DEBUG
    NOTIFY_API = os.environ.get("NOTIFY_API")
    NOTIFY_SECURITY_CODE_EMAIL_TEMPLATE_ID = os.environ.get("NOTIFY_SECURITY_CODE_EMAIL_TEMPLATE_ID")
    SERVER_NAME = "localhost:5000"
    SESSION_COOKIE_DOMAIN = False
    SESSION_COOKIE_SECURE = False


class TestConfig(Config):
    SESSION_COOKIE_SECURE = False
    TESTING = True
    WTF_CSRF_ENABLED = False

