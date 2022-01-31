import random, string
from datetime import datetime, timedelta
from grc.models import db, Application


def reference_number_generator(email):
    """An 8 alphanumeric characters code generator as string to be used as
    an application reference number
    """

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

def reference_number_string(reference_number):
    """It returns a visual representation of reference number
    """

    return reference_number[0:4] + "-" + reference_number[4:8]


def ValidateReferenceNumber(reference):
    """Validate reference number
    """

    reference = reference.replace("-", "").upper()
    record = Application.query.filter_by(reference_number=reference).first()

    if record is None:
        print ("An application with " + reference + " reference number does not exist")
        return False
    else:
        return record



