import random
import string
import datetime
import jsonpickle
from flask import session
from grc.models import Application, db
from grc.business_logic.data_structures.application_data import ApplicationData


class DataStore:
    @staticmethod
    def create_new_application(email_address: str) -> ApplicationData:
        reference_number = DataStore.generate_unallocated_reference_number()

        # Create row in database
        application_record = Application(
            reference_number=reference_number,
            email=email_address
        )
        db.session.add(application_record)
        db.session.commit()

        # Add user_input
        application_data = ApplicationData()
        application_data.reference_number = reference_number
        application_data.email_address = email_address

        DataStore.save_application(application_data)

        return application_data

    @staticmethod
    def load_application_by_session_reference_number() -> ApplicationData:
        return DataStore.load_application(session['reference_number'])

    @staticmethod
    def load_application(reference_number: str) -> ApplicationData:
        compacted_reference = DataStore.compact_reference(reference_number)

        application_record: Application = Application.query.filter_by(
            reference_number=compacted_reference
        ).first()

        if application_record is None:
            raise ValueError('This reference number was not found')

        return application_record.application_data()

    @staticmethod
    def save_application(application_data: ApplicationData) -> None:
        application_record: Application = Application.query.filter_by(
            reference_number=application_data.reference_number
        ).first()

        user_input: str = jsonpickle.encode(application_data)

        application_record.user_input = user_input
        application_record.updated = datetime.datetime.now()
        db.session.commit()

    @staticmethod
    def compact_reference(reference_number: str) -> str:
        compacted_reference = reference_number.replace('-', '').replace(' ', '').upper()
        return compacted_reference

    @staticmethod
    def format_reference(reference_number: str) -> str:
        compacted_reference = DataStore.compact_reference(reference_number)
        formatted_reference = compacted_reference[0:4] + '-' + compacted_reference[4: 8]
        return formatted_reference

    @staticmethod
    def generate_unallocated_reference_number() -> str:
        while True:
            possible_reference_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

            application_record = Application.query.filter_by(reference_number=possible_reference_number).first()
            if application_record is None:
                return possible_reference_number


