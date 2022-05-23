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
    await helpers.fill_textbox(field='first_name', value=data.BIRTH_FIRST_NAME)
    await helpers.fill_textbox(field='middle_names', value=data.BIRTH_MIDDLE_NAME)
    await helpers.fill_textbox(field='last_name', value=data.BIRTH_LAST_NAME)
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
    await asserts.field_value(field='first_name', expected_value=data.BIRTH_FIRST_NAME)
    await asserts.field_value(field='middle_names', expected_value=data.BIRTH_MIDDLE_NAME)
    await asserts.field_value(field='last_name', expected_value=data.BIRTH_LAST_NAME)

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
    await helpers.fill_textbox(field='day', value=data.DATE_OF_BIRTH_DAY)
    await helpers.fill_textbox(field='month', value=data.DATE_OF_BIRTH_MONTH)
    await helpers.fill_textbox(field='year', value='2222')
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration/dob')
    await asserts.accessibility()
    await asserts.h1('What is the date of birth on your birth or adoption certificate?')
    await asserts.number_of_errors(1)
    await asserts.error(field='year', message='You need to be at least 18 years old to apply')

    # Enter a valid date too far in the past, click "Save and continue"
    await helpers.fill_textbox(field='day', value=data.DATE_OF_BIRTH_DAY)
    await helpers.fill_textbox(field='month', value=data.DATE_OF_BIRTH_MONTH)
    await helpers.fill_textbox(field='year', value='1900')
    await helpers.click_button('Save and continue')
    await asserts.url('/birth-registration/dob')
    await asserts.accessibility()
    await asserts.h1('What is the date of birth on your birth or adoption certificate?')
    await asserts.number_of_errors(1)
    await asserts.error(field='year', message='You need to be less than 110 years old to apply')

    # Enter valid values, click "Save and continue"
    await helpers.fill_textbox(field='day', value=data.DATE_OF_BIRTH_DAY)
    await helpers.fill_textbox(field='month', value=data.DATE_OF_BIRTH_MONTH)
    await helpers.fill_textbox(field='year', value=data.DATE_OF_BIRTH_YEAR)
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
    await asserts.field_value(field='day', expected_value=data.DATE_OF_BIRTH_DAY)
    await asserts.field_value(field='month', expected_value=data.DATE_OF_BIRTH_MONTH)
    await asserts.field_value(field='year', expected_value=data.DATE_OF_BIRTH_YEAR)

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
    await helpers.fill_textbox(field='country_of_birth', value=data.BIRTH_COUNTRY)
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
    await asserts.field_value(field='country_of_birth', expected_value=data.BIRTH_COUNTRY)

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
    await asserts.check_your_answers_row(row_name='Birth name', expected_value=f"{data.BIRTH_FIRST_NAME} {data.BIRTH_MIDDLE_NAME} {data.BIRTH_LAST_NAME}")
    await asserts.check_your_answers_row(row_name='Date of birth', expected_value=data.DATE_OF_BIRTH_FORMATTED)
    await asserts.check_your_answers_row(row_name='Birth registered in UK', expected_value='No')
    await asserts.check_your_answers_row(row_name='Registered birth country', expected_value=data.BIRTH_COUNTRY)

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
    await helpers.fill_textbox(field='place_of_birth', value=data.BIRTH_TOWN)
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
    await asserts.field_value(field='place_of_birth', expected_value=data.BIRTH_TOWN)

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
    await helpers.fill_textbox(field='first_name', value=data.MOTHERS_FIRST_NAME)
    await helpers.fill_textbox(field='last_name', value=data.MOTHERS_LAST_NAME)
    await helpers.fill_textbox(field='maiden_name', value=data.MOTHERS_MAIDEN_NAME)
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
    await asserts.field_value(field='first_name', expected_value=data.MOTHERS_FIRST_NAME)
    await asserts.field_value(field='last_name', expected_value=data.MOTHERS_LAST_NAME)
    await asserts.field_value(field='maiden_name', expected_value=data.MOTHERS_MAIDEN_NAME)

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
    await helpers.fill_textbox(field='first_name', value=data.FATHERS_FIRST_NAME)
    await helpers.fill_textbox(field='last_name', value=data.FATHERS_LAST_NAME)
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
    await asserts.field_value(field='first_name', expected_value=data.FATHERS_FIRST_NAME)
    await asserts.field_value(field='last_name', expected_value=data.FATHERS_LAST_NAME)

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
    await asserts.check_your_answers_row(row_name='Birth name', expected_value=f"{data.BIRTH_FIRST_NAME} {data.BIRTH_MIDDLE_NAME} {data.BIRTH_LAST_NAME}")
    await asserts.check_your_answers_row(row_name='Date of birth', expected_value=data.DATE_OF_BIRTH_FORMATTED)
    await asserts.check_your_answers_row(row_name='Birth registered in UK', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Town or city of birth', expected_value=data.BIRTH_TOWN)
    await asserts.check_your_answers_row(row_name="Mother's name", expected_value=f"{data.MOTHERS_FIRST_NAME} {data.MOTHERS_LAST_NAME}\n(Maiden name: {data.MOTHERS_MAIDEN_NAME})")
    await asserts.check_your_answers_row(row_name="Father's name listed", expected_value='Yes')
    await asserts.check_your_answers_row(row_name="Father's name", expected_value=f"{data.FATHERS_FIRST_NAME} {data.FATHERS_LAST_NAME}")
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
