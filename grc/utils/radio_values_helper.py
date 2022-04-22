from grc.birth_registration.forms import AdoptedUKForm


def get_radio_pretty_value(formName, fieldName, value):
    if formName == 'AdoptedUKForm':
        form = AdoptedUKForm()
    else:
        return None

    for choiceId, choiceLabel in form[fieldName].choices:
        if choiceId == value:
            return choiceLabel
    return None
