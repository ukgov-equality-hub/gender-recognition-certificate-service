from enum import auto
from grc.business_logic.data_structures.grc_enum import GrcEnum


class HelpWithFeesType(GrcEnum):
    USING_ONLINE_SERVICE = auto()
    USING_EX160_FORM = auto()


class SubmitAndPayData:
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
