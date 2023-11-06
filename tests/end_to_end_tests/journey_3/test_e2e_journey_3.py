import os
import asyncio
from playwright.async_api import async_playwright
from tests.helpers.e2e_assert_helpers import AssertHelpers
from tests.helpers.e2e_page_helpers import PageHelpers
import tests.end_to_end_tests.journey_3.data as data
import tests.end_to_end_tests.journey_3.login_and_confirmation.section as section_login_and_confirmation

# TEST_URL = os.getenv('TEST_URL', 'http://localhost:5000')
TEST_URL = 'http://localhost:3000'
print('Running tests on %s' % TEST_URL)


async def run_script_for_browser(browser_type):
    browser = await browser_type.launch()
    page = await browser.new_page()
    page.set_default_timeout(data.DEFAULT_TIMEOUT)

    helpers = PageHelpers(page)
    asserts = AssertHelpers(page, helpers, TEST_URL)

    # Open homepage ("Email address")
    await page.goto(TEST_URL)

    # ------------------------------------------------
    # ---- LOGIN / CONFIRMATION section
    # ------------------------------------------------
    await section_login_and_confirmation.run_checks_on_section(page, asserts, helpers)


async def e2e_main():
    print("")  # Blank line to improve formatting
    async with async_playwright() as p:
        for browser_type in [p.chromium]:  # , p.firefox, p.webkit]:
            await run_script_for_browser(browser_type)


def test_e2e_journey_1():
    asyncio.run(e2e_main())
