from playwright.async_api import Page
from tests.helpers.e2e_assert_helpers import AssertHelpers
from tests.helpers.e2e_page_helpers import PageHelpers
import tests.end_to_end_tests.journey_1.data as data


async def run_checks_on_section(page: Page, asserts: AssertHelpers, helpers: PageHelpers):
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
    await helpers.fill_textbox(field='email', value=data.EMAIL_ADDRESS)
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Security Code page
    # ------------------------------------------------
    await asserts.url('/security-code')
    await asserts.accessibility()
    await asserts.h1('Enter security code')
    await asserts.number_of_errors(0)

    # Don't enter a Security Code, click Continue button, see an error message
    await helpers.fill_textbox(field='security_code', value='')
    await helpers.click_button('Continue')
    await asserts.url('/security-code')
    await asserts.accessibility(page_description='No security code entered')
    await asserts.h1('Enter security code')
    await asserts.number_of_errors(1)
    await asserts.error(field='security_code', message='Enter a security code')

    # Enter an invalid Security Code, click Continue button, see an error message
    await helpers.fill_textbox(field='security_code', value='4444')  # Note: Don't use a 5-digit code, otherwise this test will break once every 10,000 runs!
    await helpers.click_button('Continue')
    await asserts.url('/security-code')
    await asserts.accessibility(page_description='Invalid security code entered')
    await asserts.h1('Enter security code')
    await asserts.number_of_errors(1)
    await asserts.error(field='security_code', message='Enter the security code that we emailed you')

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
    initial_reference_number_on_reference_number_page = await page.inner_text('#reference-number')

    # Clicking "Back" should take us to the Is First Visit page
    await helpers.click_button('Back')

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

    # Copy reference number so we can use it later
    reference_number_on_reference_number_page = await page.inner_text('#reference-number')

    # The reference number should be different to the one we saw earlier
    assert reference_number_on_reference_number_page != initial_reference_number_on_reference_number_page

    # CLick "Continue"
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

    # Click "save and exit"
    await helpers.click_button('save and exit')

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
    await helpers.fill_textbox(field='email', value=data.DIFFERENT_EMAIL_ADDRESS)
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
