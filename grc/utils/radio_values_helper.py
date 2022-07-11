from grc.business_logic.data_structures.birth_registration_data import AdoptedInTheUkEnum


def get_radio_pretty_value(formName, fieldName, value):
    if formName == 'AdoptedUKForm':
        if value in ['Yes', AdoptedInTheUkEnum.ADOPTED_IN_THE_UK_YES]:
            return 'Yes'
        if value in ['No', AdoptedInTheUkEnum.ADOPTED_IN_THE_UK_NO]:
            return 'No'
        if value in ["DO_NOT_KNOW", AdoptedInTheUkEnum.ADOPTED_IN_THE_UK_DO_NOT_KNOW]:
            return "I don't know"
    else:
        return None
