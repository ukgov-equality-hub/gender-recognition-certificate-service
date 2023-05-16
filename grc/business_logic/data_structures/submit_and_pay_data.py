from enum import auto
from grc.business_logic.data_structures.grc_enum import GrcEnum


class HelpWithFeesType(GrcEnum):
    USING_ONLINE_SERVICE = auto()
    USING_EX160_FORM = auto()


class SubmitAndPayData:
    def __init__(self):
        self.applying_for_help_with_fee: bool = None

        self.how_applying_for_help_with_fees: HelpWithFeesType = None
        self.help_with_fees_reference_number: str = None

        self.declaration: bool = None

        self.gov_pay_payment_id: str = None
        self.gov_pay_uuid: str = None
        self.gov_pay_payment_details: str = None

        self.is_submitted: bool = False

    @property
    def applying_for_help_with_fee_formatted(self) -> str:
        return 'Help' if self.applying_for_help_with_fee else 'Online'

    @property
    def how_applying_for_help_with_fees_formatted(self) -> str:
        return ('Using the online service'
                if self.how_applying_for_help_with_fees == HelpWithFeesType.USING_ONLINE_SERVICE
                else 'Using the EX160 form')

    @property
    def is_using_online_service(self) -> bool:
        return self.how_applying_for_help_with_fees == HelpWithFeesType.USING_ONLINE_SERVICE

    @property
    def is_using_ex160_form(self) -> bool:
        return self.how_applying_for_help_with_fees == HelpWithFeesType.USING_EX160_FORM
