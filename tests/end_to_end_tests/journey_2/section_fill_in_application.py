from playwright.async_api import Page
from tests.helpers.e2e_assert_helpers import AssertHelpers
from tests.helpers.e2e_page_helpers import PageHelpers
import tests.end_to_end_tests.journey_2.data as data


async def fill_in_application(page: Page, asserts: AssertHelpers, helpers: PageHelpers):
    # ------------------------------------------------
    # ---- Homepage / Email address page
    # ------------------------------------------------
    await asserts.url('/')
    await asserts.accessibility()
    await asserts.h1('Email address')
    await asserts.number_of_errors(0)

    # Enter a valid Email Address, click Continue button, see the Security Code page
    await helpers.fill_textbox(field='email', value=data.EMAIL_ADDRESS)
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Security Code page
    # ------------------------------------------------
    await asserts.url('/security-code')
    await asserts.accessibility()
    await asserts.h1('Enter security code')
    await asserts.number_of_errors(0)

    # Enter a valid Security Code, click Continue button
    await helpers.fill_textbox(field='security_code', value='11111')
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Is First Visit page
    # ------------------------------------------------
    await asserts.url('/is-first-visit')
    await asserts.accessibility()
    await asserts.h1('Have you already started an application?')
    await asserts.number_of_errors(0)

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

    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Overseas Check page
    # ------------------------------------------------
    await asserts.url('/overseas-check')
    await asserts.accessibility()
    await asserts.h1('Have you ever been issued a Gender Recognition Certificate (or its equivalent) in another country?')
    await asserts.number_of_errors(0)

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

    # Click "Your personal details"
    await helpers.click_button('Your personal details')

    # ------------------------------------------------
    # ---- Your Name page
    # ------------------------------------------------
    await asserts.url('/personal-details')
    await asserts.accessibility()
    await asserts.h1('What is your name?')
    await asserts.number_of_errors(0)

    # Enter valid details, click Save and continue
    await helpers.fill_textbox(field='title', value=data.TITLE)
    await helpers.fill_textbox(field='first_name', value=data.FIRST_NAME)
    await helpers.fill_textbox(field='last_name', value=data.LAST_NAME)
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Affirmed Gender page
    # ------------------------------------------------
    await asserts.url('/personal-details/affirmed-gender')
    await asserts.accessibility()
    await asserts.h1('What is your affirmed gender?')
    await asserts.number_of_errors(0)

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

    # Enter some valid dates
    await helpers.check_radio(field='contactDatesCheck', value='Yes')
    await helpers.fill_textbox(field='dates', value=data.DATES_TO_AVOID)
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Contact Preferences page
    # ------------------------------------------------
    await asserts.url('/personal-details/contact-preferences')
    await asserts.accessibility()
    await asserts.h1('How would you like to be contacted if we have any questions about your application?')
    await asserts.number_of_errors(0)

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

    # Enter a valid National Insurance number
    await helpers.check_radio(field='tell_hmrc', value='Yes')
    await helpers.fill_textbox(field='national_insurance_number', value=data.NATIONAL_INSURANCE_NUMBER)
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/personal-details/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers: Your personal details')
    await asserts.number_of_errors(0)

    # Click Save and continue to return to Task List page
    await helpers.click_button('Save and continue')

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

    # Click "Save and continue"
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Click "Marriage or civil partnership details" to go to the "Are You Married" page
    await helpers.click_button('Marriage or civil partnership details')

    # ------------------------------------------------
    # ---- Are You Married page
    # ------------------------------------------------
    await asserts.url('/partnership-details')
    await asserts.accessibility()
    await asserts.h1('Marriages and civil partnerships')
    await asserts.number_of_errors(0)

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

    # Click "Save and continue" to finish this section (Phew!) and return to the Task List page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Click "Name change documents" to go to the "Name Change Documents" page
    await helpers.click_button('Name change documents')

    # ------------------------------------------------
    # ---- Name Change Documents page
    # ------------------------------------------------
    await asserts.url('/upload/name-change')
    await asserts.accessibility()
    await asserts.h1('Upload name change documents')
    await asserts.number_of_errors(0)
    await asserts.documents_uploaded(0)

    DOCUMENT_ONE_NAME = 'document_1.bmp'

    # Upload a valid document
    await helpers.upload_file_valid(field='documents', file_name=DOCUMENT_ONE_NAME)
    await helpers.click_button('Upload file')
    await asserts.url('/upload/name-change')
    await asserts.accessibility()
    await asserts.h1('Upload name change documents')
    await asserts.number_of_errors(0)
    await asserts.documents_uploaded(1)

    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Click "Marriage documents" to go to the "Marriage Documents" page
    await helpers.click_button('Marriage and civil partnership documents')

    # ------------------------------------------------
    # ---- Marriage Documents page
    # ------------------------------------------------
    await asserts.url('/upload/marriage-documents')
    await asserts.accessibility()
    await asserts.h1('Upload marriage and civil partnership documents')
    await asserts.number_of_errors(0)
    await asserts.documents_uploaded(0)

    DOCUMENT_ONE_NAME = 'document_1.bmp'

    # Upload a valid document
    await helpers.upload_file_valid(field='documents', file_name=DOCUMENT_ONE_NAME)
    await helpers.click_button('Upload file')
    await asserts.url('/upload/marriage-documents')
    await asserts.accessibility()
    await asserts.h1('Upload marriage and civil partnership documents')
    await asserts.number_of_errors(0)
    await asserts.documents_uploaded(1)

    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Click "Overseas certificate documents" to go to the "Overseas certificate Documents" page
    await helpers.click_button('Overseas certificate documents')

    # ------------------------------------------------
    # ---- Overseas Certificate page
    # ------------------------------------------------
    await asserts.url('/upload/overseas-certificate')
    await asserts.accessibility()
    await asserts.h1('Overseas gender recognition certificate documents')
    await asserts.number_of_errors(0)
    await asserts.documents_uploaded(0)

    DOCUMENT_ONE_NAME = 'document_1.bmp'

    # Upload a valid document
    await helpers.upload_file_valid(field='documents', file_name=DOCUMENT_ONE_NAME)
    await helpers.click_button('Upload file')
    await asserts.url('/upload/overseas-certificate')
    await asserts.accessibility()
    await asserts.h1('Overseas gender recognition certificate documents')
    await asserts.number_of_errors(0)
    await asserts.documents_uploaded(1)

    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Click "Statutory declarations" to go to the "Statutory Declarations" page
    await helpers.click_button('Statutory declarations')

    # ------------------------------------------------
    # ---- Statutory Declarations page
    # ------------------------------------------------
    await asserts.url('/upload/statutory-declarations')
    await asserts.accessibility()
    await asserts.h1('Statutory declarations documents')
    await asserts.number_of_errors(0)
    await asserts.documents_uploaded(0)

    DOCUMENT_ONE_NAME = 'document_1.bmp'

    # Upload a valid document
    await helpers.upload_file_valid(field='documents', file_name=DOCUMENT_ONE_NAME)
    await helpers.click_button('Upload file')
    await asserts.url('/upload/statutory-declarations')
    await asserts.accessibility()
    await asserts.h1('Statutory declarations documents')
    await asserts.number_of_errors(0)
    await asserts.documents_uploaded(1)

    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Click "Submit and pay"
    await helpers.click_button('Submit and pay')

    # ------------------------------------------------
    # ---- Payment page
    # ------------------------------------------------
    await asserts.url('/submit-and-pay')
    await asserts.accessibility()
    await asserts.h1('Payment')
    await asserts.number_of_errors(0)

    # Choose "No, I will pay now" option, click Save and continue
    await helpers.check_radio(field='applying_for_help_with_fee', value='Online')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/submit-and-pay/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers before sending your application')
    await asserts.number_of_errors(0)

    # Check the values in the summary table
    await asserts.check_your_answers_rows(25)
    await asserts.check_your_answers_row(row_name='Have you ever been issued a Gender Recognition Certificate (or its equivalent) in another country?', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Do you have official documentation that shows you have ever been issued a Gender Recognition Certificate (or its equivalent) in one of the allowed countries or territories?', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Do you consent to the General Register Office contacting you about your application?', expected_value='Yes')

    await asserts.check_your_answers_row(row_name='Name (as you would like it to appear on your Gender Recognition Certificate)', expected_value=f"{data.TITLE} {data.FIRST_NAME} {data.LAST_NAME}")
    await asserts.check_your_answers_row(row_name='Affirmed gender', expected_value='Male')
    await asserts.check_your_answers_row(row_name='When you transitioned', expected_value='March 2000')
    await asserts.check_your_answers_row(row_name='When you signed your statutory declaration', expected_value=data.STATUTORY_DECLARATION_DATE_FORMATTED)
    await asserts.check_your_answers_row(row_name='Ever changed name', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Address', expected_value=f"{data.ADDRESS_LINE_ONE}\n{data.ADDRESS_LINE_TWO}\n{data.TOWN}\n{data.POSTCODE}")
    await asserts.check_your_answers_row(row_name='Contact preferences', expected_value=f"Email: {data.EMAIL_ADDRESS}\nPhone: {data.PHONE_NUMBER}\nPost: {data.ADDRESS_LINE_ONE}, {data.ADDRESS_LINE_TWO}, {data.TOWN}, {data.POSTCODE}")
    await asserts.check_your_answers_row(row_name='Unavailable over the next 6 months', expected_value=f"Yes\n{data.DATES_TO_AVOID}")
    await asserts.check_your_answers_row(row_name='Notify HMRC', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='National insurance number', expected_value=data.NATIONAL_INSURANCE_NUMBER)

    await asserts.check_your_answers_row(row_name='Birth name', expected_value=f"{data.BIRTH_FIRST_NAME} {data.BIRTH_MIDDLE_NAME} {data.BIRTH_LAST_NAME}")
    await asserts.check_your_answers_row(row_name='Date of birth', expected_value=data.DATE_OF_BIRTH_FORMATTED)
    await asserts.check_your_answers_row(row_name='Birth registered in UK', expected_value='No')
    await asserts.check_your_answers_row(row_name='Registered birth country', expected_value=data.BIRTH_COUNTRY)

    await asserts.check_your_answers_row(row_name='Currently married or in a civil partnership', expected_value='Neither')
    await asserts.check_your_answers_row(row_name='Spouse or partner has died', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Marriage or civil partnership has ended', expected_value='Yes')

    await asserts.check_your_answers_row(row_name='Name change documents', expected_value='document_1.bmp')
    await asserts.check_your_answers_row(row_name='Marriage documents', expected_value='document_1.bmp')
    await asserts.check_your_answers_row(row_name='Overseas certificate documents', expected_value='document_1.bmp')
    await asserts.check_your_answers_row(row_name='Statutory declarations', expected_value='document_1.bmp')

    await asserts.check_your_answers_row(row_name='Payment method', expected_value='Online')
