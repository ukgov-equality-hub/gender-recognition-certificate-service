import os
import asyncio
from playwright.async_api import async_playwright
from tests.helpers.e2e_assert_helpers import AssertHelpers
from tests.helpers.e2e_page_helpers import PageHelpers
import tests.end_to_end_tests.journey_2.data as data
import tests.end_to_end_tests.journey_2.section_fill_in_application as section_fill_in_application
import tests.end_to_end_tests.journey_2.section_gov_uk_pay as section_gov_uk_pay


TEST_URL = os.getenv('TEST_URL', 'http://localhost:5000')


# ########################################
#
#   WHAT IS THIS TEST FOR?
#
#   The main purpose of this test is to
#   test the connection to Gov.UK Pay
#
# ########################################



async def run_script_for_browser(browser_type):
    browser = await browser_type.launch()
    page = await browser.new_page()
    page.set_default_timeout(data.DEFAULT_TIMEOUT)

    helpers = PageHelpers(page)
    asserts = AssertHelpers(page, helpers, TEST_URL)

    # Open homepage ("Email address")
    await page.goto(TEST_URL)

    # ------------------------------------------------
    # ---- Fill in application
    # ------------------------------------------------
    await section_fill_in_application.fill_in_application(page, asserts, helpers)

    # ------------------------------------------------
    # ---- Test Gov.Uk Pay pages
    # ------------------------------------------------
    await section_gov_uk_pay.check_gov_uk_pay(page, asserts, helpers)

    # Tidy up
    await browser.close()
    asserts.run_final_accessibility_checks()


async def e2e_main():
    print("")  # Blank line to improve formatting
    async with async_playwright() as p:
        for browser_type in [p.chromium]: #, p.firefox, p.webkit]:
            await run_script_for_browser(browser_type)


def test_e2e():
    asyncio.run(e2e_main())
