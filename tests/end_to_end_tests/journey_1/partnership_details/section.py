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
    await helpers.check_radio(field='currently_married', value='NEITHER')
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
    await asserts.is_checked(field='currently_married', value='NEITHER')
    await asserts.not_checked(field='currently_married', value='MARRIED')
    await asserts.not_checked(field='currently_married', value='CIVIL_PARTNERSHIP')

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
    await helpers.check_radio(field='partner_died', value='True')
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
    await asserts.is_checked(field='partner_died', value='True')
    await asserts.not_checked(field='partner_died', value='False')

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
    await helpers.check_radio(field='previous_partnership_ended', value='True')
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
    await asserts.is_checked(field='previous_partnership_ended', value='True')
    await asserts.not_checked(field='previous_partnership_ended', value='False')

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
    await helpers.check_radio(field='currently_married', value='MARRIED')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Stay Together page
    # ------------------------------------------------
    await asserts.url('/partnership-details/stay-together')
    await asserts.accessibility()
    await asserts.h1('Do you plan to remain married after you receive your Gender Recognition Certificate?')
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
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
    await asserts.is_checked(field='currently_married', value='MARRIED')
    await asserts.not_checked(field='currently_married', value='CIVIL_PARTNERSHIP')
    await asserts.not_checked(field='currently_married', value='NEITHER')

    # Continue to the Stay Together page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Stay Together page
    # ------------------------------------------------
    await asserts.url('/partnership-details/stay-together')
    await asserts.accessibility()
    await asserts.h1('Do you plan to remain married after you receive your Gender Recognition Certificate?')
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
    await asserts.number_of_errors(0)

    # Don't select an option, click "Save and continue"
    await helpers.click_button('Save and continue')
    await asserts.url('/partnership-details/stay-together')
    await asserts.accessibility()
    await asserts.h1('Do you plan to remain married after you receive your Gender Recognition Certificate?')
    await asserts.number_of_errors(1)
    await asserts.error(field='stay_together', message='Select if you plan to remain married or in your civil partnership after receiving your Gender Recognition Certificate')

    # Select the "No" option, go down that route
    # Then backtrack and choose "Yes
    await helpers.check_radio(field='stay_together', value='False')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Stay Together page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Stay Together page
    # ------------------------------------------------
    await asserts.url('/partnership-details/stay-together')
    await asserts.accessibility()
    await asserts.h1('Do you plan to remain married after you receive your Gender Recognition Certificate?')
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='stay_together', value='False')
    await asserts.not_checked(field='stay_together', value='True')

    # Continue to the Interim GRC page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
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
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
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
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
    await asserts.number_of_errors(0)

    # Click "Back" to get back to the "Stay Together" page, then choose "Yes"
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Stay Together page
    # ------------------------------------------------
    await asserts.url('/partnership-details/stay-together')
    await asserts.accessibility()
    await asserts.h1('Do you plan to remain married after you receive your Gender Recognition Certificate?')
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
    await asserts.number_of_errors(0)

    # Now choose the "Yes" option
    await helpers.check_radio(field='stay_together', value='True')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Partner Agrees page
    # ------------------------------------------------
    await asserts.url('/partnership-details/partner-agrees')
    await asserts.accessibility()
    await asserts.h1('Declaration of consent')
    await asserts.fieldset_legend('Can you provide a statutory declaration from your spouse?')
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Stay Together page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Stay Together page
    # ------------------------------------------------
    await asserts.url('/partnership-details/stay-together')
    await asserts.accessibility()
    await asserts.h1('Do you plan to remain married after you receive your Gender Recognition Certificate?')
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='stay_together', value='True')
    await asserts.not_checked(field='stay_together', value='False')

    # Continue to the Partner Agrees page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Partner Agrees page
    # ------------------------------------------------
    await asserts.url('/partnership-details/partner-agrees')
    await asserts.accessibility()
    await asserts.h1('Declaration of consent')
    await asserts.fieldset_legend('Can you provide a statutory declaration from your spouse?')
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
    await asserts.number_of_errors(0)

    # Don't select an option, click "Save and continue"
    await helpers.click_button('Save and continue')
    await asserts.url('/partnership-details/partner-agrees')
    await asserts.accessibility()
    await asserts.h1('Declaration of consent')
    await asserts.fieldset_legend('Can you provide a statutory declaration from your spouse?')
    await asserts.number_of_errors(1)
    await asserts.error(field='partner_agrees', message='Select if you can provide a declaration of consent from your spouse or civil partner')

    # Select the "No" option, go down that route
    # Then backtrack and choose "Yes
    await helpers.check_radio(field='partner_agrees', value='False')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
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
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='partner_agrees', value='False')
    await asserts.not_checked(field='partner_agrees', value='True')

    # Continue to the Interim GRC page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
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
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
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
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
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
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
    await asserts.number_of_errors(0)

    # This time, select the "Yes" option
    await helpers.check_radio(field='partner_agrees', value='True')
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
    await asserts.page_does_not_contain_text('civil partner', 'civil partnership')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='partner_agrees', value='True')
    await asserts.not_checked(field='partner_agrees', value='False')

    # Continue to the Marriage details: Check Your Answers page
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
    await asserts.check_your_answers_row(row_name='Currently married or in a civil partnership', expected_value='Married')
    await asserts.check_your_answers_row(row_name='Remain married', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Can provide a declaration of consent from your spouse', expected_value='Yes')

    # Click each "Change" link to check it takes us to the correct page
    await asserts.change_links_to_url(link_text='Change if you are currently married or in a civil partnership', expected_url='/partnership-details')
    await asserts.change_links_to_url(link_text='Change if you plan to remain married after receiving your Gender Recognition Certificate', expected_url='/partnership-details/stay-together')
    await asserts.change_links_to_url(link_text='Change if you can provide a declaration of consent from your spouse', expected_url='/partnership-details/partner-agrees')

    # REWIND!
    # Go all the way back to the "Are you married" page,
    # Select the "Civil partnership" option
    # Go through all the same journeys, checking the text has changed from "married" to "in a civil partnership"
    await helpers.click_button('Back')
    await asserts.url('/partnership-details/partner-agrees')

    # REWIND!
    # Go all the way back to the "Are you married" page,
    # Select the "Civil partnership" option
    # Go through all the same journeys, checking the text has changed from "married" to "in a civil partnership"
    await helpers.click_button('Back')
    await asserts.url('/partnership-details/stay-together')

    # REWIND!
    # Go all the way back to the "Are you married" page,
    # Select the "Civil partnership" option
    # Go through all the same journeys, checking the text has changed from "married" to "in a civil partnership"
    await helpers.click_button('Back')
    await asserts.url('/partnership-details')

    # ------------------------------------------------
    # ---- Are You Married page
    # ------------------------------------------------
    await asserts.url('/partnership-details')
    await asserts.accessibility()
    await asserts.h1('Marriages and civil partnerships')
    await asserts.number_of_errors(0)

    # Select the "Civil partnership" option
    # Go through all the same journeys, checking the text has changed from "married" to "in a civil partnership"
    await helpers.check_radio(field='currently_married', value='CIVIL_PARTNERSHIP')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Stay Together page
    # ------------------------------------------------
    await asserts.url('/partnership-details/stay-together')
    await asserts.accessibility()
    await asserts.h1('Do you plan to remain in your civil partnership after you receive your Gender Recognition Certificate?')
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
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
    await asserts.is_checked(field='currently_married', value='CIVIL_PARTNERSHIP')
    await asserts.not_checked(field='currently_married', value='MARRIED')
    await asserts.not_checked(field='currently_married', value='NEITHER')

    # Continue to the Stay Together page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Stay Together page
    # ------------------------------------------------
    await asserts.url('/partnership-details/stay-together')
    await asserts.accessibility()
    await asserts.h1('Do you plan to remain in your civil partnership after you receive your Gender Recognition Certificate?')
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
    await asserts.number_of_errors(0)

    # Select the "No" option, go down that route
    # Then backtrack and choose "Yes
    await helpers.check_radio(field='stay_together', value='False')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Stay Together page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Stay Together page
    # ------------------------------------------------
    await asserts.url('/partnership-details/stay-together')
    await asserts.accessibility()
    await asserts.h1('Do you plan to remain in your civil partnership after you receive your Gender Recognition Certificate?')
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='stay_together', value='False')
    await asserts.not_checked(field='stay_together', value='True')

    # Continue to the Interim GRC page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
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
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
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
    await asserts.check_your_answers_row(row_name='Currently married or in a civil partnership', expected_value='Civil partnership')
    await asserts.check_your_answers_row(row_name='Remain in your civil partnership', expected_value='No')
    await asserts.check_your_answers_row(row_name='Interim GRC', expected_value='Yes')

    # Click each "Change" link to check it takes us to the correct page
    await asserts.change_links_to_url(link_text='Change if you are currently married or in a civil partnership', expected_url='/partnership-details')
    await asserts.change_links_to_url(link_text='Change if you plan to remain in your civil partnership after receiving your Gender Recognition Certificate', expected_url='/partnership-details/stay-together')
    await asserts.change_links_to_url(link_text='Change if you understand that you will receive an Interim GRC', expected_url='/partnership-details/interim-check')

    # Click "Back" to get back to the "Stay Together" page, then choose "Yes"
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
    await asserts.number_of_errors(0)

    # Click "Back" to get back to the "Stay Together" page, then choose "Yes"
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Stay Together page
    # ------------------------------------------------
    await asserts.url('/partnership-details/stay-together')
    await asserts.accessibility()
    await asserts.h1('Do you plan to remain in your civil partnership after you receive your Gender Recognition Certificate?')
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
    await asserts.number_of_errors(0)

    # Now choose the "Yes" option
    await helpers.check_radio(field='stay_together', value='True')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Partner Agrees page
    # ------------------------------------------------
    await asserts.url('/partnership-details/partner-agrees')
    await asserts.accessibility()
    await asserts.h1('Declaration of consent')
    await asserts.fieldset_legend('Can you provide a statutory declaration from your civil partner?')
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Stay Together page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Stay Together page
    # ------------------------------------------------
    await asserts.url('/partnership-details/stay-together')
    await asserts.accessibility()
    await asserts.h1('Do you plan to remain in your civil partnership after you receive your Gender Recognition Certificate?')
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='stay_together', value='True')
    await asserts.not_checked(field='stay_together', value='False')

    # Continue to the Partner Agrees page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Partner Agrees page
    # ------------------------------------------------
    await asserts.url('/partnership-details/partner-agrees')
    await asserts.accessibility()
    await asserts.h1('Declaration of consent')
    await asserts.fieldset_legend('Can you provide a statutory declaration from your civil partner?')
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
    await asserts.number_of_errors(0)

    # Select the "No" option, go down that route
    # Then backtrack and choose "Yes
    await helpers.check_radio(field='partner_agrees', value='False')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
    await asserts.number_of_errors(0)

    # Clicking "Back" should take us back to the Partner Agrees page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Partner Agrees page
    # ------------------------------------------------
    await asserts.url('/partnership-details/partner-agrees')
    await asserts.accessibility()
    await asserts.h1('Declaration of consent')
    await asserts.fieldset_legend('Can you provide a statutory declaration from your civil partner?')
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='partner_agrees', value='False')
    await asserts.not_checked(field='partner_agrees', value='True')

    # Continue to the Interim GRC page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
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
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
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
    await asserts.check_your_answers_row(row_name='Currently married or in a civil partnership', expected_value='Civil partnership')
    await asserts.check_your_answers_row(row_name='Remain in your civil partnership', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Can provide a declaration of consent from your civil partner', expected_value='No')
    await asserts.check_your_answers_row(row_name='Interim GRC', expected_value='Yes')

    # Click each "Change" link to check it takes us to the correct page
    await asserts.change_links_to_url(link_text='Change if you are currently married or in a civil partnership', expected_url='/partnership-details')
    await asserts.change_links_to_url(link_text='Change if you plan to remain in your civil partnership after receiving your Gender Recognition Certificate', expected_url='/partnership-details/stay-together')
    await asserts.change_links_to_url(link_text='Change if you can provide a declaration of consent from your civil partner', expected_url='/partnership-details/partner-agrees')
    await asserts.change_links_to_url(link_text='Change if you understand that you will receive an Interim GRC', expected_url='/partnership-details/interim-check')

    # Click "Back" to get back to the "Partner Agrees" page, then choose "Yes"
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Interim GRC page
    # ------------------------------------------------
    await asserts.url('/partnership-details/interim-check')
    await asserts.accessibility()
    await asserts.h1('Interim Gender Recognition Certificate')
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
    await asserts.number_of_errors(0)

    # Click "Back" to get back to the "Partner Agrees" page, then choose "Yes"
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Partner Agrees page
    # ------------------------------------------------
    await asserts.url('/partnership-details/partner-agrees')
    await asserts.accessibility()
    await asserts.h1('Declaration of consent')
    await asserts.fieldset_legend('Can you provide a statutory declaration from your civil partner?')
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
    await asserts.number_of_errors(0)

    # This time, select the "Yes" option
    await helpers.check_radio(field='partner_agrees', value='True')
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
    await asserts.fieldset_legend('Can you provide a statutory declaration from your civil partner?')
    await asserts.page_does_not_contain_text('marriage', 'married', 'spouce')
    await asserts.number_of_errors(0)

    # Check the values we entered have been remembered
    await asserts.is_checked(field='partner_agrees', value='True')
    await asserts.not_checked(field='partner_agrees', value='False')

    # Continue to the Marriage details: Check Your Answers page
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
    await asserts.check_your_answers_row(row_name='Currently married or in a civil partnership', expected_value='Civil partnership')
    await asserts.check_your_answers_row(row_name='Remain in your civil partnership', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Can provide a declaration of consent from your civil partner', expected_value='Yes')

    # Click each "Change" link to check it takes us to the correct page
    await asserts.change_links_to_url(link_text='Change if you are currently married or in a civil partnership', expected_url='/partnership-details')
    await asserts.change_links_to_url(link_text='Change if you plan to remain in your civil partnership after receiving your Gender Recognition Certificate', expected_url='/partnership-details/stay-together')
    await asserts.change_links_to_url(link_text='Change if you can provide a declaration of consent from your civil partner', expected_url='/partnership-details/partner-agrees')


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
    # The "Marriage documents" section should now be visible
    await asserts.task_list_sections(9)
    await asserts.task_list_section(section='Confirmation', expected_status='COMPLETED')
    await asserts.task_list_section(section='Your personal details', expected_status='COMPLETED')
    await asserts.task_list_section(section='Your birth registration information', expected_status='COMPLETED')
    await asserts.task_list_section(section='Marriage or civil partnership details', expected_status='COMPLETED')
    await asserts.task_list_section(section='Name change documents', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Marriage and civil partnership documents', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Overseas certificate documents', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Statutory declarations', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Submit and pay', expected_status='CANNOT START YET')
