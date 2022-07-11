import datetime
from enum import auto
from grc.business_logic.data_structures.grc_enum import GrcEnum


class AffirmedGender(GrcEnum):
    MALE = auto()
    FEMALE = auto()


class PersonalDetailsData:
    title: str = None
    first_names: str = None
    last_name: str = None

    affirmed_gender: AffirmedGender = None

    transition_date: datetime.date = None
    statutory_declaration_date: datetime.date = None

    changed_name_to_reflect_gender: bool = None

    address_line_one: str = None
    address_line_two: str = None
    address_town_city: str = None
    address_postcode: str = None

    contact_email_address: str = None
    contact_phone_number: str = None
    contact_by_post: bool = None  # We take the postal address from the address fields above

    contact_dates_should_avoid: bool = None
    contact_dates_to_avoid: str = None

    tell_hmrc: bool = None
    national_insurance_number: str = None
