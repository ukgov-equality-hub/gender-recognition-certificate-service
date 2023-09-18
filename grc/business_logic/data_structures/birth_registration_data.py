import datetime
from enum import auto
from grc.business_logic.data_structures.grc_enum import GrcEnum
from grc.list_status import ListStatus


class AdoptedInTheUkEnum(GrcEnum):
    ADOPTED_IN_THE_UK_YES = auto()
    ADOPTED_IN_THE_UK_NO = auto()
    ADOPTED_IN_THE_UK_DO_NOT_KNOW = auto()


class BirthRegistrationData:
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
        self.first_name: str = None
        self.middle_names: str = None
        self.last_name: str = None

        self.date_of_birth: datetime.date = None

        self.birth_registered_in_uk: bool = None
        self.country_of_birth: str = None
        self.town_city_of_birth: str = None

        self.mothers_first_name: str = None
        self.mothers_last_name: str = None
        self.mothers_maiden_name: str = None

        self.fathers_name_on_birth_certificate: bool = None
        self.fathers_first_name: str = None
        self.fathers_last_name: str = None

        self.adopted: bool = None
        self.adopted_in_the_uk: AdoptedInTheUkEnum = None

        self.forces_registration: bool = None

    @property
    def full_name(self) -> str:
        return (
            self.first_name + ' ' +
            (self.middle_names + ' ' if self.middle_names else '') +
            self.last_name
        )

    @property
    def middle_names_or_empty_string(self) -> str:
        return self.middle_names if self.middle_names else ''

    @property
    def date_of_birth_formatted_DD_MMMM_YYYY(self) -> str:
        return self.date_of_birth.strftime('%d %B %Y')

    @property
    def date_of_birth_formatted_DD_MM_YYYY_dots(self) -> str:
        return self.date_of_birth.strftime('%d.%m.%Y')

    @property
    def birth_registered_in_uk_formatted(self) -> str:
        return 'Yes' if self.birth_registered_in_uk else 'No'

    @property
    def fathers_name_on_birth_certificate_formatted(self) -> str:
        return 'Yes' if self.fathers_name_on_birth_certificate else 'No'

    @property
    def adopted_formatted(self) -> str:
        return 'Yes' if self.adopted else 'No'

    @property
    def adopted_in_the_uk_formatted(self) -> str:
        if self.adopted_in_the_uk == AdoptedInTheUkEnum.ADOPTED_IN_THE_UK_YES:
            return 'Yes'
        elif self.adopted_in_the_uk == AdoptedInTheUkEnum.ADOPTED_IN_THE_UK_NO:
            return 'No'
        elif self.adopted_in_the_uk == AdoptedInTheUkEnum.ADOPTED_IN_THE_UK_DO_NOT_KNOW:
            return "I don't know"

    @property
    def forces_registration_formatted(self) -> str:
        return 'Yes' if self.forces_registration else 'No'

    @property
    def section_status(self) -> ListStatus:
        if self.first_name is None or self.last_name is None:
            return ListStatus.NOT_STARTED

        if self.date_of_birth is None:
            return ListStatus.IN_PROGRESS

        if self.birth_registered_in_uk is None:
            return ListStatus.IN_PROGRESS

        if self.birth_registered_in_uk:
            if self.town_city_of_birth is None:
                return ListStatus.IN_PROGRESS

            if self.mothers_first_name is None or self.mothers_last_name is None or self.mothers_maiden_name is None:
                return ListStatus.IN_PROGRESS

            if self.fathers_name_on_birth_certificate is None:
                return ListStatus.IN_PROGRESS

            if self.fathers_name_on_birth_certificate:
                if self.fathers_first_name is None or self.fathers_last_name is None:
                    return ListStatus.IN_PROGRESS

            if self.adopted is None:
                return ListStatus.IN_PROGRESS

            if self.adopted:
                if self.adopted_in_the_uk is None:
                    return ListStatus.IN_PROGRESS

            if self.forces_registration is None:
                return ListStatus.IN_PROGRESS

        else:
            if self.country_of_birth is None:
                return ListStatus.IN_PROGRESS

        return ListStatus.COMPLETED
