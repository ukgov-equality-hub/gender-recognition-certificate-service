from datetime import date
from dateutil.relativedelta import relativedelta

DEFAULT_TIMEOUT = 3 * 1000  # Wait a maximum of 3 seconds
TIMEOUT_FOR_SLOW_OPERATIONS = 30 * 1000  # For slow operations, wait a maximum of 30 seconds


EMAIL_ADDRESS = 'ivan.touloumbadjian@hmcts.net'
DIFFERENT_EMAIL_ADDRESS = 'grc-service-account@cabinetoffice.gov.uk'

TITLE = 'Mr'
FIRST_NAME = 'Joseph'
MIDDLE_NAMES = 'Adam Brian'
LAST_NAME = 'Bloggs'

ADDRESS_LINE_ONE = '16-20'
ADDRESS_LINE_TWO = 'Great Smith Street'
TOWN = 'London'
POSTCODE = 'SW1P 3BT'

TRANSITION_DATE_MONTH = '3'
TRANSITION_DATE_YEAR = date.today() - relativedelta(2)
TRANSITION_DATE_YEAR_INVALID = date.today() - relativedelta(3)
TRANSITION_DATE_FORMATTED = f'March {TRANSITION_DATE_YEAR}'

STATUTORY_DECLARATION_DATE_DAY = '5'
STATUTORY_DECLARATION_DATE_MONTH = '3'
STATUTORY_DECLARATION_DATE_YEAR = '2000'
STATUTORY_DECLARATION_DATE_FORMATTED = '05 March 2000'

DATES_TO_AVOID = '1st June - 2nd July\n3rd August - 4th September'

PHONE_NUMBER = '07700900000'

NATIONAL_INSURANCE_NUMBER = 'AB123456C'

BIRTH_FIRST_NAME = 'Joanna'
BIRTH_MIDDLE_NAME = 'Mary'
BIRTH_LAST_NAME = 'Bloggs'

DATE_OF_BIRTH_DAY = '3'
DATE_OF_BIRTH_MONTH = '4'
DATE_OF_BIRTH_YEAR = '1956'
DATE_OF_BIRTH_FORMATTED = '03 April 1956'

BIRTH_COUNTRY = 'France'
BIRTH_TOWN = 'London'

MOTHERS_FIRST_NAME = 'Margaret'
MOTHERS_LAST_NAME = 'Bloggs'
MOTHERS_MAIDEN_NAME = 'Jones'

FATHERS_FIRST_NAME = 'Norman'
FATHERS_LAST_NAME = 'Bloggs'

PARTNER_TITLE = 'Ms'
PARTNER_FIRST_NAME = 'Sam'
PARTNER_LAST_NAME = 'Jones'
PARTNER_POSTAL_ADDRESS = '10 Victoria Street\nLondon\nSW1H 0NB'

HELP_WITH_FEES_REFERENCE_NUMBER = 'ABC-123'
