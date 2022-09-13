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

    # Click "Submit and pay"
    await helpers.click_button('Submit and pay')

    # ------------------------------------------------
    # ---- Payment page
    # ------------------------------------------------
    await asserts.url('/submit-and-pay')
    await asserts.accessibility()
    await asserts.h1('Payment')
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

    # Click "Submit and pay" again
    await helpers.click_button('Submit and pay')

    # ------------------------------------------------
    # ---- Payment page
    # ------------------------------------------------
    await asserts.url('/submit-and-pay')
    await asserts.accessibility()
    await asserts.h1('Payment')
    await asserts.number_of_errors(0)

    # Don't choose any option, click Save and continue
    await helpers.click_button('Save and continue')
    await asserts.url('/submit-and-pay')
    await asserts.accessibility()
    await asserts.h1('Payment')
    await asserts.number_of_errors(1)
    await asserts.error(field='applying_for_help_with_fee', message='Select if you are applying for help paying the fee')

    # Choose "No, I will pay now" option, click Save and continue
    await helpers.check_radio(field='applying_for_help_with_fee', value='False')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/submit-and-pay/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers before sending your application')
    await asserts.number_of_errors(0)

    # "Back" link should take you to the Payment page
    # Click "Back"
    # Then choose the "Help" option and continue down that route
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Payment page
    # ------------------------------------------------
    await asserts.url('/submit-and-pay')
    await asserts.accessibility()
    await asserts.h1('Payment')
    await asserts.number_of_errors(0)

    # The fields should be pre-populated with the values we just entered
    await asserts.is_checked(field='applying_for_help_with_fee', value='False')
    await asserts.not_checked(field='applying_for_help_with_fee', value='True')

    # Choose the "Help" option and continue down that route
    await helpers.check_radio(field='applying_for_help_with_fee', value='True')
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Applying For Help page
    # ------------------------------------------------
    await asserts.url('/submit-and-pay/help-type')
    await asserts.accessibility()
    await asserts.h1('Applying for help with the fee')
    await asserts.number_of_errors(0)

    # "Back" link should take you to the Payment page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Payment page
    # ------------------------------------------------
    await asserts.url('/submit-and-pay')
    await asserts.accessibility()
    await asserts.h1('Payment')
    await asserts.number_of_errors(0)

    # The fields should be pre-populated with the values we just entered
    await asserts.is_checked(field='applying_for_help_with_fee', value='True')
    await asserts.not_checked(field='applying_for_help_with_fee', value='False')

    # Continue to the "Applying For Help" page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Applying For Help page
    # ------------------------------------------------
    await asserts.url('/submit-and-pay/help-type')
    await asserts.accessibility()
    await asserts.h1('Applying for help with the fee')
    await asserts.number_of_errors(0)

    # Don't choose any option, click Save and continue
    await helpers.click_button('Save and continue')
    await asserts.url('/submit-and-pay/help-type')
    await asserts.accessibility()
    await asserts.h1('Applying for help with the fee')
    await asserts.number_of_errors(1)
    await asserts.error(field='how_applying_for_fees', message='Select how are you applying for help paying the fee')

    # Choose "Using the online service" option, but don't enter a Help with Fees reference number
    await helpers.check_radio(field='how_applying_for_fees', value='USING_ONLINE_SERVICE')
    await helpers.click_button('Save and continue')
    await asserts.url('/submit-and-pay/help-type')
    await asserts.accessibility()
    await asserts.h1('Applying for help with the fee')
    await asserts.number_of_errors(1)
    await asserts.error(field='help_with_fees_reference_number', message='Enter your Help with Fees reference number')

    # Enter a valid Help with Fees reference number
    await helpers.check_radio(field='how_applying_for_fees', value='USING_ONLINE_SERVICE')
    await helpers.fill_textbox(field='help_with_fees_reference_number', value=data.HELP_WITH_FEES_REFERENCE_NUMBER)
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/submit-and-pay/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers before sending your application')
    await asserts.number_of_errors(0)

    # "Back" link should take you to the Applying For Help page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Applying For Help page
    # ------------------------------------------------
    await asserts.url('/submit-and-pay/help-type')
    await asserts.accessibility()
    await asserts.h1('Applying for help with the fee')
    await asserts.number_of_errors(0)

    # The fields should be pre-populated with the values we just entered
    await asserts.is_checked(field='how_applying_for_fees', value='USING_ONLINE_SERVICE')
    await asserts.not_checked(field='how_applying_for_fees', value='USING_EX160_FORM')
    await asserts.field_value(field='help_with_fees_reference_number', expected_value=data.HELP_WITH_FEES_REFERENCE_NUMBER)

    # Continue to the Check Your Answers page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/submit-and-pay/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers before sending your application')
    await asserts.number_of_errors(0)

    # Check the values in the summary table
    await asserts.check_your_answers_rows(35)
    await asserts.check_your_answers_row(row_name='Have you ever been issued a Gender Recognition Certificate (or its equivalent) in another country?', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Do you have official documentation that shows you have ever been issued a Gender Recognition Certificate (or its equivalent) in one of the allowed countries or territories?', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Do you consent to the General Register Office contacting you about your application?', expected_value='Yes')

    await asserts.check_your_answers_row(row_name='Name (as you would like it to appear on your Gender Recognition Certificate)', expected_value=f"{data.TITLE} {data.FIRST_NAME} {data.MIDDLE_NAMES} {data.LAST_NAME}")
    await asserts.check_your_answers_row(row_name='Affirmed gender', expected_value='Male')
    await asserts.check_your_answers_row(row_name='When you transitioned', expected_value='March 2000')
    await asserts.check_your_answers_row(row_name='When you signed your statutory declaration', expected_value=data.STATUTORY_DECLARATION_DATE_FORMATTED)
    await asserts.check_your_answers_row(row_name='Ever changed name', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Address', expected_value=f"{data.ADDRESS_LINE_ONE}\n{data.ADDRESS_LINE_TWO}\n{data.TOWN}\n{data.POSTCODE}")
    await asserts.check_your_answers_row(row_name='Contact preferences', expected_value=f"Email: {data.EMAIL_ADDRESS}\nPhone: {data.PHONE_NUMBER}\nPost: {data.ADDRESS_LINE_ONE}, {data.ADDRESS_LINE_TWO}, {data.TOWN}, {data.POSTCODE}")
    await asserts.check_your_answers_row(row_name='Unavailable over the next 6 months', expected_value=f"Yes\n{data.DATES_TO_AVOID}")
    await asserts.check_your_answers_row(row_name='Notify HMRC', expected_value='No')

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

    await asserts.check_your_answers_row(row_name='Currently married or in a civil partnership', expected_value='Civil partnership')
    await asserts.check_your_answers_row(row_name='Remain in your civil partnership', expected_value='Yes')
    await asserts.check_your_answers_row(row_name='Can provide a declaration of consent from your civil partner', expected_value='Yes')
    await asserts.check_your_answers_row(row_name="Civil partner's first name", expected_value=data.PARTNER_FIRST_NAME)
    await asserts.check_your_answers_row(row_name="Civil partner's last name", expected_value=data.PARTNER_LAST_NAME)
    await asserts.check_your_answers_row(row_name="Civil partner's postal address", expected_value=data.PARTNER_POSTAL_ADDRESS)

    await asserts.check_your_answers_row(row_name='Name change documents', expected_value='document_1.bmp')
    await asserts.check_your_answers_row(row_name='Marriage documents', expected_value='document_1.bmp')
    await asserts.check_your_answers_row(row_name='Overseas certificate documents', expected_value='document_1.bmp')
    await asserts.check_your_answers_row(row_name='Statutory declarations', expected_value='document_1.bmp')

    await asserts.check_your_answers_row(row_name='Payment method', expected_value='Help')
    await asserts.check_your_answers_row(row_name='Help type', expected_value='Using the online service')
    await asserts.check_your_answers_row(row_name='Help with Fees reference number', expected_value=data.HELP_WITH_FEES_REFERENCE_NUMBER)

    # Click each "Change" link to check it takes us to the correct page
    await asserts.change_links_to_url(link_text='Change if you have ever been issued a Gender Recognition Certificate (or its equivalent) in another country', expected_url='/overseas-check', save_and_continue_button_text='Continue')
    await asserts.change_links_to_url(link_text='Change if you have official documentation that shows you have ever been issued a Gender Recognition Certificate (or its equivalent) in one of the allowed countries or territories', expected_url='/overseas-approved-check', save_and_continue_button_text='Continue')
    await asserts.change_links_to_url(link_text='Change if you consent to the General Register Office contacting you about your application', expected_url='/declaration', save_and_continue_button_text='Continue')

    await asserts.change_links_to_url(link_text='Change name (as you would like it to appear on your Gender Recognition Certificate)', expected_url='/personal-details')
    await asserts.change_links_to_url(link_text='Change affirmed gender', expected_url='/personal-details/affirmed-gender')
    await asserts.change_links_to_url(link_text='Change when you transitioned', expected_url='/personal-details/transition-date')
    await asserts.change_links_to_url(link_text='Change when you signed your statutory declaration', expected_url='/personal-details/statutory-declaration-date')
    await asserts.change_links_to_url(link_text='Change whether you have changed your name to reflect your gender', expected_url='/personal-details/previous-names-check')
    await asserts.change_links_to_url(link_text='Change address', expected_url='/personal-details/address')
    await asserts.change_links_to_url(link_text='Change contact preferences', expected_url='/personal-details/contact-preferences')
    await asserts.change_links_to_url(link_text="Change whether there are any dates you don't want us to contact you by post over the next 6 months", expected_url='/personal-details/contact-dates')
    await asserts.change_links_to_url(link_text='Change whether you want us to notify HMRC after you receive a Gender Recognition Certificate', expected_url='/personal-details/hmrc')

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

    await asserts.change_links_to_url(link_text='Change if you are currently married or in a civil partnership', expected_url='/partnership-details')
    await asserts.change_links_to_url(link_text='Change if you plan to remain in your civil partnership after receiving your Gender Recognition Certificate', expected_url='/partnership-details/stay-together')
    await asserts.change_links_to_url(link_text='Change if you can provide a declaration of consent from your civil partner', expected_url='/partnership-details/partner-agrees')
    await asserts.change_links_to_url(link_text="Change your civil partner's first name", expected_url='/partnership-details/partner-details')
    await asserts.change_links_to_url(link_text="Change your civil partner's last name", expected_url='/partnership-details/partner-details')
    await asserts.change_links_to_url(link_text="Change your civil partner's postal address", expected_url='/partnership-details/partner-details')

    await asserts.change_links_to_url(link_text='Change the documents you have uploaded as evidence of changing your name', expected_url='/upload/name-change', back_link_should_return_to_check_page=False, save_button_should_return_to_check_page=False)
    await asserts.change_links_to_url(link_text='Change the documents you have uploaded as evidence of your marriage or civil partnership', expected_url='/upload/marriage-documents', back_link_should_return_to_check_page=False, save_button_should_return_to_check_page=False)
    await asserts.change_links_to_url(link_text='Change the documents you have uploaded as evidence of your overseas certificate', expected_url='/upload/overseas-certificate', back_link_should_return_to_check_page=False, save_button_should_return_to_check_page=False)
    await asserts.change_links_to_url(link_text='Change the statutory declarations documents you have uploaded', expected_url='/upload/statutory-declarations', back_link_should_return_to_check_page=False, save_button_should_return_to_check_page=False)

    await asserts.change_links_to_url(link_text='Change payment method', expected_url='/submit-and-pay')
    await asserts.change_links_to_url(link_text='Change the way your are applying for help with paying the fees', expected_url='/submit-and-pay/help-type')
    await asserts.change_links_to_url(link_text='Change your Help with Fees reference number', expected_url='/submit-and-pay/help-type')


    # Don't choose any option, click Save and continue
    await helpers.click_button('Submit application')
    await page.wait_for_timeout(2000)
    await asserts.url('/submit-and-pay/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers before sending your application')
    await asserts.number_of_errors(1)
    await asserts.error(field='certify', message='You must certify that all information given in this application is correct and that you understand making a false application is an offence.')

    # Check the checkbox, click Save and continue
    await helpers.check_checkbox(field='certify')
    await helpers.click_button('Submit application')

    # ------------------------------------------------
    # ---- Confirmation page
    # ------------------------------------------------
    await asserts.url('/submit-and-pay/confirmation')
    await asserts.accessibility()
    await asserts.h1('Application submitted')
    await asserts.number_of_errors(0)
