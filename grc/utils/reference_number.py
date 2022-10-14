from grc.models import Application


def reference_number_string(reference_number):
    trimmed_reference = reference_number.replace('-', '').replace(' ', '').upper()
    formatted_reference = trimmed_reference[0: 4] + '-' + trimmed_reference[4: 8]
    return formatted_reference


def validate_reference_number(reference):
    reference = reference.replace('-', '').replace(' ', '').upper()
    application = Application.query.filter_by(reference_number=reference).first()

    if application is None:
        print(f"An application with reference number {reference} does not exist", flush=True)
        return False
    else:
        return application
