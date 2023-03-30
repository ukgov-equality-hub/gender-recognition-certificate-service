from datetime import date
from dateutil.relativedelta import relativedelta

DEFAULT_TIMEOUT = 3 * 1000  # Wait a maximum of 3 seconds
TIMEOUT_FOR_SLOW_OPERATIONS = 30 * 1000  # For slow operations, wait a maximum of 30 seconds


EMAIL_ADDRESS = 'ivan.touloumbadjian@hmcts.net'

TITLE = 'Mr'
FIRST_NAME = 'Joseph'
MIDDLE_NAMES = 'Adam Brian'
LAST_NAME = 'Bloggs'

ADDRESS_LINE_ONE = '16-20'
ADDRESS_LINE_TWO = 'Great Smith Street'
TOWN = 'London'
POSTCODE = 'SW1P 3BT'

TRANSITION_DATE_MONTH = '3'
TRANSITION_DATE_YEAR = str((date.today() - relativedelta(years=3)).year)
TRANSITION_DATE_MONTH_INVALID = str((date.today() + relativedelta(months=1)).month)
TRANSITION_DATE_YEAR_INVALID = str((date.today() - relativedelta(years=2)).year)
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

TEST_CARD_NUMBER = '4444333322221111'
TEST_CARD_EXPIRY_MONTH = '01'
TEST_CARD_EXPIRY_YEAR = '2025'
TEST_CARDHOLDER_NAME = 'Joseph Bloggs'
TEST_CARD_CVC = '123'
TEST_CARD_COUNTRY = 'United Kingdom'
TEST_CARD_ADDRESS_LINE_1 = '16-20'
TEST_CARD_ADDRESS_LINE_2 = 'Great Smith Street'
TEST_CARD_ADDRESS_CITY = 'London'
TEST_CARD_ADDRESS_POSTCODE = 'SW1P 3BT'
