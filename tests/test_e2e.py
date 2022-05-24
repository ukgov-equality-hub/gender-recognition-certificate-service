import os
import asyncio
from playwright.async_api import async_playwright
from tests.helpers.e2e_assert_helpers import AssertHelpers
from tests.helpers.e2e_page_helpers import PageHelpers


"""
To setup on docker container:
pip install playwright pytest-playwright asyncio
playwright install
apt-get install -y gstreamer1.0-libav libnss3-tools libatk-bridge2.0-0 libcups2-dev libxkbcommon-x11-0 libxcomposite-dev libxrandr2 libgbm-dev libgtk-3-0

To setup locally:
pip install playwright pytest-playwright asyncio
pip install -e .
playwright install --with-deps

To run test locally in debug mode:
PWDEBUG=1 pytest -s
"""


TEST_URL = os.getenv('TEST_URL', 'http://localhost:5000')
print('Running tests on %s' % TEST_URL)

EMAIL_ADDRESS = 'test@example.com'
DIFFERENT_EMAIL_ADDRESS = 'different@example.com'

TITLE = 'Mr'
FIRST_NAME = 'Joseph'
LAST_NAME = 'Bloggs'

ADDRESS_LINE_ONE = '16-20'
ADDRESS_LINE_TWO = 'Great Smith Street'
TOWN = 'London'
POSTCODE = 'SW1P 3BT'

TRANSITION_DATE_MONTH = '3'
TRANSITION_DATE_YEAR = '2000'

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


