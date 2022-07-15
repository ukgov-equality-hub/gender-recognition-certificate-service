from grc.list_status import ListStatus


class ConfirmationData:
    gender_recognition_outside_uk: bool = None
    gender_recognition_from_approved_country: bool = None
    consent_to_GRO_contact: bool = None

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
