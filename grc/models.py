from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import json
from datetime import datetime
import enum

db = SQLAlchemy()

class ApplicationStatus(enum.Enum):
    STARTED = "STARTED"
    SUBMITTED = "SUBMITTED"
    COMPLETED = "COMPLETED"
    DELETED = "DELETED"



class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference_number = db.Column(db.String(8), unique=True, nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False)
    user_input = db.Column(JSON)
    status = db.Column(db.Enum(ApplicationStatus, name="application_status"), default=ApplicationStatus.STARTED)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(db.DateTime)

    def data(self):
        if self.user_input:
            return self.user_input
        else:
            print(111111111, self.reference_number)
            return {
                "reference_number": self.reference_number,
                "email": self.email,
                "confirmation": {
                    "overseasCheck": "None",
                    "overseasApprovedCheck":"None",
                    "declaration": "None"
                }
            }


class SecurityCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), unique=True, nullable=False)
    email = db.Column(db.String(180), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