async def run_script_for_browser(browser_type):
    browser = await browser_type.launch()
    page = await browser.new_page()
    page.set_default_timeout(3000)  # Wait a maximum of 3 seconds

    helpers = PageHelpers(page)
    asserts = AssertHelpers(page, helpers, TEST_URL)

    # Open homepage ("Email address")
    await page.goto(TEST_URL)

    # ------------------------------------------------
    # ---- Homepage / Email address page
    # ------------------------------------------------
    await asserts.url('/')
    await asserts.accessibility()
    assert await page.inner_text('a.govuk-header__link.govuk-header__link--service-name') == 'Apply for a Gender Recognition Certificate'
    await asserts.h1('Email address')
    await asserts.number_of_errors(0)

    # Don't enter an Email Address, click Continue button, see an error message
    await helpers.fill_textbox(field='email', value='')
    await helpers.click_button('Continue')
    await asserts.url('/')
    await asserts.accessibility(page_description='No email address entered')
    await asserts.h1('Email address')
    await asserts.number_of_errors(1)
    await asserts.error(field='email', message='Enter your email address')

    # Enter an invalid Email Address, click Continue button, see an error message
    await helpers.fill_textbox(field='email', value='invalid-email-address')
    await helpers.click_button('Continue')
    await asserts.url('/')
    await asserts.accessibility(page_description='Invalid email address entered')
    await asserts.h1('Email address')
    await asserts.number_of_errors(1)
    await asserts.error(field='email', message='Enter a valid email address')

    # Enter a valid Email Address, click Continue button, see the Security Code page
    await helpers.fill_textbox(field='email', value=EMAIL_ADDRESS)
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Security Code page
    # ------------------------------------------------
    await asserts.url('/email-confirmation')
    await asserts.accessibility()
    await asserts.h1('Enter security code')
    await asserts.number_of_errors(0)

    # Don't enter a Security Code, click Continue button, see an error message
    await helpers.fill_textbox(field='code', value='')
    await helpers.click_button('Continue')
    await asserts.url('/email-confirmation')
    await asserts.accessibility(page_description='No security code entered')
    await asserts.h1('Enter security code')
    await asserts.number_of_errors(1)
    await asserts.error(field='code', message='Enter a security code')

    # Enter an invalid Security Code, click Continue button, see an error message
    await helpers.fill_textbox(field='code', value='4444')  # Note: Don't use a 5-digit code, otherwise this test will break once every 10,000 runs!
    await helpers.click_button('Continue')
    await asserts.url('/email-confirmation')
    await asserts.accessibility(page_description='Invalid security code entered')
    await asserts.h1('Enter security code')
    await asserts.number_of_errors(1)
    await asserts.error(field='code', message='Enter the security code that we emailed you')

    # Enter a valid Security Code, click Continue button
    await helpers.fill_textbox(field='code', value='11111')
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Is First Visit page
    # ------------------------------------------------
    await asserts.url('/is-first-visit')
    await asserts.accessibility()
    await asserts.h1('Have you already started an application?')
    await asserts.number_of_errors(0)

    # Don't choose any radio option
    await helpers.click_button('Continue')
    await asserts.url('/is-first-visit')
    await asserts.accessibility()
    await asserts.h1('Have you already started an application?')
    await asserts.number_of_errors(1)
    await asserts.error(field='isFirstVisit', message='Select if you have already started an application')

    # Choose the "Yes, and I have my reference number" option, but don't enter a reference
    await helpers.check_radio(field='isFirstVisit', value='HAS_REFERENCE')
    await helpers.click_button('Continue')
    await asserts.url('/is-first-visit')
    await asserts.accessibility()
    await asserts.h1('Have you already started an application?')
    await asserts.number_of_errors(1)
    await asserts.error(field='reference', message='Enter a reference number')

    # Choose the "Yes, and I have my reference number" option, but enter an invalid reference
    await helpers.check_radio(field='isFirstVisit', value='HAS_REFERENCE')
    await helpers.fill_textbox(field='reference', value='INVA-LID')
    await helpers.click_button('Continue')
    await asserts.url('/is-first-visit')
    await asserts.accessibility()
    await asserts.h1('Have you already started an application?')
    await asserts.number_of_errors(1)
    await asserts.error(field='reference', message='Enter a valid reference number')

    # Choose the "No" (this is my first visit) option
    await helpers.check_radio(field='isFirstVisit', value='FIRST_VISIT')
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Reference Number page
    # ------------------------------------------------
    await asserts.url('/reference-number')
    await asserts.accessibility()
    await asserts.h1('Your reference number')
    await asserts.number_of_errors(0)

    # Copy reference number so we can use it later
    reference_number_on_reference_number_page = await page.inner_text('#reference-number')
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Overseas Check page
    # ------------------------------------------------
    await asserts.url('/overseas-check')
    await asserts.accessibility()
    await asserts.h1('Have you ever been issued a Gender Recognition Certificate (or its equivalent) in another country?')
    await asserts.number_of_errors(0)

    # Click "Back" to return to the Reference Number page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Reference Number page
    # ------------------------------------------------
    await asserts.url('/reference-number')
    await asserts.accessibility()
    await asserts.h1('Your reference number')
    await asserts.number_of_errors(0)

    # Click "Continue" to return to the Overseas Check page
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Overseas Check page
    # ------------------------------------------------
    await asserts.url('/overseas-check')
    await asserts.accessibility()
    await asserts.h1('Have you ever been issued a Gender Recognition Certificate (or its equivalent) in another country?')
    await asserts.number_of_errors(0)

    # Don't choose any radio option
    await helpers.click_button('Continue')
    await asserts.url('/overseas-check')
    await asserts.accessibility()
    await asserts.h1('Have you ever been issued a Gender Recognition Certificate (or its equivalent) in another country?')
    await asserts.number_of_errors(1)
    await asserts.error(field='overseasCheck', message='Select if you ever been issued a Gender Recognition Certificate')

    # Choose the "No" option - this should take you straight to the Declaration page
    # i.e. you should skip the Overseas Approved Check page
    await helpers.check_radio(field='overseasCheck', value='No')
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Declaration page
    # ------------------------------------------------
    await asserts.url('/declaration')
    await asserts.accessibility()
    await asserts.h1('Notifying the General Register Office')
    await asserts.number_of_errors(0)

    # Click "Back" to return to the Overseas Check page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Overseas Check page
    # ------------------------------------------------
    await asserts.url('/overseas-check')
    await asserts.accessibility()
    await asserts.h1('Have you ever been issued a Gender Recognition Certificate (or its equivalent) in another country?')
    await asserts.number_of_errors(0)

    # Selection of "No" should be remembered
    await asserts.is_checked(field='overseasCheck', value='No')
    await asserts.not_checked(field='overseasCheck', value='Yes')

    # Choose the "Yes" radio option
    # This should take us to the Overseas Approved Check page
    await helpers.check_radio(field='overseasCheck', value='Yes')
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Overseas Approved Check page
    # ------------------------------------------------
    await asserts.url('/overseas-approved-check')
    await asserts.accessibility()
    await asserts.h1('Gender recognition in approved countries and territories')
    await asserts.number_of_errors(0)

    # Click "Back" to return to the Overseas Check page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Overseas Check page
    # ------------------------------------------------
    await asserts.url('/overseas-check')
    await asserts.accessibility()
    await asserts.h1('Have you ever been issued a Gender Recognition Certificate (or its equivalent) in another country?')
    await asserts.number_of_errors(0)

    # Selection of "Yes" should be remembered
    await asserts.is_checked(field='overseasCheck', value='Yes')
    await asserts.not_checked(field='overseasCheck', value='No')

    # Go forward to the Overseas Approved Check page
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Overseas Approved Check page
    # ------------------------------------------------
    await asserts.url('/overseas-approved-check')
    await asserts.accessibility()
    await asserts.h1('Gender recognition in approved countries and territories')
    await asserts.number_of_errors(0)

    # Don't choose any radio option
    await helpers.click_button('Continue')
    await asserts.url('/overseas-approved-check')
    await asserts.accessibility()
    await asserts.h1('Gender recognition in approved countries and territories')
    await asserts.number_of_errors(1)
    await asserts.error(field='overseasApprovedCheck', message='Select if you have official documentation')

    # Choose the "Yes" radio option
    await helpers.check_radio(field='overseasApprovedCheck', value='Yes')
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Declaration page
    # ------------------------------------------------
    await asserts.url('/declaration')
    await asserts.accessibility()
    await asserts.h1('Notifying the General Register Office')
    await asserts.number_of_errors(0)

    # Click "Back" to return to the Overseas Approved Check page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Overseas Approved Check page
    # ------------------------------------------------
    await asserts.url('/overseas-approved-check')
    await asserts.accessibility()
    await asserts.h1('Gender recognition in approved countries and territories')
    await asserts.number_of_errors(0)

    # Selection of "Yes" should be remembered
    await asserts.is_checked(field='overseasApprovedCheck', value='Yes')
    await asserts.not_checked(field='overseasApprovedCheck', value='No')

    # Go forward to the Declaration page
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Declaration page
    # ------------------------------------------------
    await asserts.url('/declaration')
    await asserts.accessibility()
    await asserts.h1('Notifying the General Register Office')
    await asserts.number_of_errors(0)

    # Don't check the checkbox
    await helpers.click_button('Continue')
    await asserts.url('/declaration')
    await asserts.accessibility()
    await asserts.h1('Notifying the General Register Office')
    await asserts.number_of_errors(1)
    await asserts.error(field='consent', message='You must consent to the General Register Office contacting you')

    # Check the checkbox
    await helpers.check_checkbox(field='consent')
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Click "Exit and return later"
    await helpers.click_button('Exit and return later')

    # ------------------------------------------------
    # ---- Application Saved page
    # ------------------------------------------------
    await asserts.url('/save-and-return/exit-application')
    await asserts.accessibility()
    await asserts.h1('Application saved')
    await asserts.number_of_errors(0)

    # Check reference number matches that given on earlier page
    reference_number_on_application_saved_page = await page.inner_text('#reference-number')
    assert reference_number_on_application_saved_page == reference_number_on_reference_number_page

    # Click "return to your application"
    await helpers.click_button('return to your application')

    # ------------------------------------------------
    # ---- Homepage / Email address page
    # ------------------------------------------------
    await asserts.url('/')
    await asserts.accessibility()
    await asserts.h1('Email address')
    await asserts.number_of_errors(0)

    # Enter a DIFFERENT email address than the one we used earlier
    await helpers.fill_textbox(field='email', value=DIFFERENT_EMAIL_ADDRESS)
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Security Code page
    # ------------------------------------------------
    await asserts.url('/email-confirmation')
    await asserts.accessibility()
    await asserts.h1('Enter security code')
    await asserts.number_of_errors(0)

    # Enter a valid Security Code, click Continue button
    await helpers.fill_textbox(field='code', value='11111')
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Is First Visit page
    # ------------------------------------------------
    await asserts.url('/is-first-visit')
    await asserts.accessibility()
    await asserts.h1('Have you already started an application?')
    await asserts.number_of_errors(0)

    # Choose the "Yes, and I have my reference number" option
    # Enter the reference number we were given earlier
    # This should FAIL because we're logging in as a different user
    await helpers.check_radio(field='isFirstVisit', value='HAS_REFERENCE')
    await helpers.fill_textbox(field='reference', value=reference_number_on_reference_number_page)
    await helpers.click_button('Continue')
    await asserts.url('/is-first-visit')
    await asserts.accessibility()
    await asserts.h1('Have you already started an application?')
    await asserts.number_of_errors(1)
    await asserts.error(field='reference', message='Enter a valid reference number')

    # Click "Back" to return to the Homepage
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Homepage / Email address page
    # ------------------------------------------------
    await asserts.url('/')
    await asserts.accessibility()
    await asserts.h1('Email address')
    await asserts.number_of_errors(0)

    # Enter THE SAME email address than the one we used earlier
    await helpers.fill_textbox(field='email', value=EMAIL_ADDRESS)
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Security Code page
    # ------------------------------------------------
    await asserts.url('/email-confirmation')
    await asserts.accessibility()
    await asserts.h1('Enter security code')
    await asserts.number_of_errors(0)

    # Enter a valid Security Code, click Continue button
    await helpers.fill_textbox(field='code', value='11111')
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Is First Visit page
    # ------------------------------------------------
    await asserts.url('/is-first-visit')
    await asserts.accessibility()
    await asserts.h1('Have you already started an application?')
    await asserts.number_of_errors(0)

    # Choose the "Yes, and I have my reference number" option
    # Enter the reference number we were given earlier
    # This should SUCCEED, because we are now logging in as the same user who created this application
    await helpers.check_radio(field='isFirstVisit', value='HAS_REFERENCE')
    await helpers.fill_textbox(field='reference', value=reference_number_on_reference_number_page)
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Status of "Confirmation" section should be "COMPLETED"
    await asserts.task_list_sections(7)
    await asserts.task_list_section(section='Confirmation', expected_status='COMPLETED')
    await asserts.task_list_section(section='Your personal details', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Your birth registration information', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Marriage or civil partnership details', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Overseas certificate documents', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Statutory declarations', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Submit and pay', expected_status='CANNOT START YET')

    # Click "Your personal details"
    await helpers.click_button('Your personal details')

    # ------------------------------------------------
    # ---- Your Name page
    # ------------------------------------------------
    await asserts.url('/personal-details')
    await asserts.accessibility()
    await asserts.h1('What is your name?')
    await asserts.number_of_errors(0)

    # "Back" link should take you to the Task List page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # "Your personal details" section should still be "NOT STARTED"
    await asserts.task_list_section(section='Your personal details', expected_status='NOT STARTED')

    # Click "Your personal details" again
    await helpers.click_button('Your personal details')

    # ------------------------------------------------
    # ---- Your Name page
    # ------------------------------------------------
    await asserts.url('/personal-details')
    await asserts.accessibility()
    await asserts.h1('What is your name?')
    await asserts.number_of_errors(0)

    # Don't enter any details, click Save and continue
    await helpers.fill_textbox(field='title', value='')
    await helpers.fill_textbox(field='first_name', value='')
    await helpers.fill_textbox(field='last_name', value='')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details')
    await asserts.accessibility()
    await asserts.h1('What is your name?')
    await asserts.number_of_errors(3)
    await asserts.error(field='title', message='Enter your title')
    await asserts.error(field='first_name', message='Enter your first name(s)')
    await asserts.error(field='last_name', message='Enter your last name')

    # Enter valid details, click Save and continue
    await helpers.fill_textbox(field='title', value=TITLE)
    await helpers.fill_textbox(field='first_name', value=FIRST_NAME)
    await helpers.fill_textbox(field='last_name', value=LAST_NAME)
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Affirmed Gender page
    # ------------------------------------------------
    await asserts.url('/personal-details/affirmed-gender')
    await asserts.accessibility()
    await asserts.h1('What is your affirmed gender?')
    await asserts.number_of_errors(0)

    # "Back" link should take you to the "Your Name" page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Your Name page
    # ------------------------------------------------
    await asserts.url('/personal-details')
    await asserts.accessibility()
    await asserts.h1('What is your name?')
    await asserts.number_of_errors(0)

    # The fields should be pre-populated with the values we just entered
    await asserts.field_value(field='title', expected_value=TITLE)
    await asserts.field_value(field='first_name', expected_value=FIRST_NAME)
    await asserts.field_value(field='last_name', expected_value=LAST_NAME)

    # Click "Return to task list" to return to Task List page
    await helpers.click_button('Return to task list')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Status of "Your personal details" section should be "IN PROGRESS"
    await asserts.task_list_sections(7)
    await asserts.task_list_section(section='Confirmation', expected_status='COMPLETED')
    await asserts.task_list_section(section='Your personal details', expected_status='IN PROGRESS')
    await asserts.task_list_section(section='Your birth registration information', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Marriage or civil partnership details', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Overseas certificate documents', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Statutory declarations', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Submit and pay', expected_status='CANNOT START YET')

    # Click "Your personal details"
    # This should now take you to the Affirmed Gender page
    await helpers.click_button('Your personal details')

    # ------------------------------------------------
    # ---- Affirmed Gender page
    # ------------------------------------------------
    await asserts.url('/personal-details/affirmed-gender')
    await asserts.accessibility()
    await asserts.h1('What is your affirmed gender?')
    await asserts.number_of_errors(0)

    # Don't choose any option, click Save and continue
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/affirmed-gender')
    await asserts.accessibility()
    await asserts.h1('What is your affirmed gender?')
    await asserts.number_of_errors(1)
    await asserts.error(field='affirmedGender', message='Select your affirmed gender')

    # Choose an option, click Save and continue
    await helpers.check_radio(field='affirmedGender', value='MALE')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Transition Date page
    # ------------------------------------------------
    await asserts.url('/personal-details/transition-date')
    await asserts.accessibility()
    await asserts.h1('When did you transition?')
    await asserts.number_of_errors(0)

    # "Back" link should take you to the Affirmed Gender page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Affirmed Gender page
    # ------------------------------------------------
    await asserts.url('/personal-details/affirmed-gender')
    await asserts.accessibility()
    await asserts.h1('What is your affirmed gender?')
    await asserts.number_of_errors(0)

    # The fields should be pre-populated with the values we just entered
    await asserts.is_checked(field='affirmedGender', value='MALE')
    await asserts.not_checked(field='affirmedGender', value='FEMALE')

    # Click Save and continue to return to Transition date page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Transition Date page
    # ------------------------------------------------
    await asserts.url('/personal-details/transition-date')
    await asserts.accessibility()
    await asserts.h1('When did you transition?')
    await asserts.number_of_errors(0)

    # Don't enter any values, click Save and continue
    await helpers.fill_textbox(field='transition_date_month', value='')
    await helpers.fill_textbox(field='transition_date_year', value='')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/transition-date')
    await asserts.accessibility()
    await asserts.h1('When did you transition?')
    await asserts.number_of_errors(2)
    await asserts.error(field='transition_date_month', message='Enter a month')
    await asserts.error(field='transition_date_year', message='Enter a year')

    # Enter values that aren't numbers, click Save and continue
    await helpers.fill_textbox(field='transition_date_month', value='AA')
    await helpers.fill_textbox(field='transition_date_year', value='BBBB')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/transition-date')
    await asserts.accessibility()
    await asserts.h1('When did you transition?')
    await asserts.number_of_errors(2)
    await asserts.error(field='transition_date_month', message='Enter a month as a number between 1 and 12')
    await asserts.error(field='transition_date_year', message='Enter a year as a 4-digit number, like 2000')

    # Enter values that are fractional numbers
    await helpers.fill_textbox(field='transition_date_month', value='1.2')
    await helpers.fill_textbox(field='transition_date_year', value='2000.4')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/transition-date')
    await asserts.accessibility()
    await asserts.h1('When did you transition?')
    await asserts.number_of_errors(2)
    await asserts.error(field='transition_date_month', message='Enter a month as a number between 1 and 12')
    await asserts.error(field='transition_date_year', message='Enter a year as a 4-digit number, like 2000')

    # Enter values that are too low
    await helpers.fill_textbox(field='transition_date_month', value='0')
    await helpers.fill_textbox(field='transition_date_year', value='999')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/transition-date')
    await asserts.accessibility()
    await asserts.h1('When did you transition?')
    await asserts.number_of_errors(2)
    await asserts.error(field='transition_date_month', message='Enter a month as a number between 1 and 12')
    await asserts.error(field='transition_date_year', message='Enter a year as a 4-digit number, like 2000')

    # Enter a month that is too high
    await helpers.fill_textbox(field='transition_date_month', value='13')
    await helpers.fill_textbox(field='transition_date_year', value='2000')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/transition-date')
    await asserts.accessibility()
    await asserts.h1('When did you transition?')
    await asserts.number_of_errors(1)
    await asserts.error(field='transition_date_month', message='Enter a month as a number between 1 and 12')

    # Enter a valid date that is more than 100 years' ago
    await helpers.fill_textbox(field='transition_date_month', value='1')
    await helpers.fill_textbox(field='transition_date_year', value='1900')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/transition-date')
    await asserts.accessibility()
    await asserts.h1('When did you transition?')
    await asserts.number_of_errors(1)
    await asserts.error(field='transition_date_year', message='Enter a date within the last 100 years')

    # Enter a valid date
    await helpers.fill_textbox(field='transition_date_month', value=TRANSITION_DATE_MONTH)
    await helpers.fill_textbox(field='transition_date_year', value=TRANSITION_DATE_YEAR)
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Previous Name Check page
    # ------------------------------------------------
    await asserts.url('/personal-details/previous-names-check')
    await asserts.accessibility()
    await asserts.h1('If you have ever changed your name to reflect your gender')
    await asserts.number_of_errors(0)

    # "Back" link should take you to the Transition Date page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Transition Date page
    # ------------------------------------------------
    await asserts.url('/personal-details/transition-date')
    await asserts.accessibility()
    await asserts.h1('When did you transition?')
    await asserts.number_of_errors(0)

    # The fields should be pre-populated with the values we just entered
    await asserts.field_value(field='transition_date_month', expected_value=TRANSITION_DATE_MONTH)
    await asserts.field_value(field='transition_date_year', expected_value=TRANSITION_DATE_YEAR)

    # Click Save and continue to return to Previous Name Check page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Previous Name Check page
    # ------------------------------------------------
    await asserts.url('/personal-details/previous-names-check')
    await asserts.accessibility()
    await asserts.h1('If you have ever changed your name to reflect your gender')
    await asserts.number_of_errors(0)

    # Don't choose an option, click Save and continue
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/previous-names-check')
    await asserts.accessibility()
    await asserts.h1('If you have ever changed your name to reflect your gender')
    await asserts.number_of_errors(1)
    await asserts.error(field='previousNameCheck', message='Select if you have ever changed your name to reflect your gender')

    # Choose an option, click Save and continue
    await helpers.check_radio(field='previousNameCheck', value='Yes')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Address page
    # ------------------------------------------------
    await asserts.url('/personal-details/address')
    await asserts.accessibility()
    await asserts.h1('What is your address?')
    await asserts.number_of_errors(0)

    # "Back" link should take you to the Previous Name Check page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Previous Name Check page
    # ------------------------------------------------
    await asserts.url('/personal-details/previous-names-check')
    await asserts.accessibility()
    await asserts.h1('If you have ever changed your name to reflect your gender')
    await asserts.number_of_errors(0)

    # The fields should be pre-populated with the values we just entered
    await asserts.is_checked(field='previousNameCheck', value='Yes')
    await asserts.not_checked(field='previousNameCheck', value='No')

    # Click Save and continue to return to Address page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Address page
    # ------------------------------------------------
    await asserts.url('/personal-details/address')
    await asserts.accessibility()
    await asserts.h1('What is your address?')
    await asserts.number_of_errors(0)

    # Don't enter any values, click Save and continue
    await helpers.fill_textbox(field='address_line_one', value='')
    await helpers.fill_textbox(field='address_line_two', value='')
    await helpers.fill_textbox(field='town', value='')
    await helpers.fill_textbox(field='postcode', value='')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/address')
    await asserts.accessibility()
    await asserts.h1('What is your address?')
    await asserts.number_of_errors(4)
    await asserts.error(field='address_line_one', message='Enter your building')
    await asserts.error(field='address_line_two', message='Enter your street')
    await asserts.error(field='town', message='Enter your town or city')
    await asserts.error(field='postcode', message='Enter your postcode')

    # Enter valid values, click Save and continue
    await helpers.fill_textbox(field='address_line_one', value=ADDRESS_LINE_ONE)
    await helpers.fill_textbox(field='address_line_two', value=ADDRESS_LINE_TWO)
    await helpers.fill_textbox(field='town', value=TOWN)
    await helpers.fill_textbox(field='postcode', value=POSTCODE)
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Contact Dates page
    # ------------------------------------------------
    await asserts.url('/personal-details/contact-dates')
    await asserts.accessibility()
    await asserts.h1('If we need to contact you by post in the next 6 months, are there any dates we should avoid?')
    await asserts.number_of_errors(0)

    # "Back" link should take you to the Address page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Address page
    # ------------------------------------------------
    await asserts.url('/personal-details/address')
    await asserts.accessibility()
    await asserts.h1('What is your address?')
    await asserts.number_of_errors(0)

    # The fields should be pre-populated with the values we just entered
    await asserts.field_value(field='address_line_one', expected_value=ADDRESS_LINE_ONE)
    await asserts.field_value(field='address_line_two', expected_value=ADDRESS_LINE_TWO)
    await asserts.field_value(field='town', expected_value=TOWN)
    await asserts.field_value(field='postcode', expected_value=POSTCODE)

    # Click Save and continue to return to Contact Dates page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Contact Dates page
    # ------------------------------------------------
    await asserts.url('/personal-details/contact-dates')
    await asserts.accessibility()
    await asserts.h1('If we need to contact you by post in the next 6 months, are there any dates we should avoid?')
    await asserts.number_of_errors(0)

    # Don't choose an option, click Save and continue
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/contact-dates')
    await asserts.accessibility()
    await asserts.h1('If we need to contact you by post in the next 6 months, are there any dates we should avoid?')
    await asserts.number_of_errors(1)
    await asserts.error(field='contactDatesCheck', message="Select if you don't want us to contact you at any point in the next 6 months")

    # Choose "Yes", but don't enter any dates
    await helpers.check_radio(field='contactDatesCheck', value='Yes')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/contact-dates')
    await asserts.accessibility()
    await asserts.h1('If we need to contact you by post in the next 6 months, are there any dates we should avoid?')
    await asserts.number_of_errors(1)
    await asserts.error(field='dates', message="Enter the dates you don't want us to contact you by post")

    # Enter some valid dates
    await helpers.check_radio(field='contactDatesCheck', value='Yes')
    await helpers.fill_textbox(field='dates', value=DATES_TO_AVOID)
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Contact Preferences page
    # ------------------------------------------------
    await asserts.url('/personal-details/contact-preferences')
    await asserts.accessibility()
    await asserts.h1('How would you like to be contacted if we have any questions about your application?')
    await asserts.number_of_errors(0)

    # "Back" link should take you to the Contact Dates page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Contact Dates page
    # ------------------------------------------------
    await asserts.url('/personal-details/contact-dates')
    await asserts.accessibility()
    await asserts.h1('If we need to contact you by post in the next 6 months, are there any dates we should avoid?')
    await asserts.number_of_errors(0)

    # The fields should be pre-populated with the values we just entered
    await asserts.is_checked(field='contactDatesCheck', value='Yes')
    await asserts.not_checked(field='contactDatesCheck', value='No')
    await asserts.field_value(field='dates', expected_value=DATES_TO_AVOID)

    # Click Save and continue to return to Contact Preferences page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Contact Preferences page
    # ------------------------------------------------
    await asserts.url('/personal-details/contact-preferences')
    await asserts.accessibility()
    await asserts.h1('How would you like to be contacted if we have any questions about your application?')
    await asserts.number_of_errors(0)

    # Don't choose an option, click Save and continue
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/contact-preferences')
    await asserts.accessibility()
    await asserts.h1('How would you like to be contacted if we have any questions about your application?')
    await asserts.number_of_errors(1)
    await asserts.error(field='contact_options', message="Select how would you like to be contacted")

    # Choose "Email" and "Phone" options, but don't enter an email address or phone number
    await helpers.check_checkbox(field='contact_options', value='EMAIL')
    await helpers.check_checkbox(field='contact_options', value='PHONE')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/contact-preferences')
    await asserts.accessibility()
    await asserts.h1('How would you like to be contacted if we have any questions about your application?')
    await asserts.number_of_errors(2)
    await asserts.error(field='email', message="Enter your email address")
    await asserts.error(field='phone', message="Enter your phone number")

    # Enter an invalid email address
    await helpers.check_checkbox(field='contact_options', value='EMAIL')
    await helpers.fill_textbox(field='email', value='inv@lid.email.@ddress')
    await helpers.uncheck_checkbox(field='contact_options', value='PHONE')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/contact-preferences')
    await asserts.accessibility()
    await asserts.h1('How would you like to be contacted if we have any questions about your application?')
    await asserts.number_of_errors(1)
    await asserts.error(field='email', message="Enter a valid email address")

    # Choose all the options and enter a valid email address and phone number
    await helpers.check_checkbox(field='contact_options', value='EMAIL')
    await helpers.fill_textbox(field='email', value=EMAIL_ADDRESS)
    await helpers.check_checkbox(field='contact_options', value='PHONE')
    await helpers.fill_textbox(field='phone', value=PHONE_NUMBER)
    await helpers.check_checkbox(field='contact_options', value='POST')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Notify HMRC page
    # ------------------------------------------------
    await asserts.url('/personal-details/hmrc')
    await asserts.accessibility()
    await asserts.h1('Notifying HMRC')
    await asserts.number_of_errors(0)

    # "Back" link should take you to the Contact Preferences page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Contact Preferences page
    # ------------------------------------------------
    await asserts.url('/personal-details/contact-preferences')
    await asserts.accessibility()
    await asserts.h1('How would you like to be contacted if we have any questions about your application?')
    await asserts.number_of_errors(0)

    # The fields should be pre-populated with the values we just entered
    await asserts.is_checked(field='contact_options', value='EMAIL')
    await asserts.is_checked(field='contact_options', value='PHONE')
    await asserts.is_checked(field='contact_options', value='POST')
    await asserts.field_value(field='email', expected_value=EMAIL_ADDRESS)
    await asserts.field_value(field='phone', expected_value=PHONE_NUMBER)

    # Click Save and continue to return to Notify HMRC page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Notify HMRC page
    # ------------------------------------------------
    await asserts.url('/personal-details/hmrc')
    await asserts.accessibility()
    await asserts.h1('Notifying HMRC')
    await asserts.number_of_errors(0)

    # Don't choose an option, click Save and continue
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/hmrc')
    await asserts.accessibility()
    await asserts.h1('Notifying HMRC')
    await asserts.number_of_errors(1)
    await asserts.error(field='tell_hmrc', message='Select if you would like us to tell HMRC after you receive a Gender Recognition Certificate')

    # Choose "Yes" option, but don't enter a National Insurance number
    await helpers.check_radio(field='tell_hmrc', value='Yes')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/hmrc')
    await asserts.accessibility()
    await asserts.h1('Notifying HMRC')
    await asserts.number_of_errors(1)
    await asserts.error(field='national_insurance_number', message='Enter your National Insurance number')

    # Enter an invalid National Insurance number
    await helpers.check_radio(field='tell_hmrc', value='Yes')
    await helpers.fill_textbox(field='national_insurance_number', value='INVALID-NI')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/hmrc')
    await asserts.accessibility()
    await asserts.h1('Notifying HMRC')
    await asserts.number_of_errors(1)
    await asserts.error(field='national_insurance_number', message='Enter a valid National Insurance number')

    # Enter a valid National Insurance number
    await helpers.check_radio(field='tell_hmrc', value='Yes')
    await helpers.fill_textbox(field='national_insurance_number', value=NATIONAL_INSURANCE_NUMBER)
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/personal-details/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers: Your personal details')
    await asserts.number_of_errors(0)

    # "Back" link should take you to the Notify HMRC page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Notify HMRC page
    # ------------------------------------------------
    await asserts.url('/personal-details/hmrc')
    await asserts.accessibility()
    await asserts.h1('Notifying HMRC')
    await asserts.number_of_errors(0)

    # The fields should be pre-populated with the values we just entered
    await asserts.is_checked(field='tell_hmrc', value='Yes')
    await asserts.not_checked(field='tell_hmrc', value='No')
    await asserts.field_value(field='national_insurance_number', expected_value=NATIONAL_INSURANCE_NUMBER)

    # Click Save and continue to return to Check Your Answers page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/personal-details/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers: Your personal details')
    await asserts.number_of_errors(0)

    # Check the values in the summary table
    await asserts.check_your_answers_rows(9)
    await asserts.check_your_answers_row(row_name='Name', expected_value=f"{TITLE} {FIRST_NAME} {LAST_NAME}")
    await asserts.check_your_answers_row(row_name='Affirmed gender', expected_value='Male')
    await asserts.check_your_answers_row(row_name='When you transitioned', expected_value='March 2000')
    await asserts.check_your_answers_row(row_name='Ever changed name', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Address', expected_value=f"{ADDRESS_LINE_ONE}\n{ADDRESS_LINE_TWO}\n{TOWN}\n{POSTCODE}")
    await asserts.check_your_answers_row(row_name='Contact preferences', expected_value=f"Email: {EMAIL_ADDRESS}\nPhone: {PHONE_NUMBER}\nPost: {ADDRESS_LINE_ONE}, {ADDRESS_LINE_TWO}, {TOWN}, {POSTCODE}")
    await asserts.check_your_answers_row(row_name='Unavailable over the next 6 months', expected_value=f"Yes\n{DATES_TO_AVOID}")
    await asserts.check_your_answers_row(row_name='Notify HMRC', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='National insurance number', expected_value=NATIONAL_INSURANCE_NUMBER)

    # Click each "Change" link to check it takes us to the correct page
    await asserts.change_links_to_url(link_text='Change name', expected_url='/personal-details')
    await asserts.change_links_to_url(link_text='Change affirmed gender', expected_url='/personal-details/affirmed-gender')
    await asserts.change_links_to_url(link_text='Change when you transitioned', expected_url='/personal-details/transition-date')
    await asserts.change_links_to_url(link_text='Change whether you have changed your name to reflect your gender', expected_url='/personal-details/previous-names-check')
    await asserts.change_links_to_url(link_text='Change address', expected_url='/personal-details/address')
    await asserts.change_links_to_url(link_text='Change contact preferences', expected_url='/personal-details/contact-preferences')
    await asserts.change_links_to_url(link_text="Change whether there are any dates you don't want us to contact you by post over the next 6 months", expected_url='/personal-details/contact-dates')
    await asserts.change_links_to_url(link_text='Change whether you want us to notify HMRC after you receive a Gender Recognition Certificate', expected_url='/personal-details/hmrc')
    await asserts.change_links_to_url(link_text='Change your National Insurance number', expected_url='/personal-details/hmrc')

    # Click "Change" on "Notify HMRC" and choose the "No" option
    # This should remove the "National Insurance number" row on the Check Your Answers page
    await helpers.click_button('Change whether you want us to notify HMRC after you receive a Gender Recognition Certificate')

    # ------------------------------------------------
    # ---- Notify HMRC page
    # ------------------------------------------------
    await asserts.url('/personal-details/hmrc')
    await asserts.accessibility()
    await asserts.h1('Notifying HMRC')
    await asserts.number_of_errors(0)

    await helpers.check_radio(field='tell_hmrc', value='No')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/personal-details/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers: Your personal details')
    await asserts.number_of_errors(0)

    await asserts.check_your_answers_rows(8)
    await asserts.check_your_answers_row(row_name='Notify HMRC', expected_value='No')
    await asserts.check_your_answers_row_missing(row_name='National insurance number')

    # Click Save and continue to return to Task List page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Status of "Your personal details" section should be "COMPLETED"
    await asserts.task_list_sections(8)
    await asserts.task_list_section(section='Confirmation', expected_status='COMPLETED')
    await asserts.task_list_section(section='Your personal details', expected_status='COMPLETED')
    await asserts.task_list_section(section='Your birth registration information', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Marriage or civil partnership details', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Name change documents', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Overseas certificate documents', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Statutory declarations', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Submit and pay', expected_status='CANNOT START YET')

    # TODO:
    #  * Currently, the "Your personal details" section is "COMPLETE"
    #  * Click "Your personal details"
    #  * Click "Return to Task List"
    #  * The "Your personal details" section *should* still be "COMPLETE"
    #  * Note: at the moment, it changes to be "IN PROGRESS"

    # Click "Your birth registration information" to go to the Birth Certificate Name page
    await helpers.click_button('Your birth registration information')

    # ------------------------------------------------
    # ---- Birth Certificate Name page
    # ------------------------------------------------
    await asserts.url('/birth-registration')
    await asserts.accessibility()
    await asserts.h1('What name was originally registered on your birth or adoption certificate?')
    await asserts.number_of_errors(0)

    # "Back" should take us to the Task List page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Click "Your birth registration information" to go to the Birth Certificate Name page again
    await helpers.click_button('Your birth registration information')

    # ------------------------------------------------
    # ---- Birth Certificate Name page
    # ------------------------------------------------
    await asserts.url('/birth-registration')
    await asserts.accessibility()
    await asserts.h1('What name was originally registered on your birth or adoption certificate?')
    await asserts.number_of_errors(0)

    # Don't enter any values, click "Save and continue"
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration')
    await asserts.accessibility()
    await asserts.h1('What name was originally registered on your birth or adoption certificate?')
    await asserts.number_of_errors(2)
    await asserts.error(field='first_name', message='Enter your first name, as originally registered on your birth or adoption certificate')
    await asserts.error(field='last_name', message='Enter your last name, as originally registered on your birth or adoption certificate')

    # Enter a valid name, click "Save and continue"
    await helpers.fill_textbox(field='first_name', value=BIRTH_FIRST_NAME)
    await helpers.fill_textbox(field='middle_names', value=BIRTH_MIDDLE_NAME)
    await helpers.fill_textbox(field='last_name', value=BIRTH_LAST_NAME)
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Date of Birth page
    # ------------------------------------------------
    await asserts.url('/birth-registration/dob')
    await asserts.accessibility()
    await asserts.h1('What is the date of birth on your birth or adoption certificate?')
    await asserts.number_of_errors(0)

    # Click "Back" to go back to Birth Certificate Name page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Birth Certificate Name page
    # ------------------------------------------------
    await asserts.url('/birth-registration')
    await asserts.accessibility()
    await asserts.h1('What name was originally registered on your birth or adoption certificate?')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.field_value(field='first_name', expected_value=BIRTH_FIRST_NAME)
    await asserts.field_value(field='middle_names', expected_value=BIRTH_MIDDLE_NAME)
    await asserts.field_value(field='last_name', expected_value=BIRTH_LAST_NAME)

    # Continue to Date of Birth page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Date of Birth page
    # ------------------------------------------------
    await asserts.url('/birth-registration/dob')
    await asserts.accessibility()
    await asserts.h1('What is the date of birth on your birth or adoption certificate?')
    await asserts.number_of_errors(0)

    # Don't enter any values, click "Save and continue"
    await helpers.fill_textbox(field='day', value='')
    await helpers.fill_textbox(field='month', value='')
    await helpers.fill_textbox(field='year', value='')
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration/dob')
    await asserts.accessibility()
    await asserts.h1('What is the date of birth on your birth or adoption certificate?')
    await asserts.number_of_errors(3)
    await asserts.error(field='day', message='Enter a day')
    await asserts.error(field='month', message='Enter a month')
    await asserts.error(field='year', message='Enter a year')

    # Enter values that are not numbers, click "Save and continue"
    await helpers.fill_textbox(field='day', value='AA')
    await helpers.fill_textbox(field='month', value='BB')
    await helpers.fill_textbox(field='year', value='CCCC')
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration/dob')
    await asserts.accessibility()
    await asserts.h1('What is the date of birth on your birth or adoption certificate?')
    await asserts.number_of_errors(3)
    await asserts.error(field='day', message='Enter a day as a number between 1 and 31')
    await asserts.error(field='month', message='Enter a month as a number between 1 and 12')
    await asserts.error(field='year', message='Enter a year as a 4-digit number, like 2000')

    # Enter values that are too small, click "Save and continue"
    await helpers.fill_textbox(field='day', value='0')
    await helpers.fill_textbox(field='month', value='0')
    await helpers.fill_textbox(field='year', value='999')
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration/dob')
    await asserts.accessibility()
    await asserts.h1('What is the date of birth on your birth or adoption certificate?')
    await asserts.number_of_errors(3)
    await asserts.error(field='day', message='Enter a day as a number between 1 and 31')
    await asserts.error(field='month', message='Enter a month as a number between 1 and 12')
    await asserts.error(field='year', message='Enter a year as a 4-digit number, like 2000')

    # Enter values that are too large, click "Save and continue"
    await helpers.fill_textbox(field='day', value='32')
    await helpers.fill_textbox(field='month', value='13')
    await helpers.fill_textbox(field='year', value='1956')
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration/dob')
    await asserts.accessibility()
    await asserts.h1('What is the date of birth on your birth or adoption certificate?')
    await asserts.number_of_errors(2)
    await asserts.error(field='day', message='Enter a day as a number between 1 and 31')
    await asserts.error(field='month', message='Enter a month as a number between 1 and 12')

    # Enter a valid date in the future, click "Save and continue"
    await helpers.fill_textbox(field='day', value=DATE_OF_BIRTH_DAY)
    await helpers.fill_textbox(field='month', value=DATE_OF_BIRTH_MONTH)
    await helpers.fill_textbox(field='year', value='2222')
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration/dob')
    await asserts.accessibility()
    await asserts.h1('What is the date of birth on your birth or adoption certificate?')
    await asserts.number_of_errors(1)
    await asserts.error(field='year', message='You need to be at least 18 years old to apply')

    # Enter a valid date too far in the past, click "Save and continue"
    await helpers.fill_textbox(field='day', value=DATE_OF_BIRTH_DAY)
    await helpers.fill_textbox(field='month', value=DATE_OF_BIRTH_MONTH)
    await helpers.fill_textbox(field='year', value='1900')
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration/dob')
    await asserts.accessibility()
    await asserts.h1('What is the date of birth on your birth or adoption certificate?')
    await asserts.number_of_errors(1)
    await asserts.error(field='year', message='You need to be less than 110 years old to apply')

    # Enter valid values, click "Save and continue"
    await helpers.fill_textbox(field='day', value=DATE_OF_BIRTH_DAY)
    await helpers.fill_textbox(field='month', value=DATE_OF_BIRTH_MONTH)
    await helpers.fill_textbox(field='year', value=DATE_OF_BIRTH_YEAR)
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Birth Registered in UK page
    # ------------------------------------------------
    await asserts.url('/birth-registration/uk-check')
    await asserts.accessibility()
    await asserts.h1('Was your birth registered in the UK?')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Date of Birth page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Date of Birth page
    # ------------------------------------------------
    await asserts.url('/birth-registration/dob')
    await asserts.accessibility()
    await asserts.h1('What is the date of birth on your birth or adoption certificate?')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.field_value(field='day', expected_value=DATE_OF_BIRTH_DAY)
    await asserts.field_value(field='month', expected_value=DATE_OF_BIRTH_MONTH)
    await asserts.field_value(field='year', expected_value=DATE_OF_BIRTH_YEAR)

    # Continue to Birth Registered in UK page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Birth Registered in UK page
    # ------------------------------------------------
    await asserts.url('/birth-registration/uk-check')
    await asserts.accessibility()
    await asserts.h1('Was your birth registered in the UK?')
    await asserts.number_of_errors(0)

    # Don't choose an option, click "Save and continue"
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration/uk-check')
    await asserts.accessibility()
    await asserts.h1('Was your birth registered in the UK?')
    await asserts.number_of_errors(1)
    await asserts.error(field='birth_registered_in_uk', message='Select if your birth was registered in the UK')

    # Select "No" to go down the "abroad" route first
    # Later, we will re-trace our steps, and select "Yes" to go down the "UK" route
    await helpers.check_radio(field='birth_registered_in_uk', value='No')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- What Country page
    # ------------------------------------------------
    await asserts.url('/birth-registration/country')
    await asserts.accessibility()
    await asserts.h1('What country was your birth registered in?')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Birth Registered in UK page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Birth Registered in UK page
    # ------------------------------------------------
    await asserts.url('/birth-registration/uk-check')
    await asserts.accessibility()
    await asserts.h1('Was your birth registered in the UK?')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='birth_registered_in_uk', value='No')
    await asserts.not_checked(field='birth_registered_in_uk', value='Yes')

    # Continue to What Country page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- What Country page
    # ------------------------------------------------
    await asserts.url('/birth-registration/country')
    await asserts.accessibility()
    await asserts.h1('What country was your birth registered in?')
    await asserts.number_of_errors(0)

    # Don't enter a value, click "Save and continue"
    await helpers.fill_textbox(field='country_of_birth', value='')
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration/country')
    await asserts.accessibility()
    await asserts.h1('What country was your birth registered in?')
    await asserts.number_of_errors(1)
    await asserts.error(field='country_of_birth', message='Enter your country of birth')

    # Enter a valid value, click "Save and continue"
    await helpers.fill_textbox(field='country_of_birth', value=BIRTH_COUNTRY)
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Birth Registration: Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/birth-registration/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers: Birth registration details')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the What Country page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- What Country page
    # ------------------------------------------------
    await asserts.url('/birth-registration/country')
    await asserts.accessibility()
    await asserts.h1('What country was your birth registered in?')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.field_value(field='country_of_birth', expected_value=BIRTH_COUNTRY)

    # Continue to Birth Registration: Check Your Answers page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Birth Registration: Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/birth-registration/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers: Birth registration details')
    await asserts.number_of_errors(0)

    # Check the values in the table
    await asserts.check_your_answers_rows(4)
    await asserts.check_your_answers_row(row_name='Birth name', expected_value=f"{BIRTH_FIRST_NAME} {BIRTH_MIDDLE_NAME} {BIRTH_LAST_NAME}")
    await asserts.check_your_answers_row(row_name='Date of birth', expected_value=DATE_OF_BIRTH_FORMATTED)
    await asserts.check_your_answers_row(row_name='Birth registered in UK', expected_value='No')
    await asserts.check_your_answers_row(row_name='Registered birth country', expected_value=BIRTH_COUNTRY)

    # Click each "Change" link to check it takes us to the correct page
    await asserts.change_links_to_url(link_text='Change birth name', expected_url='/birth-registration')
    await asserts.change_links_to_url(link_text='Change date of birth', expected_url='/birth-registration/dob')
    await asserts.change_links_to_url(link_text='Change whether your birth was regstered in the UK', expected_url='/birth-registration/uk-check')
    await asserts.change_links_to_url(link_text='Change the country you were born in', expected_url='/birth-registration/country')

    # Click "Back" to return to the "Birth Registered in UK page"
    # Choose the "UK" option and proceed down that branch
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- What Country page
    # ------------------------------------------------
    await asserts.url('/birth-registration/country')
    await asserts.accessibility()
    await asserts.h1('What country was your birth registered in?')
    await asserts.number_of_errors(0)

    # Click "Back" to return to the "Birth Registered in UK page"
    # Choose the "UK" option and proceed down that branch
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Birth Registered in UK page
    # ------------------------------------------------
    await asserts.url('/birth-registration/uk-check')
    await asserts.accessibility()
    await asserts.h1('Was your birth registered in the UK?')
    await asserts.number_of_errors(0)

    # Choose the "UK" option and proceed down that branch
    await helpers.check_radio(field='birth_registered_in_uk', value='Yes')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Place of Birth page
    # ------------------------------------------------
    await asserts.url('/birth-registration/place-of-birth')
    await asserts.accessibility()
    await asserts.h1('What is the town or city of birth on your birth or adoption certificate?')
    await asserts.number_of_errors(0)

    # Don't enter a value, click "Save and continue"
    await helpers.fill_textbox(field='place_of_birth', value='')
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration/place-of-birth')
    await asserts.accessibility()
    await asserts.h1('What is the town or city of birth on your birth or adoption certificate?')
    await asserts.number_of_errors(1)
    await asserts.error(field='place_of_birth', message='Enter your town or city of birth')

    # Enter a valid value, click "Save and continue"
    await helpers.fill_textbox(field='place_of_birth', value=BIRTH_TOWN)
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Mother's Name page
    # ------------------------------------------------
    await asserts.url('/birth-registration/mothers-name')
    await asserts.accessibility()
    await asserts.h1('What is your mother’s name as listed on your birth or adoption certificate?')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Place of Birth page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Place of Birth page
    # ------------------------------------------------
    await asserts.url('/birth-registration/place-of-birth')
    await asserts.accessibility()
    await asserts.h1('What is the town or city of birth on your birth or adoption certificate?')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.field_value(field='place_of_birth', expected_value=BIRTH_TOWN)

    # Continue to Mother's Name page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Mother's Name page
    # ------------------------------------------------
    await asserts.url('/birth-registration/mothers-name')
    await asserts.accessibility()
    await asserts.h1('What is your mother’s name as listed on your birth or adoption certificate?')
    await asserts.number_of_errors(0)

    # Don't enter any values, click "Save and continue"
    await helpers.fill_textbox(field='first_name', value='')
    await helpers.fill_textbox(field='last_name', value='')
    await helpers.fill_textbox(field='maiden_name', value='')
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration/mothers-name')
    await asserts.accessibility()
    await asserts.h1('What is your mother’s name as listed on your birth or adoption certificate?')
    await asserts.number_of_errors(3)
    await asserts.error(field='first_name', message="Enter your mother's first name")
    await asserts.error(field='last_name', message="Enter your mother's last name")
    await asserts.error(field='maiden_name', message="Enter your mother's maiden name")

    # Enter valid values, click "Save and continue"
    await helpers.fill_textbox(field='first_name', value=MOTHERS_FIRST_NAME)
    await helpers.fill_textbox(field='last_name', value=MOTHERS_LAST_NAME)
    await helpers.fill_textbox(field='maiden_name', value=MOTHERS_MAIDEN_NAME)
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Is Father's Name On Certificate page
    # ------------------------------------------------
    await asserts.url('/birth-registration/fathers-name-check')
    await asserts.accessibility()
    await asserts.h1("Is your father's name listed on the certificate?")
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Mother's Name page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Mother's Name page
    # ------------------------------------------------
    await asserts.url('/birth-registration/mothers-name')
    await asserts.accessibility()
    await asserts.h1('What is your mother’s name as listed on your birth or adoption certificate?')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.field_value(field='first_name', expected_value=MOTHERS_FIRST_NAME)
    await asserts.field_value(field='last_name', expected_value=MOTHERS_LAST_NAME)
    await asserts.field_value(field='maiden_name', expected_value=MOTHERS_MAIDEN_NAME)

    # Continue to Mother's Name page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Is Father's Name On Certificate page
    # ------------------------------------------------
    await asserts.url('/birth-registration/fathers-name-check')
    await asserts.accessibility()
    await asserts.h1("Is your father's name listed on the certificate?")
    await asserts.number_of_errors(0)

    # Don't select an option, click "Save and continue"
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration/fathers-name-check')
    await asserts.accessibility()
    await asserts.h1("Is your father's name listed on the certificate?")
    await asserts.number_of_errors(1)
    await asserts.error(field='fathers_name_on_certificate', message="Select if your father's name is listed on the certificate")

    # Select the "No" option, click "Save and continue"
    # This should take us to the "Adopted" question
    await helpers.check_radio(field='fathers_name_on_certificate', value='No')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Were You Adopted page
    # ------------------------------------------------
    await asserts.url('/birth-registration/adopted')
    await asserts.accessibility()
    await asserts.h1('Were you adopted?')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Is Father's Name On Certificate page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Is Father's Name On Certificate page
    # ------------------------------------------------
    await asserts.url('/birth-registration/fathers-name-check')
    await asserts.accessibility()
    await asserts.h1("Is your father's name listed on the certificate?")
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='fathers_name_on_certificate', value='No')
    await asserts.not_checked(field='fathers_name_on_certificate', value='Yes')

    # Select the "Yes" option, click "Save and continue"
    # This should take us to the "Father's Name" question
    await helpers.check_radio(field='fathers_name_on_certificate', value='Yes')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Father's Name page
    # ------------------------------------------------
    await asserts.url('/birth-registration/fathers-name')
    await asserts.accessibility()
    await asserts.h1("What is your father's name as listed on your birth or adoption certificate?")
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Is Father's Name On Certificate page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Is Father's Name On Certificate page
    # ------------------------------------------------
    await asserts.url('/birth-registration/fathers-name-check')
    await asserts.accessibility()
    await asserts.h1("Is your father's name listed on the certificate?")
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='fathers_name_on_certificate', value='Yes')
    await asserts.not_checked(field='fathers_name_on_certificate', value='No')

    # Continue to Father's Name page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Father's Name page
    # ------------------------------------------------
    await asserts.url('/birth-registration/fathers-name')
    await asserts.accessibility()
    await asserts.h1("What is your father's name as listed on your birth or adoption certificate?")
    await asserts.number_of_errors(0)

    # Don't enter any values, click "Save and continue"
    await helpers.fill_textbox(field='first_name', value='')
    await helpers.fill_textbox(field='last_name', value='')
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration/fathers-name')
    await asserts.accessibility()
    await asserts.h1("What is your father's name as listed on your birth or adoption certificate?")
    await asserts.number_of_errors(2)
    await asserts.error(field='first_name', message="Enter your father's first name")
    await asserts.error(field='last_name', message="Enter your father's last name")

    # Enter valid values, click "Save and continue"
    await helpers.fill_textbox(field='first_name', value=FATHERS_FIRST_NAME)
    await helpers.fill_textbox(field='last_name', value=FATHERS_LAST_NAME)
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Were You Adopted page
    # ------------------------------------------------
    await asserts.url('/birth-registration/adopted')
    await asserts.accessibility()
    await asserts.h1('Were you adopted?')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Father's Name page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Father's Name page
    # ------------------------------------------------
    await asserts.url('/birth-registration/fathers-name')
    await asserts.accessibility()
    await asserts.h1("What is your father's name as listed on your birth or adoption certificate?")
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.field_value(field='first_name', expected_value=FATHERS_FIRST_NAME)
    await asserts.field_value(field='last_name', expected_value=FATHERS_LAST_NAME)

    # Continue to the Were You Adopted page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Were You Adopted page
    # ------------------------------------------------
    await asserts.url('/birth-registration/adopted')
    await asserts.accessibility()
    await asserts.h1('Were you adopted?')
    await asserts.number_of_errors(0)

    # Don't select an option, click "Save and continue"
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration/adopted')
    await asserts.accessibility()
    await asserts.h1('Were you adopted?')
    await asserts.number_of_errors(1)
    await asserts.error(field='adopted', message='Select if you were you adopted')

    # Select the "No" option, click "Save and continue"
    # This should take us to the "Forces" question
    # i.e. we will skip the "Adopted in the UK" page
    await helpers.check_radio(field='adopted', value='No')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Forces page
    # ------------------------------------------------
    await asserts.url('/birth-registration/forces')
    await asserts.accessibility()
    await asserts.h1('Was your birth registered by a Forces registering service, or with a British Consul or High Commission, or under Merchant Shipping or Civil Aviation provisions?')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Were You Adopted page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Were You Adopted page
    # ------------------------------------------------
    await asserts.url('/birth-registration/adopted')
    await asserts.accessibility()
    await asserts.h1('Were you adopted?')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='adopted', value='No')
    await asserts.not_checked(field='adopted', value='Yes')

    # Now choose "Yes" and click "Save and continue"
    # This should take us to the "Adopted in the UK" page (which we previously skipped)
    await helpers.check_radio(field='adopted', value='Yes')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Adopted In The UK page
    # ------------------------------------------------
    await asserts.url('/birth-registration/adopted-uk')
    await asserts.accessibility()
    await asserts.h1('Were you adopted in the United Kingdom?')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Were You Adopted page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Were You Adopted page
    # ------------------------------------------------
    await asserts.url('/birth-registration/adopted')
    await asserts.accessibility()
    await asserts.h1('Were you adopted?')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='adopted', value='Yes')
    await asserts.not_checked(field='adopted', value='No')

    # Continue to the "Adopted In The UK" page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Adopted In The UK page
    # ------------------------------------------------
    await asserts.url('/birth-registration/adopted-uk')
    await asserts.accessibility()
    await asserts.h1('Were you adopted in the United Kingdom?')
    await asserts.number_of_errors(0)

    # Don't select an option, click "Save and continue"
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration/adopted-uk')
    await asserts.accessibility()
    await asserts.h1('Were you adopted in the United Kingdom?')
    await asserts.number_of_errors(1)
    await asserts.error(field='adopted_uk', message='Select if you were adopted in the United Kingdom')

    # Select a valid option, click "Save and continue"
    await helpers.check_radio(field='adopted_uk', value='DO_NOT_KNOW')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Forces page
    # ------------------------------------------------
    await asserts.url('/birth-registration/forces')
    await asserts.accessibility()
    await asserts.h1('Was your birth registered by a Forces registering service, or with a British Consul or High Commission, or under Merchant Shipping or Civil Aviation provisions?')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Adopted In The UK page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Adopted In The UK page
    # ------------------------------------------------
    await asserts.url('/birth-registration/adopted-uk')
    await asserts.accessibility()
    await asserts.h1('Were you adopted in the United Kingdom?')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='adopted_uk', value='DO_NOT_KNOW')
    await asserts.not_checked(field='adopted_uk', value='Yes')
    await asserts.not_checked(field='adopted_uk', value='No')

    # Continue to the "Adopted In The UK" page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Forces page
    # ------------------------------------------------
    await asserts.url('/birth-registration/forces')
    await asserts.accessibility()
    await asserts.h1('Was your birth registered by a Forces registering service, or with a British Consul or High Commission, or under Merchant Shipping or Civil Aviation provisions?')
    await asserts.number_of_errors(0)

    # Don't select an option, click "Save and continue"
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration/forces')
    await asserts.accessibility()
    await asserts.h1('Was your birth registered by a Forces registering service, or with a British Consul or High Commission, or under Merchant Shipping or Civil Aviation provisions?')
    await asserts.number_of_errors(1)
    await asserts.error(field='forces', message='Select if your birth was registered by a Forces registering service, or with a British Consul or High Commission, or under Merchant Shipping or Civil Aviation provisions')

    # Select a valid option, click "Save and continue"
    await helpers.check_radio(field='forces', value='No')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Birth Registration: Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/birth-registration/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers: Birth registration details')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Forces page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Forces page
    # ------------------------------------------------
    await asserts.url('/birth-registration/forces')
    await asserts.accessibility()
    await asserts.h1('Was your birth registered by a Forces registering service, or with a British Consul or High Commission, or under Merchant Shipping or Civil Aviation provisions?')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='forces', value='No')
    await asserts.not_checked(field='forces', value='Yes')

    # Continue to Birth Registration: Check Your Answers page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Birth Registration: Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/birth-registration/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers: Birth registration details')
    await asserts.number_of_errors(0)

    # Check the values in the table
    await asserts.check_your_answers_rows(10)
    await asserts.check_your_answers_row(row_name='Birth name', expected_value=f"{BIRTH_FIRST_NAME} {BIRTH_MIDDLE_NAME} {BIRTH_LAST_NAME}")
    await asserts.check_your_answers_row(row_name='Date of birth', expected_value=DATE_OF_BIRTH_FORMATTED)
    await asserts.check_your_answers_row(row_name='Birth registered in UK', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Town or city of birth', expected_value=BIRTH_TOWN)
    await asserts.check_your_answers_row(row_name="Mother's name", expected_value=f"{MOTHERS_FIRST_NAME} {MOTHERS_LAST_NAME}\n(Maiden name: {MOTHERS_MAIDEN_NAME})")
    await asserts.check_your_answers_row(row_name="Father's name listed", expected_value='Yes')
    await asserts.check_your_answers_row(row_name="Father's name", expected_value=f"{FATHERS_FIRST_NAME} {FATHERS_LAST_NAME}")
    await asserts.check_your_answers_row(row_name='Adopted', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Adopted in UK', expected_value="I don't know")
    await asserts.check_your_answers_row(row_name='Forces registering service, British Consul or High Commission, or under Merchant Shipping or Civil Aviation provisions', expected_value='No')

    # Click each "Change" link to check it takes us to the correct page
    await asserts.change_links_to_url(link_text='Change birth name', expected_url='/birth-registration')
    await asserts.change_links_to_url(link_text='Change date of birth', expected_url='/birth-registration/dob')
    await asserts.change_links_to_url(link_text='Change whether your birth was regstered in the UK', expected_url='/birth-registration/uk-check')
    await asserts.change_links_to_url(link_text='Change your town or city of birth', expected_url='/birth-registration/place-of-birth')
    await asserts.change_links_to_url(link_text="Change your mother's name", expected_url='/birth-registration/mothers-name')
    await asserts.change_links_to_url(link_text="Change whether your father's name is listed on your birth or adoption certificate", expected_url='/birth-registration/fathers-name-check')
    await asserts.change_links_to_url(link_text="Change your father's name", expected_url='/birth-registration/fathers-name')
    await asserts.change_links_to_url(link_text='Change whether you were adopted', expected_url='/birth-registration/adopted')
    await asserts.change_links_to_url(link_text='Change whether you were adopted in the UK', expected_url='/birth-registration/adopted-uk')
    await asserts.change_links_to_url(link_text='Change whether your birth was registered under the Forces registering service, British Consul or High Commission, or under Merchant Shipping or Civil Aviation provisions', expected_url='/birth-registration/forces')

    # Click "Save and continue"
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Status of "Your birth registration information" section should be "COMPLETED"
    await asserts.task_list_sections(8)
    await asserts.task_list_section(section='Confirmation', expected_status='COMPLETED')
    await asserts.task_list_section(section='Your personal details', expected_status='COMPLETED')
    await asserts.task_list_section(section='Your birth registration information', expected_status='COMPLETED')
    await asserts.task_list_section(section='Marriage or civil partnership details', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Name change documents', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Overseas certificate documents', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Statutory declarations', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Submit and pay', expected_status='CANNOT START YET')

    # Click "Marriage or civil partnership details" to go to the "Are You Married" page
    await helpers.click_button('Marriage or civil partnership details')

    # ------------------------------------------------
    # ---- Are You Married page
    # ------------------------------------------------
    await asserts.url('/partnership-details')
    await asserts.accessibility()
    await asserts.h1('Marriages and civil partnerships')
    await asserts.number_of_errors(0)

    # "Back" should take us to the Task List page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Continue to the "Are You Married" page again
    await helpers.click_button('Marriage or civil partnership details')

    # ------------------------------------------------
    # ---- Are You Married page
    # ------------------------------------------------
    await asserts.url('/partnership-details')
    await asserts.accessibility()
    await asserts.h1('Marriages and civil partnerships')
    await asserts.number_of_errors(0)

    # Don't select an option, click "Save and continue"
    await helpers.click_button('Save and continue')
    await asserts.url('/partnership-details')
    await asserts.accessibility()
    await asserts.h1('Marriages and civil partnerships')
    await asserts.number_of_errors(1)
    await asserts.error(field='currently_married', message='Select if you are currently married or in a civil partnership')

    # Select "Neither" option and proceed down this route until the "Check you answers" page
    # Then, re-trace our steps back here and choose the "Married" and then "Civil partnership" options
    await helpers.check_radio(field='currently_married', value='Neither')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Partner Died page
    # ------------------------------------------------
    await asserts.url('/partnership-details/partner-died')
    await asserts.accessibility()
    await asserts.h1('Were you previously married or in a civil partnership, and your spouse or partner died?')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Are You Married page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Are You Married page
    # ------------------------------------------------
    await asserts.url('/partnership-details')
    await asserts.accessibility()
    await asserts.h1('Marriages and civil partnerships')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='currently_married', value='Neither')
    await asserts.not_checked(field='currently_married', value='Married')
    await asserts.not_checked(field='currently_married', value='Civil partnership')

    # Continue to Partner Died page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Partner Died page
    # ------------------------------------------------
    await asserts.url('/partnership-details/partner-died')
    await asserts.accessibility()
    await asserts.h1('Were you previously married or in a civil partnership, and your spouse or partner died?')
    await asserts.number_of_errors(0)

    # Don't select an option, click "Save and continue"
    await helpers.click_button('Save and continue')
    await asserts.url('/partnership-details/partner-died')
    await asserts.accessibility()
    await asserts.h1('Were you previously married or in a civil partnership, and your spouse or partner died?')
    await asserts.number_of_errors(1)
    await asserts.error(field='partner_died', message='Select if you were previously married or in a civil partnership, and your spouse or partner died')

    # Select a valid option, click "Save and continue"
    await helpers.check_radio(field='partner_died', value='Yes')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Partnership Ended page
    # ------------------------------------------------
    await asserts.url('/partnership-details/ended-check')
    await asserts.accessibility()
    await asserts.h1('Have you ever been married or in a civil partnership that ended?')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Partner Died page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Partner Died page
    # ------------------------------------------------
    await asserts.url('/partnership-details/partner-died')
    await asserts.accessibility()
    await asserts.h1('Were you previously married or in a civil partnership, and your spouse or partner died?')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='partner_died', value='Yes')
    await asserts.not_checked(field='partner_died', value='No')

    # Continue to Partnership Ended page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Partnership Ended page
    # ------------------------------------------------
    await asserts.url('/partnership-details/ended-check')
    await asserts.accessibility()
    await asserts.h1('Have you ever been married or in a civil partnership that ended?')
    await asserts.number_of_errors(0)

    # Don't select an option, click "Save and continue"
    await helpers.click_button('Save and continue')
    await asserts.url('/partnership-details/ended-check')
    await asserts.accessibility()
    await asserts.h1('Have you ever been married or in a civil partnership that ended?')
    await asserts.number_of_errors(1)
    await asserts.error(field='previous_partnership_ended', message='Select if you have ever been married or in a civil partnership that has ended')

    # Select a valid option, click "Save and continue"
    await helpers.check_radio(field='previous_partnership_ended', value='Yes')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Marriage details: Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/partnership-details/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers: Marriage or civil partnership details')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Partner Died page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Partnership Ended page
    # ------------------------------------------------
    await asserts.url('/partnership-details/ended-check')
    await asserts.accessibility()
    await asserts.h1('Have you ever been married or in a civil partnership that ended?')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='previous_partnership_ended', value='Yes')
    await asserts.not_checked(field='previous_partnership_ended', value='No')

    # Continue to Marriage details: Check Your Answers page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Marriage details: Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/partnership-details/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers: Marriage or civil partnership details')
    await asserts.number_of_errors(0)

    # Check the values in the table
    await asserts.check_your_answers_rows(3)
    await asserts.check_your_answers_row(row_name='Currently married or in a civil partnership', expected_value='Neither')
    await asserts.check_your_answers_row(row_name='Spouse or partner has died', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Marriage or civil partnership has ended', expected_value='Yes')

    # Click each "Change" link to check it takes us to the correct page
    await asserts.change_links_to_url(link_text='Change if you are currently married or in a civil partnership', expected_url='/partnership-details')
    await asserts.change_links_to_url(link_text='Change if your spouse or partner has died', expected_url='/partnership-details/partner-died')
    await asserts.change_links_to_url(link_text='Change if your marriage or civil partnership has ended', expected_url='/partnership-details/ended-check')

    # Click "Back" to get back to the "Are You Married" page, then choose "Married"
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Partnership Ended page
    # ------------------------------------------------
    await asserts.url('/partnership-details/ended-check')
    await asserts.accessibility()
    await asserts.h1('Have you ever been married or in a civil partnership that ended?')
    await asserts.number_of_errors(0)

    # Click "Back" to get back to the "Are You Married" page, then choose "Married"
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Partner Died page
    # ------------------------------------------------
    await asserts.url('/partnership-details/partner-died')
    await asserts.accessibility()
    await asserts.h1('Were you previously married or in a civil partnership, and your spouse or partner died?')
    await asserts.number_of_errors(0)

    # Click "Back" to get back to the "Are You Married" page, then choose "Married"
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Are You Married page
    # ------------------------------------------------
    await asserts.url('/partnership-details')
    await asserts.accessibility()
    await asserts.h1('Marriages and civil partnerships')
    await asserts.number_of_errors(0)

    # Choose the "Married" option and go down that path
    await helpers.check_radio(field='currently_married', value='Married')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Stay Together page
    # ------------------------------------------------
    await asserts.url('/partnership-details/stay-together')
    await asserts.accessibility()
    await asserts.h1('Do you plan to remain married after you receive your Gender Recognition Certificate?')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the "Are You Married" page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Are You Married page
    # ------------------------------------------------
    await asserts.url('/partnership-details')
    await asserts.accessibility()
    await asserts.h1('Marriages and civil partnerships')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='currently_married', value='Married')
    await asserts.not_checked(field='currently_married', value='Civil partnership')
    await asserts.not_checked(field='currently_married', value='Neither')

    # Continue to the Stay Together page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Stay Together page
    # ------------------------------------------------
    await asserts.url('/partnership-details/stay-together')
    await asserts.accessibility()
    await asserts.h1('Do you plan to remain married after you receive your Gender Recognition Certificate?')
    await asserts.number_of_errors(0)

    # Don't select an option, click "Save and continue"
    await helpers.click_button('Save and continue')
    await asserts.url('/partnership-details/stay-together')
    await asserts.accessibility()
    await asserts.h1('Do you plan to remain married after you receive your Gender Recognition Certificate?')
    await asserts.number_of_errors(1)
    await asserts.error(field='stay_together', message='Select if you plan to remain married after receiving your Gender Recognition Certificate')

    # Select the "No" option, go down that route
    # Then backtrack and choose "Yes
    await helpers.check_radio(field='stay_together', value='No')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Stay Together page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Stay Together page
    # ------------------------------------------------
    await asserts.url('/partnership-details/stay-together')
    await asserts.accessibility()
    await asserts.h1('Do you plan to remain married after you receive your Gender Recognition Certificate?')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='stay_together', value='No')
    await asserts.not_checked(field='stay_together', value='Yes')

    # Continue to the Interim GRC page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.number_of_errors(0)

    # Click "Continue"
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Marriage details: Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/partnership-details/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers: Marriage or civil partnership details')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Interim GRC page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.number_of_errors(0)

    # Continue to the Marriage details: Check Your Answers page
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Marriage details: Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/partnership-details/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers: Marriage or civil partnership details')
    await asserts.number_of_errors(0)

    # Check the values in the table
    await asserts.check_your_answers_rows(3)
    await asserts.check_your_answers_row(row_name='Currently married or in a civil partnership', expected_value='Married')
    await asserts.check_your_answers_row(row_name='Remain married', expected_value='No')
    await asserts.check_your_answers_row(row_name='Interim GRC', expected_value='Yes')

    # Click each "Change" link to check it takes us to the correct page
    await asserts.change_links_to_url(link_text='Change if you are currently married or in a civil partnership', expected_url='/partnership-details')
    await asserts.change_links_to_url(link_text='Change if you plan to remain married after receiving your Gender Recognition Certificate', expected_url='/partnership-details/stay-together')
    await asserts.change_links_to_url(link_text='Change if you understand that you will receive an Interim GRC', expected_url='/partnership-details/interim-check')

    # Click "Back" to get back to the "Stay Together" page, then choose "Yes"
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.number_of_errors(0)

    # Click "Back" to get back to the "Stay Together" page, then choose "Yes"
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Stay Together page
    # ------------------------------------------------
    await asserts.url('/partnership-details/stay-together')
    await asserts.accessibility()
    await asserts.h1('Do you plan to remain married after you receive your Gender Recognition Certificate?')
    await asserts.number_of_errors(0)

    # Now choose the "Yes" option
    await helpers.check_radio(field='stay_together', value='Yes')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Partner Agrees page
    # ------------------------------------------------
    await asserts.url('/partnership-details/partner-agrees')
    await asserts.accessibility()
    await asserts.h1('Declaration of consent')
    await asserts.fieldset_legend('Can you provide a statutory declaration from your spouse?')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Stay Together page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Stay Together page
    # ------------------------------------------------
    await asserts.url('/partnership-details/stay-together')
    await asserts.accessibility()
    await asserts.h1('Do you plan to remain married after you receive your Gender Recognition Certificate?')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='stay_together', value='Yes')
    await asserts.not_checked(field='stay_together', value='No')

    # Continue to the Partner Agrees page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Partner Agrees page
    # ------------------------------------------------
    await asserts.url('/partnership-details/partner-agrees')
    await asserts.accessibility()
    await asserts.h1('Declaration of consent')
    await asserts.fieldset_legend('Can you provide a statutory declaration from your spouse?')
    await asserts.number_of_errors(0)

    # Don't select an option, click "Save and continue"
    await helpers.click_button('Save and continue')
    await asserts.url('/partnership-details/partner-agrees')
    await asserts.accessibility()
    await asserts.h1('Declaration of consent')
    await asserts.fieldset_legend('Can you provide a statutory declaration from your spouse?')
    await asserts.number_of_errors(1)
    await asserts.error(field='partner_agrees', message='Select if you can provide a declaration of consent from your spouse')

    # Select the "No" option, go down that route
    # Then backtrack and choose "Yes
    await helpers.check_radio(field='partner_agrees', value='No')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Partner Agrees page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Partner Agrees page
    # ------------------------------------------------
    await asserts.url('/partnership-details/partner-agrees')
    await asserts.accessibility()
    await asserts.h1('Declaration of consent')
    await asserts.fieldset_legend('Can you provide a statutory declaration from your spouse?')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='partner_agrees', value='No')
    await asserts.not_checked(field='partner_agrees', value='Yes')

    # Continue to the Interim GRC page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.number_of_errors(0)

    # Continue to the Marriage details: Check Your Answers page
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Marriage details: Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/partnership-details/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers: Marriage or civil partnership details')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Interim GRC page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.number_of_errors(0)

    # Continue to the Marriage details: Check Your Answers page
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Marriage details: Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/partnership-details/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers: Marriage or civil partnership details')
    await asserts.number_of_errors(0)

    # Check the values in the table
    await asserts.check_your_answers_rows(4)
    await asserts.check_your_answers_row(row_name='Currently married or in a civil partnership', expected_value='Married')
    await asserts.check_your_answers_row(row_name='Remain married', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Can provide a declaration of consent from your spouse', expected_value='No')
    await asserts.check_your_answers_row(row_name='Interim GRC', expected_value='Yes')

    # Click each "Change" link to check it takes us to the correct page
    await asserts.change_links_to_url(link_text='Change if you are currently married or in a civil partnership', expected_url='/partnership-details')
    await asserts.change_links_to_url(link_text='Change if you plan to remain married after receiving your Gender Recognition Certificate', expected_url='/partnership-details/stay-together')
    await asserts.change_links_to_url(link_text='Change if you can provide a declaration of consent from your spouse', expected_url='/partnership-details/partner-agrees')
    await asserts.change_links_to_url(link_text='Change if you understand that you will receive an Interim GRC', expected_url='/partnership-details/interim-check')

    # Click "Back" to get back to the "Partner Agrees" page, then choose "Yes"
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.number_of_errors(0)

    # Click "Back" to get back to the "Partner Agrees" page, then choose "Yes"
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Partner Agrees page
    # ------------------------------------------------
    await asserts.url('/partnership-details/partner-agrees')
    await asserts.accessibility()
    await asserts.h1('Declaration of consent')
    await asserts.fieldset_legend('Can you provide a statutory declaration from your spouse?')
    await asserts.number_of_errors(0)

    # This time, select the "Yes" option
    await helpers.check_radio(field='partner_agrees', value='Yes')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Marriage details: Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/partnership-details/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers: Marriage or civil partnership details')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Partner Agrees page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Partner Agrees page
    # ------------------------------------------------
    await asserts.url('/partnership-details/partner-agrees')
    await asserts.accessibility()
    await asserts.h1('Declaration of consent')
    await asserts.fieldset_legend('Can you provide a statutory declaration from your spouse?')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='partner_agrees', value='Yes')
    await asserts.not_checked(field='partner_agrees', value='No')

    # Continue to the Marriage details: Check Your Answers page
    await helpers.click_button('Save and continue')

    # Check the values in the table
    await asserts.check_your_answers_rows(3)
    await asserts.check_your_answers_row(row_name='Currently married or in a civil partnership', expected_value='Married')
    await asserts.check_your_answers_row(row_name='Remain married', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Can provide a declaration of consent from your spouse', expected_value='Yes')

    # Click each "Change" link to check it takes us to the correct page
    await asserts.change_links_to_url(link_text='Change if you are currently married or in a civil partnership', expected_url='/partnership-details')
    await asserts.change_links_to_url(link_text='Change if you plan to remain married after receiving your Gender Recognition Certificate', expected_url='/partnership-details/stay-together')
    await asserts.change_links_to_url(link_text='Change if you can provide a declaration of consent from your spouse', expected_url='/partnership-details/partner-agrees')

    # TODO Hold up!
    #  Before we continue to the Task List, we should
    #  check that selecting "Civil partnership" changes all the text appropriately

    # Click "Save and continue" to finish this section (Phew!) and return to the Task List page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Status of "Marriage or civil partnership details" section should be "COMPLETED"
    await asserts.task_list_sections(9)
    await asserts.task_list_section(section='Confirmation', expected_status='COMPLETED')
    await asserts.task_list_section(section='Your personal details', expected_status='COMPLETED')
    await asserts.task_list_section(section='Your birth registration information', expected_status='COMPLETED')
    await asserts.task_list_section(section='Marriage or civil partnership details', expected_status='COMPLETED')
    await asserts.task_list_section(section='Name change documents', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Marriage documents', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Overseas certificate documents', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Statutory declarations', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Submit and pay', expected_status='CANNOT START YET')

    # Click "Name change documents" to go to the "Name Change Documents" page
    await helpers.click_button('Name change documents')

    # ------------------------------------------------
    # ---- Name Change Documents page
    # ------------------------------------------------
    await asserts.url('/upload/name-change')
    await asserts.accessibility()
    await asserts.h1('Upload name change documents')
    await asserts.number_of_errors(0)

    # "Back" should take us to the Task List page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Continue to the "Name Change Documents" page again
    await helpers.click_button('Name change documents')

    # ------------------------------------------------
    # ---- Name Change Documents page
    # ------------------------------------------------
    await asserts.url('/upload/name-change')
    await asserts.accessibility()
    await asserts.h1('Upload name change documents')
    await asserts.number_of_errors(0)









    await browser.close()
    asserts.run_final_accessibility_checks()


async def e2e_main():
    print("")  # Blank line to improve formatting
    async with async_playwright() as p:
        for browser_type in [p.chromium]: #, p.firefox, p.webkit]:
            await run_script_for_browser(browser_type)


def test_e2e():
    asyncio.run(e2e_main())
