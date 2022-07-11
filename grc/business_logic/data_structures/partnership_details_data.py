from enum import auto
from grc.business_logic.data_structures.grc_enum import GrcEnum


class CurrentlyInAPartnershipEnum(GrcEnum):
    MARRIED = auto()
    CIVIL_PARTNERSHIP = auto()
    NEITHER = auto()


class PartnershipDetailsData:
    currently_in_a_partnership: CurrentlyInAPartnershipEnum = None

    plan_to_remain_in_a_partnership: bool = None
    partner_agrees: bool = None
    confirm_understood_interim_certificate: bool = None

    previous_partnership_partner_died: bool = None
    previous_partnership_ended: bool = None
