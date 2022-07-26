from grc.models import Application


def reference_number_string(reference_number):
    trimmed_reference = reference_number.replace('-', '').replace(' ', '').upper()
    formatted_reference = trimmed_reference[0:4] + '-' + trimmed_reference[4: 8]
    return formatted_reference


def validate_reference_number(reference):
    reference = reference.replace('-', '').replace(' ', '').upper()
    record = Application.query.filter_by(reference_number=reference).first()

    if record is None:
        print("An application with reference number " + reference + " does not exist")
        return False
    else:
        return record
