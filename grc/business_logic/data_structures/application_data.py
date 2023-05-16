from datetime import datetime
from typing import List
from grc.business_logic.data_structures.confirmation_data import ConfirmationData
from grc.business_logic.data_structures.birth_registration_data import BirthRegistrationData
from grc.business_logic.data_structures.personal_details_data import PersonalDetailsData
from grc.business_logic.data_structures.partnership_details_data import PartnershipDetailsData
from grc.business_logic.data_structures.uploads_data import UploadsData, EvidenceFile
from grc.business_logic.data_structures.submit_and_pay_data import SubmitAndPayData, HelpWithFeesType
from grc.list_status import ListStatus


def any_password_protected_files(uploads_files: List[EvidenceFile]):
    return len([file for file in uploads_files if file.password_required]) > 0


def any_duplicate_aws_file_names(uploads_files: List[EvidenceFile]):
    aws_file_names = [file.aws_file_name for file in uploads_files]
    duplicate_aws_file_names = [file_name for file_name in aws_file_names if aws_file_names.count(file_name) > 1]
    return len(duplicate_aws_file_names) > 0


class ApplicationData:
    def __new__(cls, *args, **kwargs):
        # This method has been added to address a limitation of jsonpickle.decode
        # We use the jsonpickle library to convert these python classes to/from JSON to store in the database
        # The instance-level fields are declared in the __init__ method
        # When jsonpickle.decode re-creates a class, it calls __new__, but it does not call __init__
        # We need it to call __init__ to make sure we have set up all the instance-level fields, so we call __init__ here manually
        new_instance = super().__new__(cls)
        new_instance.__init__()
        return new_instance

    def __init__(self):
        self.reference_number: str = None
        self.email_address: str = None
        self.updated: datetime = None
        self.confirmation_data: ConfirmationData = ConfirmationData()
        self.personal_details_data: PersonalDetailsData = PersonalDetailsData()
        self.birth_registration_data: BirthRegistrationData = BirthRegistrationData()
        self.partnership_details_data: PartnershipDetailsData = PartnershipDetailsData()
        self.uploads_data: UploadsData = UploadsData()
        self.submit_and_pay_data: SubmitAndPayData = SubmitAndPayData()

    def _upload_section_status(self, section):
        if len(section) == 0:
            return ListStatus.NOT_STARTED
        elif any_password_protected_files(section):
            return ListStatus.ERROR
        elif any_duplicate_aws_file_names(section):
            return ListStatus.ERROR
        else:
            return ListStatus.COMPLETED

    @property
    def reference_number_formatted(self) -> str:
        trimmed_reference = self.reference_number.replace('-', '').replace(' ', '').upper()
        formatted_reference = trimmed_reference[0: 4] + '-' + trimmed_reference[4: 8]
        return formatted_reference

    @property
    def is_uk_application(self) -> bool:
        return self.confirmation_data.gender_recognition_outside_uk == False or \
               self.confirmation_data.gender_recognition_from_approved_country == False  # == False because we want to exclude None

    @property
    def is_overseas_application(self) -> bool:
        return self.confirmation_data.gender_recognition_outside_uk and \
               self.confirmation_data.gender_recognition_from_approved_country

    @property
    def application_certificate_type(self) -> str:
        certificate_type = 'INTERIM' if self.partnership_details_data.is_interim_certificate else 'FULL'
        overseas_type = 'OVERSEAS' if self.is_overseas_application else 'STANDARD'
        return f'{certificate_type} {overseas_type} CERTIFICATE APPLICATION'

    @property
    def need_medical_reports(self) -> bool:
        return self.is_uk_application

    @property
    def need_evidence_of_living_in_gender(self) -> bool:
        return self.is_uk_application

    @property
    def need_name_change_documents(self) -> bool:
        return self.personal_details_data.changed_name_to_reflect_gender

    @property
    def need_partnership_documents(self) -> bool:
        return self.partnership_details_data.is_currently_in_partnership or \
               self.partnership_details_data.previous_partnership_partner_died or \
               self.partnership_details_data.previous_partnership_ended

    @property
    def need_overseas_documents(self) -> bool:
        return self.is_overseas_application

    @property
    def section_status_medical_reports(self) -> ListStatus:
        if self.need_medical_reports:
            return self._upload_section_status(self.uploads_data.medical_reports)
        else:
            return ListStatus.CANNOT_START_YET

    @property
    def section_status_evidence_of_living_in_gender(self) -> ListStatus:
        if self.need_evidence_of_living_in_gender:
            return self._upload_section_status(self.uploads_data.evidence_of_living_in_gender)
        else:
            return ListStatus.CANNOT_START_YET

    @property
    def section_status_name_change_documents(self) -> ListStatus:
        if self.need_name_change_documents:
            return self._upload_section_status(self.uploads_data.name_change_documents)
        else:
            return ListStatus.CANNOT_START_YET

    @property
    def section_status_partnership_documents(self) -> ListStatus:
        if self.need_partnership_documents:
            return self._upload_section_status(self.uploads_data.partnership_documents)
        else:
            return ListStatus.CANNOT_START_YET

    @property
    def section_status_overseas_documents(self) -> ListStatus:
        if self.need_overseas_documents:
            return self._upload_section_status(self.uploads_data.overseas_documents)
        else:
            return ListStatus.CANNOT_START_YET

    @property
    def section_status_statutory_declarations(self) -> ListStatus:
        return self._upload_section_status(self.uploads_data.statutory_declarations)

    @property
    def section_status_submit_and_pay_data(self) -> ListStatus:
        if self.submit_and_pay_data.is_submitted:
            return ListStatus.COMPLETED

        if self.confirmation_data.section_status != ListStatus.COMPLETED:
            return ListStatus.CANNOT_START_YET

        if self.personal_details_data.section_status != ListStatus.COMPLETED:
            return ListStatus.CANNOT_START_YET

        if self.birth_registration_data.section_status != ListStatus.COMPLETED:
            return ListStatus.CANNOT_START_YET

        if self.partnership_details_data.section_status != ListStatus.COMPLETED:
            return ListStatus.CANNOT_START_YET

        if self.need_medical_reports and self.section_status_medical_reports != ListStatus.COMPLETED:
            return ListStatus.CANNOT_START_YET

        if self.need_evidence_of_living_in_gender and self.section_status_evidence_of_living_in_gender != ListStatus.COMPLETED:
            return ListStatus.CANNOT_START_YET

        if self.need_name_change_documents and self.section_status_name_change_documents != ListStatus.COMPLETED:
            return ListStatus.CANNOT_START_YET

        if self.need_partnership_documents and self.section_status_partnership_documents != ListStatus.COMPLETED:
            return ListStatus.CANNOT_START_YET

        if self.need_overseas_documents and self.section_status_overseas_documents != ListStatus.COMPLETED:
            return ListStatus.CANNOT_START_YET

        if self.section_status_statutory_declarations != ListStatus.COMPLETED:
            return ListStatus.CANNOT_START_YET

        if self.submit_and_pay_data.applying_for_help_with_fee is None:
            return ListStatus.NOT_STARTED

        if self.submit_and_pay_data.applying_for_help_with_fee:
            if self.submit_and_pay_data.how_applying_for_help_with_fees is None:
                return ListStatus.IN_PROGRESS

            if self.submit_and_pay_data.how_applying_for_help_with_fees == HelpWithFeesType.USING_ONLINE_SERVICE:
                if self.submit_and_pay_data.help_with_fees_reference_number is None:
                    return ListStatus.IN_PROGRESS

        return ListStatus.IN_REVIEW
