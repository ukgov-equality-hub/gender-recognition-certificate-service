from enum import Enum, auto


class GrcEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class CurrentlyInAPartnershipEnum(GrcEnum):
    MARRIED = auto()
    CIVIL_PARTNERSHIP = auto()
    NEITHER = auto()

    @property
    def is_married(self) -> bool: return self == CurrentlyInAPartnershipEnum.MARRIED
    @property
    def is_in_civil_partnership(self) -> bool: return self == CurrentlyInAPartnershipEnum.CIVIL_PARTNERSHIP
    @property
    def is_currently_in_partnership(self) -> bool: return self.is_married or self.is_in_civil_partnership


class DocCheckerState(object):
    changed_name_to_reflect_gender: bool = None
    currently_in_a_partnership: CurrentlyInAPartnershipEnum = None
    previous_partnership_partner_died: bool = None
    previous_partnership_ended: bool = None
    plan_to_remain_in_a_partnership: bool = None
    gender_recognition_outside_uk: bool = None
