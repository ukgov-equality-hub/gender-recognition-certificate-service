import datetime
from enum import auto
from grc.business_logic.data_structures.grc_enum import GrcEnum
from grc.list_status import ListStatus


class AffirmedGender(GrcEnum):
    MALE = auto()
    FEMALE = auto()


class ContactDatesAvoid(GrcEnum):
    SINGLE_DATE = auto()
    DATE_RANGE = auto()
    NO_DATES = auto()


class DateRange:
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
        self.index: int = None
        self.from_date: datetime.date = None
        self.to_date: datetime.date = None


class PersonalDetailsData:
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
        self.title: str = None
        self.first_name: str = None
        self.middle_names: str = None
        self.last_name: str = None

        self.affirmed_gender: AffirmedGender = None

        self.transition_date: datetime.date = None
        self.statutory_declaration_date: datetime.date = None

        self.changed_name_to_reflect_gender: bool = None

        self.address_line_one: str = None
        self.address_line_two: str = None
        self.address_town_city: str = None
        self.address_country: str = None
        self.address_postcode: str = None

        self.contact_email_address: str = None
        self.contact_phone_number: str = None
        self.contact_by_post: bool = None  # We take the postal address from the address fields above

        self.contact_dates_should_avoid: bool = None
        self.contact_dates_to_avoid: str = None
        self.contact_dates_to_avoid_option: ContactDatesAvoid = None
        self.contact_date_to_avoid: datetime.date = None
        self.contact_date_ranges_to_avoid: [DateRange] = None

        self.tell_hmrc: bool = None
        self.national_insurance_number: str = None


    @property
    def full_name(self) -> str:
        return (
            self.title + ' ' +
            self.first_name + ' ' +
            (self.middle_names + ' ' if self.middle_names else '') +
            self.last_name
        )

    @property
    def middle_names_or_empty_string(self) -> str:
        return self.middle_names if self.middle_names else ''

    @property
    def address_comma_separated(self) -> str:
        return (
            self.address_line_one + ', ' +
            ((self.address_line_two + ', ') if self.address_line_two else '') +
            self.address_town_city + ', ' +
            ((self.address_country + ', ') if self.address_country else '') +
            self.address_postcode
        )

    @property
    def address_with_line_breaks(self) -> str:
        return (
            self.address_line_one + '\n' +
            ((self.address_line_two + '\n') if self.address_line_two else '') +
            self.address_town_city + '\n' +
            ((self.address_country + '\n') if self.address_country else '') +
            self.address_postcode
        )

    @property
    def affirmed_gender_formatted(self) -> str:
        return 'Male' if self.affirmed_gender == AffirmedGender.MALE else 'Female'

    @property
    def transition_date_formatted_MMMM_YYYY(self) -> str:
        return self.transition_date.strftime('%B %Y')

    @property
    def transition_date_formatted_DD_MM_YYYY(self) -> str:
        return self.transition_date.strftime('%d/%m/%Y')

    @property
    def statutory_declaration_date_formatted_DD_MMMM_YYYY(self) -> str:
        return self.statutory_declaration_date.strftime('%d %B %Y')

    @property
    def statutory_declaration_date_formatted_DD_MM_YYYY(self) -> str:
        return self.statutory_declaration_date.strftime('%d/%m/%Y')

    @property
    def changed_name_to_reflect_gender_formatted(self) -> str:
        return 'Yes' if self.changed_name_to_reflect_gender else 'No'

    @property
    def contact_dates_should_avoid_formatted(self) -> str:
        return 'Yes' if self.contact_dates_should_avoid else 'No'

    @property
    def contact_dates_to_avoid_option_bool(self) -> bool:
        return False if self.contact_dates_to_avoid_option == ContactDatesAvoid.NO_DATES else True

    @property
    def contact_dates_to_avoid_option_formatted(self) -> str:
        return 'No' if self.contact_dates_to_avoid_option == ContactDatesAvoid.NO_DATES else 'Yes'

    @property
    def contact_date_to_avoid_formatted_DD_MM_YYYY(self) -> str:
        return self.contact_date_to_avoid.strftime('%d/%m/%Y')

    @property
    def contact_date_ranges_to_avoid_formatted_DD_MM_YYYY(self) -> (str, str):
        return ((date_range.from_date.strftime('%d/%m/%Y'), date_range.to_date.strftime('%d/%m/%Y'))
                for date_range in self.contact_date_ranges_to_avoid)

    @property
    def tell_hmrc_formatted(self) -> str:
        return 'Yes' if self.tell_hmrc else 'No'

    @property
    def section_status(self) -> ListStatus:
        if self.title is None or self.first_name is None or self.last_name is None:
            return ListStatus.NOT_STARTED

        if self.affirmed_gender is None:
            return ListStatus.IN_PROGRESS

        if self.transition_date is None:
            return ListStatus.IN_PROGRESS

        if self.statutory_declaration_date is None:
            return ListStatus.IN_PROGRESS

        if self.changed_name_to_reflect_gender is None:
            return ListStatus.IN_PROGRESS

        if self.address_line_one is None or self.address_town_city is None or self.address_country is None or self.address_postcode is None:
            return ListStatus.IN_PROGRESS

        if self.contact_email_address is None and self.contact_phone_number is None and self.contact_by_post is None:
            return ListStatus.IN_PROGRESS

        if self.contact_dates_should_avoid is None and self.contact_dates_to_avoid_option is None:
            return ListStatus.IN_PROGRESS

        if self.contact_dates_should_avoid:
            if self.contact_dates_to_avoid is None:
                return ListStatus.IN_PROGRESS

        if self.contact_dates_to_avoid_option and self.contact_dates_to_avoid_option != ContactDatesAvoid.NO_DATES:
            if self.contact_date_to_avoid is None and self.contact_date_ranges_to_avoid is None:
                return ListStatus.IN_PROGRESS

        if self.tell_hmrc is None:
            return ListStatus.IN_PROGRESS

        if self.tell_hmrc:
            if self.national_insurance_number is None:
                return ListStatus.IN_PROGRESS

        return ListStatus.COMPLETED

    def remove_old_contact_dates_to_avoid_data(self):
        self.contact_dates_should_avoid = None
        self.contact_dates_to_avoid = None