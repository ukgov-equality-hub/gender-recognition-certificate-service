import datetime
from enum import auto
from grc.business_logic.data_structures.grc_enum import GrcEnum


class AdoptedInTheUkEnum(GrcEnum):
    ADOPTED_IN_THE_UK_YES = auto()
    ADOPTED_IN_THE_UK_NO = auto()
    ADOPTED_IN_THE_UK_DO_NOT_KNOW = auto()


class BirthRegistrationData:
    first_name: str = None
    middle_names: str = None
    last_name: str = None

    date_of_birth: datetime.date = None

    birth_registered_in_uk: bool = None
    country_of_birth: str = None
    town_city_of_birth: str = None

    mothers_first_name: str = None
    mothers_last_name: str = None
    mothers_maiden_name: str = None

    fathers_name_on_birth_certificate: bool = None
    fathers_first_name: str = None
    fathers_last_name: str = None

    adopted: bool = None
    adopted_in_the_uk: AdoptedInTheUkEnum = None

    forces_registration: bool = None
