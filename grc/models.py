from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
import enum

db = SQLAlchemy()


class ApplicationStatus(enum.Enum):
    COMPLETED = "COMPLETED"
    DELETED = "DELETED"
    STARTED = "STARTED"
    SUBMITTED = "SUBMITTED"
    DOWNLOADED = "DOWNLOADED"


class ListStatus(enum.Enum):
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN PROGRESS"
    NOT_STARTED = "NOT STARTED"
    CANNOT_START_YET = "CANNOT START YET"
    IN_REVIEW = "IN REVIEW"  # Value 'in progress' is used only at task list


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference_number = db.Column(db.String(8), unique=True, nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False)
    user_input = db.Column(JSON)
    status = db.Column(
        db.Enum(ApplicationStatus, name="application_status"),
        default=ApplicationStatus.STARTED,
    )
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(db.DateTime)
    downloaded = db.Column(db.DateTime)
    downloadedBy = db.Column(db.String(180))
    completed = db.Column(db.DateTime)
    completedBy = db.Column(db.String(180))

    def data(self):
        if self.user_input:
            return self.user_input
        else:
            return {
                "reference_number": self.reference_number,
                "email": self.email,
                "confirmation": {
                    "overseasCheck": "None",
                    "overseasApprovedCheck": "None",
                    "declaration": "None",
                    "progress": ListStatus.IN_PROGRESS.name,
                    "step": "startApplication.reference",
                },
                "personalDetails": {
                    "progress": ListStatus.NOT_STARTED.name,
                    "step": "personalDetails.index",
                },
                "birthRegistration": {
                    "progress": ListStatus.NOT_STARTED.name,
                    "step": "birthRegistration.index",
                },
                "partnershipDetails": {
                    "progress": ListStatus.NOT_STARTED.name,
                    "step": "partnershipDetails.index",
                },
                "medicalReports": {
                    "progress": ListStatus.CANNOT_START_YET.name,
                    "step": "upload.medicalReports",
                },
                "genderEvidence": {
                    "progress": ListStatus.CANNOT_START_YET.name,
                    "step": "upload.genderEvidence",
                },
                "nameChange": {
                    "progress": ListStatus.CANNOT_START_YET.name,
                    "step": "upload.nameChange",
                },
                "marriageDocuments": {
                    "progress": ListStatus.CANNOT_START_YET.name,
                    "step": "upload.marriageDocuments",
                },
                "statutoryDeclarations": {
                    "progress": ListStatus.CANNOT_START_YET.name,
                    "step": "upload.statutoryDeclarations",
                },
                "submitAndPay": {
                    "progress": ListStatus.CANNOT_START_YET.name,
                    "step": "submitAndPay.index",
                },
            }


class SecurityCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), unique=True, nullable=False)
    email = db.Column(db.String(180), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(180), nullable=False)
    password = db.Column(db.String, nullable=False)
    passwordResetRequired = db.Column(db.Boolean, default=True)
    userType = db.Column(db.String, default="VIEWER")
    dateLastLogin = db.Column(db.String(20), nullable=True)
    code = db.Column(db.String(100), nullable=True)
