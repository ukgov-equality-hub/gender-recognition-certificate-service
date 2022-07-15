from enum import auto
from grc.business_logic.data_structures.grc_enum import GrcEnum
from grc.list_status import ListStatus


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

    @property
    def is_married(self) -> bool: return self.currently_in_a_partnership == CurrentlyInAPartnershipEnum.MARRIED
    @property
    def is_in_civil_partnership(self) -> bool: return self.currently_in_a_partnership == CurrentlyInAPartnershipEnum.CIVIL_PARTNERSHIP
    @property
    def is_currently_in_partnership(self) -> bool: return self.is_married or self.is_in_civil_partnership
    @property
    def is_not_in_partnership(self) -> bool: return not self.is_currently_in_partnership

    @property
    def currently_in_a_partnership_formatted(self) -> str:
        if self.currently_in_a_partnership == CurrentlyInAPartnershipEnum.MARRIED: return 'Married'
        if self.currently_in_a_partnership == CurrentlyInAPartnershipEnum.CIVIL_PARTNERSHIP: return 'Civil partnership'
        if self.currently_in_a_partnership == CurrentlyInAPartnershipEnum.NEITHER: return 'Neither'
    @property
    def plan_to_remain_in_a_partnership_formatted(self) -> str: return 'Yes' if self.plan_to_remain_in_a_partnership else 'No'
    @property
    def partner_agrees_formatted(self) -> str: return 'Yes' if self.partner_agrees else 'No'
    @property
    def previous_partnership_partner_died_formatted(self) -> str: return 'Yes' if self.previous_partnership_partner_died else 'No'
    @property
    def confirm_understood_interim_certificate_formatted(self) -> str: return 'Yes' if self.confirm_understood_interim_certificate else 'No'
    @property
    def previous_partnership_ended_formatted(self) -> str: return 'Yes' if self.previous_partnership_ended else 'No'
    @property
    def is_interim_certificate(self) -> bool:
        return self.is_currently_in_partnership and \
               (self.plan_to_remain_in_a_partnership == False or self.partner_agrees == False)

    @property
    def section_status(self) -> ListStatus:
        if self.currently_in_a_partnership is None:
            return ListStatus.NOT_STARTED

        if self.is_currently_in_partnership:
            if self.plan_to_remain_in_a_partnership is None:
                return ListStatus.IN_PROGRESS

            if self.plan_to_remain_in_a_partnership:
                if self.partner_agrees is None:
                    return ListStatus.IN_PROGRESS

            if self.plan_to_remain_in_a_partnership == False or self.partner_agrees == False:
                if self.confirm_understood_interim_certificate is None:
                    return ListStatus.IN_PROGRESS

        elif self.is_not_in_partnership:
            if self.previous_partnership_partner_died is None:
                return ListStatus.IN_PROGRESS

            if self.previous_partnership_ended is None:
                return ListStatus.IN_PROGRESS

        return ListStatus.COMPLETED
