from playwright.async_api import Page
from tests.helpers.e2e_assert_helpers import AssertHelpers
from tests.helpers.e2e_page_helpers import PageHelpers
import tests.end_to_end_tests.journey_1.data as data


async def run_checks_on_section(page: Page, asserts: AssertHelpers, helpers: PageHelpers):

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

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
    await helpers.fill_textbox(field='title', value=data.TITLE)
    await helpers.fill_textbox(field='first_name', value=data.FIRST_NAME)
    await helpers.fill_textbox(field='middle_names', value=data.MIDDLE_NAMES)
    await helpers.fill_textbox(field='last_name', value=data.LAST_NAME)
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
    await asserts.field_value(field='title', expected_value=data.TITLE)
    await asserts.field_value(field='first_name', expected_value=data.FIRST_NAME)
    await asserts.field_value(field='middle_names', expected_value=data.MIDDLE_NAMES)
    await asserts.field_value(field='last_name', expected_value=data.LAST_NAME)

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
    # This should now take you to the "Your Name" page
    await helpers.click_button('Your personal details')

    # ------------------------------------------------
    # ---- Your Name page
    # ------------------------------------------------
    await asserts.url('/personal-details')
    await asserts.accessibility()
    await asserts.h1('What is your name?')
    await asserts.number_of_errors(0)

    # Continue on to the Affirmed Gender page
    await helpers.click_button('Save and continue')

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

    # Enter a valid date that is not 2 years prior to application created date
    await helpers.fill_textbox(field='transition_date_month', value=data.TRANSITION_DATE_MONTH_INVALID)
    await helpers.fill_textbox(field='transition_date_year', value=data.TRANSITION_DATE_YEAR_INVALID)
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/transition-date')
    await asserts.accessibility()
    await asserts.h1('When did you transition?')
    await asserts.number_of_errors(1)
    await asserts.error(field='transition_date_year', message='Enter a date at least 2 years before your application')

    # Enter a valid date
    await helpers.fill_textbox(field='transition_date_month', value=data.TRANSITION_DATE_MONTH)
    await helpers.fill_textbox(field='transition_date_year', value=data.TRANSITION_DATE_YEAR)
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Statutory Declaration Date page
    # ------------------------------------------------
    await asserts.url('/personal-details/statutory-declaration-date')
    await asserts.accessibility()
    await asserts.h1('When did you sign your statutory declaration?')
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
    await asserts.field_value(field='transition_date_month', expected_value=data.TRANSITION_DATE_MONTH)
    await asserts.field_value(field='transition_date_year', expected_value=data.TRANSITION_DATE_YEAR)

    # Click Save and continue to return to Statutory Declaration Date page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Statutory Declaration Date page
    # ------------------------------------------------
    await asserts.url('/personal-details/statutory-declaration-date')
    await asserts.accessibility()
    await asserts.h1('When did you sign your statutory declaration?')
    await asserts.number_of_errors(0)

    # Don't enter any values, click Save and continue
    await helpers.fill_textbox(field='statutory_declaration_date_day', value='')
    await helpers.fill_textbox(field='statutory_declaration_date_month', value='')
    await helpers.fill_textbox(field='statutory_declaration_date_year', value='')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/statutory-declaration-date')
    await asserts.accessibility()
    await asserts.h1('When did you sign your statutory declaration?')
    await asserts.number_of_errors(3)
    await asserts.error(field='statutory_declaration_date_day', message='Enter a day')
    await asserts.error(field='statutory_declaration_date_month', message='Enter a month')
    await asserts.error(field='statutory_declaration_date_year', message='Enter a year')

    # Enter values that aren't numbers, click Save and continue
    await helpers.fill_textbox(field='statutory_declaration_date_day', value='AA')
    await helpers.fill_textbox(field='statutory_declaration_date_month', value='BB')
    await helpers.fill_textbox(field='statutory_declaration_date_year', value='CCCC')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/statutory-declaration-date')
    await asserts.accessibility()
    await asserts.h1('When did you sign your statutory declaration?')
    await asserts.number_of_errors(3)
    await asserts.error(field='statutory_declaration_date_day', message='Enter a day as a number between 1 and 31')
    await asserts.error(field='statutory_declaration_date_month', message='Enter a month as a number between 1 and 12')
    await asserts.error(field='statutory_declaration_date_year', message='Enter a year as a 4-digit number, like 2000')

    # Enter values that are fractional numbers
    await helpers.fill_textbox(field='statutory_declaration_date_day', value='1.2')
    await helpers.fill_textbox(field='statutory_declaration_date_month', value='3.4')
    await helpers.fill_textbox(field='statutory_declaration_date_year', value='2000.4')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/statutory-declaration-date')
    await asserts.accessibility()
    await asserts.h1('When did you sign your statutory declaration?')
    await asserts.number_of_errors(3)
    await asserts.error(field='statutory_declaration_date_day', message='Enter a day as a number between 1 and 31')
    await asserts.error(field='statutory_declaration_date_month', message='Enter a month as a number between 1 and 12')
    await asserts.error(field='statutory_declaration_date_year', message='Enter a year as a 4-digit number, like 2000')

    # Enter values that are too low
    await helpers.fill_textbox(field='statutory_declaration_date_day', value='0')
    await helpers.fill_textbox(field='statutory_declaration_date_month', value='0')
    await helpers.fill_textbox(field='statutory_declaration_date_year', value='999')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/statutory-declaration-date')
    await asserts.accessibility()
    await asserts.h1('When did you sign your statutory declaration?')
    await asserts.number_of_errors(3)
    await asserts.error(field='statutory_declaration_date_day', message='Enter a day as a number between 1 and 31')
    await asserts.error(field='statutory_declaration_date_month', message='Enter a month as a number between 1 and 12')
    await asserts.error(field='statutory_declaration_date_year', message='Enter a year as a 4-digit number, like 2000')

    # Enter a month that is too high
    await helpers.fill_textbox(field='statutory_declaration_date_day', value='32')
    await helpers.fill_textbox(field='statutory_declaration_date_month', value='13')
    await helpers.fill_textbox(field='statutory_declaration_date_year', value='2000')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/statutory-declaration-date')
    await asserts.accessibility()
    await asserts.h1('When did you sign your statutory declaration?')
    await asserts.number_of_errors(2)
    await asserts.error(field='statutory_declaration_date_day', message='Enter a day as a number between 1 and 31')
    await asserts.error(field='statutory_declaration_date_month', message='Enter a month as a number between 1 and 12')

    # Enter a valid date that is more than 100 years' ago
    await helpers.fill_textbox(field='statutory_declaration_date_day', value='6')
    await helpers.fill_textbox(field='statutory_declaration_date_month', value='7')
    await helpers.fill_textbox(field='statutory_declaration_date_year', value='1900')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/statutory-declaration-date')
    await asserts.accessibility()
    await asserts.h1('When did you sign your statutory declaration?')
    await asserts.number_of_errors(1)
    await asserts.error(field='statutory_declaration_date_year', message='Enter a date within the last 100 years')

    # Enter a valid date
    await helpers.fill_textbox(field='statutory_declaration_date_day', value=data.STATUTORY_DECLARATION_DATE_DAY)
    await helpers.fill_textbox(field='statutory_declaration_date_month', value=data.STATUTORY_DECLARATION_DATE_MONTH)
    await helpers.fill_textbox(field='statutory_declaration_date_year', value=data.STATUTORY_DECLARATION_DATE_YEAR)
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Previous Name Check page
    # ------------------------------------------------
    await asserts.url('/personal-details/previous-names-check')
    await asserts.accessibility()
    await asserts.h1('If you have ever changed your name to reflect your gender')
    await asserts.number_of_errors(0)

    # "Back" link should take you to the Statutory Declaration Date page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Statutory Declaration Date page
    # ------------------------------------------------
    await asserts.url('/personal-details/statutory-declaration-date')
    await asserts.accessibility()
    await asserts.h1('When did you sign your statutory declaration?')
    await asserts.number_of_errors(0)

    # The fields should be pre-populated with the values we just entered
    await asserts.field_value(field='statutory_declaration_date_day', expected_value=data.STATUTORY_DECLARATION_DATE_DAY)
    await asserts.field_value(field='statutory_declaration_date_month', expected_value=data.STATUTORY_DECLARATION_DATE_MONTH)
    await asserts.field_value(field='statutory_declaration_date_year', expected_value=data.STATUTORY_DECLARATION_DATE_YEAR)

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
    await helpers.check_radio(field='previousNameCheck', value='True')
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
    await asserts.is_checked(field='previousNameCheck', value='True')
    await asserts.not_checked(field='previousNameCheck', value='False')

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
    await asserts.number_of_errors(3)
    await asserts.error(field='address_line_one', message='Enter your address')
    await asserts.error(field='town', message='Enter your town or city')
    await asserts.error(field='postcode', message='Enter your postcode')

    # Enter valid values, click Save and continue
    await helpers.fill_textbox(field='address_line_one', value=data.ADDRESS_LINE_ONE)
    await helpers.fill_textbox(field='address_line_two', value=data.ADDRESS_LINE_TWO)
    await helpers.fill_textbox(field='town', value=data.TOWN)
    await helpers.fill_textbox(field='postcode', value=data.POSTCODE)
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
    await asserts.field_value(field='address_line_one', expected_value=data.ADDRESS_LINE_ONE)
    await asserts.field_value(field='address_line_two', expected_value=data.ADDRESS_LINE_TWO)
    await asserts.field_value(field='town', expected_value=data.TOWN)
    await asserts.field_value(field='postcode', expected_value=data.POSTCODE)

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
    await helpers.check_radio(field='contactDatesCheck', value='True')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/contact-dates')
    await asserts.accessibility()
    await asserts.h1('If we need to contact you by post in the next 6 months, are there any dates we should avoid?')
    await asserts.number_of_errors(1)
    await asserts.error(field='dates', message="Enter the dates you don't want us to contact you by post")

    # Enter some valid dates
    await helpers.check_radio(field='contactDatesCheck', value='True')
    await helpers.fill_textbox(field='dates', value=data.DATES_TO_AVOID)
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
    await asserts.is_checked(field='contactDatesCheck', value='True')
    await asserts.not_checked(field='contactDatesCheck', value='False')
    await asserts.field_value(field='dates', expected_value=data.DATES_TO_AVOID)

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
    await helpers.fill_textbox(field='email', value=data.EMAIL_ADDRESS)
    await helpers.check_checkbox(field='contact_options', value='PHONE')
    await helpers.fill_textbox(field='phone', value=data.PHONE_NUMBER)
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
    await asserts.field_value(field='email', expected_value=data.EMAIL_ADDRESS)
    await asserts.field_value(field='phone', expected_value=data.PHONE_NUMBER)

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
    await helpers.check_radio(field='tell_hmrc', value='True')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/hmrc')
    await asserts.accessibility()
    await asserts.h1('Notifying HMRC')
    await asserts.number_of_errors(1)
    await asserts.error(field='national_insurance_number', message='Enter your National Insurance number')

    # Enter an invalid National Insurance number
    await helpers.check_radio(field='tell_hmrc', value='True')
    await helpers.fill_textbox(field='national_insurance_number', value='INVALID-NI')
    await helpers.click_button('Save and continue')
    await asserts.url('/personal-details/hmrc')
    await asserts.accessibility()
    await asserts.h1('Notifying HMRC')
    await asserts.number_of_errors(1)
    await asserts.error(field='national_insurance_number', message='Enter a valid National Insurance number')

    # Enter a valid National Insurance number
    await helpers.check_radio(field='tell_hmrc', value='True')
    await helpers.fill_textbox(field='national_insurance_number', value=data.NATIONAL_INSURANCE_NUMBER)
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
    await asserts.is_checked(field='tell_hmrc', value='True')
    await asserts.not_checked(field='tell_hmrc', value='False')
    await asserts.field_value(field='national_insurance_number', expected_value=data.NATIONAL_INSURANCE_NUMBER)

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
    await asserts.check_your_answers_rows(10)
    await asserts.check_your_answers_row(row_name='Name', expected_value=f"{data.TITLE} {data.FIRST_NAME} {data.MIDDLE_NAMES} {data.LAST_NAME}")
    await asserts.check_your_answers_row(row_name='Affirmed gender', expected_value='Male')
    await asserts.check_your_answers_row(row_name='When you transitioned', expected_value=data.TRANSITION_DATE_FORMATTED)
    await asserts.check_your_answers_row(row_name='When you signed your statutory declaration', expected_value=data.STATUTORY_DECLARATION_DATE_FORMATTED)
    await asserts.check_your_answers_row(row_name='Ever changed name', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Address', expected_value=f"{data.ADDRESS_LINE_ONE}\n{data.ADDRESS_LINE_TWO}\n{data.TOWN}\n{data.POSTCODE}")
    await asserts.check_your_answers_row(row_name='Contact preferences', expected_value=f"Email: {data.EMAIL_ADDRESS}\nPhone: {data.PHONE_NUMBER}\nPost: {data.ADDRESS_LINE_ONE}, {data.ADDRESS_LINE_TWO}, {data.TOWN}, {data.POSTCODE}")
    await asserts.check_your_answers_row(row_name='Unavailable over the next 6 months', expected_value=f"Yes\n{data.DATES_TO_AVOID}")
    await asserts.check_your_answers_row(row_name='Notify HMRC', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='National insurance number', expected_value=data.NATIONAL_INSURANCE_NUMBER)

    # Click each "Change" link to check it takes us to the correct page
    await asserts.change_links_to_url(link_text='Change name', expected_url='/personal-details')
    await asserts.change_links_to_url(link_text='Change affirmed gender', expected_url='/personal-details/affirmed-gender')
    await asserts.change_links_to_url(link_text='Change when you transitioned', expected_url='/personal-details/transition-date')
    await asserts.change_links_to_url(link_text='Change when you signed your statutory declaration', expected_url='/personal-details/statutory-declaration-date')
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

    await helpers.check_radio(field='tell_hmrc', value='False')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/personal-details/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers: Your personal details')
    await asserts.number_of_errors(0)

    await asserts.check_your_answers_rows(9)
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
