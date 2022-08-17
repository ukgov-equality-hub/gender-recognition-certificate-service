from typing import List
from grc.business_logic.data_structures.confirmation_data import ConfirmationData
from grc.business_logic.data_structures.birth_registration_data import BirthRegistrationData
from grc.business_logic.data_structures.personal_details_data import PersonalDetailsData
from grc.business_logic.data_structures.partnership_details_data import PartnershipDetailsData
from grc.business_logic.data_structures.uploads_data import UploadsData, EvidenceFile
from grc.business_logic.data_structures.submit_and_pay_data import SubmitAndPayData, HelpWithFeesType
from grc.list_status import ListStatus


class ApplicationData:
    reference_number: str = None
    email_address: str = None

    confirmation_data: ConfirmationData
    personal_details_data: PersonalDetailsData
    birth_registration_data: BirthRegistrationData
    partnership_details_data: PartnershipDetailsData
    uploads_data: UploadsData
    submit_and_pay_data: SubmitAndPayData

    def __init__(self):
        self.confirmation_data = ConfirmationData()
        self.personal_details_data = PersonalDetailsData()
        self.birth_registration_data = BirthRegistrationData()
        self.partnership_details_data = PartnershipDetailsData()
        self.uploads_data = UploadsData()
        self.submit_and_pay_data = SubmitAndPayData()

    @property
    def is_uk_application(self) -> bool:
        return self.confirmation_data.gender_recognition_outside_uk == False or \
               self.confirmation_data.gender_recognition_from_approved_country == False  # == False because we want to exclude None

    @property
    def is_overseas_application(self) -> bool:
        return self.confirmation_data.gender_recognition_outside_uk and \
               self.confirmation_data.gender_recognition_from_approved_country

    @property
    def need_medical_reports(self) -> bool: return self.is_uk_application
    @property
    def need_evidence_of_living_in_gender(self) -> bool: return self.is_uk_application
    @property
    def need_name_change_documents(self) -> bool: return self.personal_details_data.changed_name_to_reflect_gender
    @property
    def need_partnership_documents(self) -> bool:
        return self.partnership_details_data.is_currently_in_partnership or \
               self.partnership_details_data.previous_partnership_partner_died or \
               self.partnership_details_data.previous_partnership_ended
    @property
    def need_overseas_documents(self) -> bool: return self.is_overseas_application

    @property
    def section_status_medical_reports(self) -> ListStatus:
        if self.need_medical_reports:
            if len(self.uploads_data.medical_reports) == 0:
                return ListStatus.NOT_STARTED
            elif any_duplicate_aws_file_names(self.uploads_data.medical_reports):
                return ListStatus.ERROR
            else:
                return ListStatus.COMPLETED
        else:
            return ListStatus.CANNOT_START_YET

    @property
    def section_status_evidence_of_living_in_gender(self) -> ListStatus:
        if self.need_evidence_of_living_in_gender:
            if len(self.uploads_data.evidence_of_living_in_gender) == 0:
                return ListStatus.NOT_STARTED
            elif any_duplicate_aws_file_names(self.uploads_data.evidence_of_living_in_gender):
                return ListStatus.ERROR
            else:
                return ListStatus.COMPLETED
        else:
            return ListStatus.CANNOT_START_YET

    @property
    def section_status_name_change_documents(self) -> ListStatus:
        if self.need_name_change_documents:
            if len(self.uploads_data.name_change_documents) == 0:
                return ListStatus.NOT_STARTED
            elif any_duplicate_aws_file_names(self.uploads_data.name_change_documents):
                return ListStatus.ERROR
            else:
                return ListStatus.COMPLETED
        else:
            return ListStatus.CANNOT_START_YET

    @property
    def section_status_partnership_documents(self) -> ListStatus:
        if self.need_partnership_documents:
            if len(self.uploads_data.partnership_documents) == 0:
                return ListStatus.NOT_STARTED
            elif any_duplicate_aws_file_names(self.uploads_data.partnership_documents):
                return ListStatus.ERROR
            else:
                return ListStatus.COMPLETED
        else:
            return ListStatus.CANNOT_START_YET

    @property
    def section_status_overseas_documents(self) -> ListStatus:
        if self.need_overseas_documents:
            if len(self.uploads_data.overseas_documents) == 0:
                return ListStatus.NOT_STARTED
            elif any_duplicate_aws_file_names(self.uploads_data.overseas_documents):
                return ListStatus.ERROR
            else:
                return ListStatus.COMPLETED
        else:
            return ListStatus.CANNOT_START_YET

    @property
    def section_status_statutory_declarations(self) -> ListStatus:
        if len(self.uploads_data.statutory_declarations) == 0:
            return ListStatus.NOT_STARTED
        elif any_duplicate_aws_file_names(self.uploads_data.statutory_declarations):
            return ListStatus.ERROR
        else:
            return ListStatus.COMPLETED

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


def any_duplicate_aws_file_names(uploads_files: List[EvidenceFile]):
    aws_file_names = [file.aws_file_name for file in uploads_files]
    duplicate_aws_file_names = [file_name for file_name in aws_file_names if aws_file_names.count(file_name) > 1]
    any_duplicates = len(duplicate_aws_file_names) > 0
    return any_duplicates
