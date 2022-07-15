from enum import auto
from grc.business_logic.data_structures.grc_enum import GrcEnum


class HelpWithFeesType(GrcEnum):
    USING_ONLINE_SERVICE = auto()
    USING_EX160_FORM = auto()


class SubmitAndPayData:
    applying_for_help_with_fee: bool = None

    how_applying_for_help_with_fees: HelpWithFeesType = None
    help_with_fees_reference_number: str = None

    declaration: bool = None

    gov_pay_payment_id: str = None
    gov_pay_uuid: str = None
    gov_pay_payment_details: str = None

    is_submitted: bool = False