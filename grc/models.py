import os
from datetime import datetime
import enum
import jsonpickle
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
from grc.business_logic.data_structures.application_data import ApplicationData

db = SQLAlchemy()
secret_key = os.environ.get('SQLALCHEMY_KEY', '')


class ApplicationStatus(enum.Enum):
    COMPLETED = "COMPLETED"
    DELETED = "DELETED"
    STARTED = "STARTED"
    SUBMITTED = "SUBMITTED"
    DOWNLOADED = "DOWNLOADED"
    ABANDONED = "ABANDONED"


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference_number = db.Column(StringEncryptedType(db.String, length=50, key=secret_key, engine=AesEngine, padding='pkcs5'), unique=True, nullable=False)
    email = db.Column(StringEncryptedType(db.String, length=500, key=secret_key, engine=AesEngine, padding='pkcs5'), nullable=False)
    user_input = db.Column(StringEncryptedType(db.String, length=100000, key=secret_key, engine=AesEngine, padding='pkcs5'))
    status = db.Column(
        db.Enum(ApplicationStatus, name='application_status'),
        default=ApplicationStatus.STARTED
    )
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(db.DateTime)
    last_page = db.Column(db.String(500))
    downloaded = db.Column(db.DateTime)
    downloadedBy = db.Column(db.String(180))
    completed = db.Column(db.DateTime)
    completedBy = db.Column(db.String(180))
    filesCreated = db.Column(db.Boolean, default=False)
    number_sessions = db.Column(db.Integer, default=0)

    def application_data(self) -> ApplicationData:
        try:
            application_data: ApplicationData = jsonpickle.decode(self.user_input)
            application_data.updated = self.updated
            return application_data
        except Exception as e:
            print(f"model error: {e}", flush=True)
            print(f"reference_number: {self.reference_number}, created: {self.created}, updated: {self.updated}", flush=True)
            print(f"data: {self.user_input}", flush=True)


class SecurityCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(StringEncryptedType(db.String, length=50, key=secret_key, engine=AesEngine, padding='pkcs5'), unique=True, nullable=False)
    email = db.Column(StringEncryptedType(db.String, length=500, key=secret_key, engine=AesEngine, padding='pkcs5'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(180), nullable=False)
    password = db.Column(db.String, nullable=False)
    passwordResetRequired = db.Column(db.Boolean, default=True)
    userType = db.Column(db.String, default="VIEWER")
    dateLastLogin = db.Column(db.String(20), nullable=True)
    code = db.Column(db.String(100), nullable=True)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    how_easy_to_complete_application = db.Column(db.String(20), nullable=True)
    any_questions_difficult_to_answer = db.Column(db.String(3), nullable=True)
    which_questions_difficult_to_answer = db.Column(db.String(5000), nullable=True)
    needed_to_call_admin_team = db.Column(db.String(3), nullable=True)
    what_did_you_need_help_with = db.Column(db.String(5000), nullable=True)
    used_doc_checker = db.Column(db.String(11), nullable=True)
    experience_of_using_doc_checker = db.Column(db.String(5000), nullable=True)
    any_other_suggestions = db.Column(db.String(5000), nullable=True)
