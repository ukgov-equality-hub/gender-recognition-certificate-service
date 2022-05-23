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