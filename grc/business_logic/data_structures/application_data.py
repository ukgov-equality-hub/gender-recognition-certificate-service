from grc.business_logic.data_structures.confirmation_data import ConfirmationData
from grc.business_logic.data_structures.birth_registration_data import BirthRegistrationData
from grc.business_logic.data_structures.personal_details_data import PersonalDetailsData
from grc.business_logic.data_structures.partnership_details_data import PartnershipDetailsData
from grc.business_logic.data_structures.uploads_data import UploadsData
from grc.business_logic.data_structures.submit_and_pay_data import SubmitAndPayData


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
