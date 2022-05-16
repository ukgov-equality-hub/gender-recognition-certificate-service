import random, string
from grc.models import db, Application


def reference_number_generator(email):
    ref_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    application_record = Application.query.filter_by(reference_number=ref_number).first()

    if application_record is None:
        try:
            record = Application(reference_number=ref_number, email=email)
            db.session.add(record)
            db.session.commit()
            return ref_number
        except ValueError:
            print("Oops!  Something went wrong.")
    else:
        print("Reference number exists, trying again")
        reference_number_generator(email)


def reference_number_string(reference_number):
    trimmed_reference = reference_number.replace('-', '').replace(' ', '').upper()
    formatted_reference = trimmed_reference[0:4] + '-' + trimmed_reference[4: 8]
    return formatted_reference


def validate_reference_number(reference):
    reference = reference.replace('-', '').replace(' ', '').upper()
    record = Application.query.filter_by(reference_number=reference).first()

    if record is None:
        print("An application with " + reference + " reference number does not exist")
        return False
    else:
        return record
