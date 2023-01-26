from playwright.async_api import Page
from tests.helpers.e2e_assert_helpers import AssertHelpers
from tests.helpers.e2e_page_helpers import PageHelpers
import tests.end_to_end_tests.journey_2.data as data


async def check_gov_uk_pay(page: Page, asserts: AssertHelpers, helpers: PageHelpers):
    # ------------------------------------------------
    # ---- Check Your Answers page
    # ------------------------------------------------
    await asserts.url('/submit-and-pay/check-your-answers')
    await asserts.accessibility()
    await asserts.h1('Check your answers before sending your application')
    await asserts.number_of_errors(0)

    # Check the checkbox, click Save and continue
    await helpers.check_checkbox(field='certify')
    page.set_default_timeout(data.TIMEOUT_FOR_SLOW_OPERATIONS)
    await helpers.click_button('Submit application and pay online')

    # ------------------------------------------------
    # ---- Gov.UK Pay - Card Details page
    # ------------------------------------------------
    await asserts.url_matches_regex('/card_details/[a-z0-9]*')
    print("FIRING PRE")
    page.set_default_timeout(data.DEFAULT_TIMEOUT)
    await asserts.h1('Enter card details')

    await helpers.fill_textbox(field='cardNo', value=data.TEST_CARD_NUMBER)
    await helpers.fill_textbox(field='expiryMonth', value=data.TEST_CARD_EXPIRY_MONTH)
    await helpers.fill_textbox(field='expiryYear', value=data.TEST_CARD_EXPIRY_YEAR)
    await helpers.fill_textbox(field='cardholderName', value=data.TEST_CARDHOLDER_NAME)
    await helpers.fill_textbox(field='cvc', value=data.TEST_CARD_CVC)
    await helpers.fill_textbox_byid(field='address-country', value=data.TEST_CARD_COUNTRY)
    await helpers.fill_textbox(field='addressLine1', value=data.TEST_CARD_ADDRESS_LINE_1)
    await helpers.fill_textbox(field='addressLine2', value=data.TEST_CARD_ADDRESS_LINE_2)
    await helpers.fill_textbox(field='addressCity', value=data.TEST_CARD_ADDRESS_CITY)
    await helpers.fill_textbox(field='addressPostcode', value=data.TEST_CARD_ADDRESS_POSTCODE)
    await helpers.fill_textbox(field='email', value=data.EMAIL_ADDRESS)
    print("FIIRING POST")
    # Click "Continue"
    await helpers.click_button('Continue')

    # ------------------------------------------------
    # ---- Gov.UK Pay - Confirm Your Payment page
    # ------------------------------------------------
    await asserts.url_matches_regex('/card_details/[a-z0-9]*/confirm')
    await asserts.h1('Confirm your payment')

    # Click "Confirm payment"
    await helpers.click_button('Confirm payment')

    # ------------------------------------------------
    # ---- Confirmation page
    # ------------------------------------------------
    await asserts.url('/submit-and-pay/confirmation')
    await asserts.accessibility()
    await asserts.h1('Application submitted')
    await asserts.number_of_errors(0)
