from grc.list_status import ListStatus


class ConfirmationData:
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
        self.gender_recognition_outside_uk: bool = None
        self.gender_recognition_from_approved_country: bool = None
        self.consent_to_GRO_contact: bool = None

    @property
    def gender_recognition_outside_uk_formatted(self) -> str:
        return 'Yes' if self.gender_recognition_outside_uk else 'No'

    @property
    def gender_recognition_from_approved_country_formatted(self) -> str:
        return 'Yes' if self.gender_recognition_from_approved_country else 'No'

    @property
    def consent_to_GRO_contact_formatted(self) -> str:
        return 'Yes' if self.consent_to_GRO_contact else 'No'

    @property
    def section_status(self) -> ListStatus:
        if self.gender_recognition_outside_uk is None:
            return ListStatus.NOT_STARTED

        if self.gender_recognition_outside_uk:
            if self.gender_recognition_from_approved_country is None:
                return ListStatus.IN_PROGRESS

        if self.consent_to_GRO_contact is None:
            return ListStatus.IN_PROGRESS

        return ListStatus.COMPLETED
