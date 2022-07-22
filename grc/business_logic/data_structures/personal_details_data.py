import datetime
from enum import auto
from grc.business_logic.data_structures.grc_enum import GrcEnum
from grc.list_status import ListStatus


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
    address_country: str = None
    address_postcode: str = None

    contact_email_address: str = None
    contact_phone_number: str = None
    contact_by_post: bool = None  # We take the postal address from the address fields above

    contact_dates_should_avoid: bool = None
    contact_dates_to_avoid: str = None

    tell_hmrc: bool = None
    national_insurance_number: str = None

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
    def affirmed_gender_formatted(self) -> str: return 'Male' if self.affirmed_gender == AffirmedGender.MALE else 'Female'
    @property
    def transition_date_formatted_MMMM_YYYY(self) -> str: return self.transition_date.strftime('%B %Y')
    @property
    def transition_date_formatted_DD_MM_YYYY(self) -> str: return self.transition_date.strftime('%d/%m/%Y')
    @property
    def statutory_declaration_date_formatted_DD_MMMM_YYYY(self) -> str: return self.statutory_declaration_date.strftime('%d %B %Y')
    @property
    def statutory_declaration_date_formatted_DD_MM_YYYY(self) -> str: return self.statutory_declaration_date.strftime('%d/%m/%Y')
    @property
    def changed_name_to_reflect_gender_formatted(self) -> str: return 'Yes' if self.changed_name_to_reflect_gender else 'No'
    @property
    def contact_dates_should_avoid_formatted(self) -> str: return 'Yes' if self.contact_dates_should_avoid else 'No'
    @property
    def tell_hmrc_formatted(self) -> str: return 'Yes' if self.tell_hmrc else 'No'

    @property
    def section_status(self) -> ListStatus:
        if self.title is None or self.first_names is None or self.last_name is None:
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

        if self.contact_dates_should_avoid is None:
            return ListStatus.IN_PROGRESS

        if self.contact_dates_should_avoid:
            if self.contact_dates_to_avoid is None:
                return ListStatus.IN_PROGRESS

        if self.tell_hmrc is None:
            return ListStatus.IN_PROGRESS

        if self.tell_hmrc:
            if self.national_insurance_number is None:
                return ListStatus.IN_PROGRESS

        return ListStatus.COMPLETED
