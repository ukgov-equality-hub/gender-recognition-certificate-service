import random, string
from grc.models import db, Application


def reference_number_generator(email):
    email_record = Application.query.filter_by(email=email).first()

    if email_record is None:
        ref_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        application_record = Application.query.filter_by(reference_number=ref_number).first()

        if application_record is None:
            try:
                record = Application(reference_number=ref_number,email=email)
                db.session.add(record)
                db.session.commit()
                return ref_number
            except ValueError:
                print("Oops!  Something went wrong.")
        else:
            print("Reference number exists, trying again")
            reference_number_generator(email)
    else:
        return False


def reference_number_string(reference_number):
    return reference_number[0:4] + '-' + reference_number[4: 8]


def validate_reference_number(reference):
    reference = reference.replace('-', '').upper()
    record = Application.query.filter_by(reference_number=reference).first()

    if record is None:
        print("An application with " + reference + " reference number does not exist")
        return False
    else:
        return record
