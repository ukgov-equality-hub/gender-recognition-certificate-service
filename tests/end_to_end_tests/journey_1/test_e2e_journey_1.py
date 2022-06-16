import os
import asyncio
from playwright.async_api import async_playwright
from tests.helpers.e2e_assert_helpers import AssertHelpers
from tests.helpers.e2e_page_helpers import PageHelpers
import tests.end_to_end_tests.journey_1.data as data
import tests.end_to_end_tests.journey_1.login_and_confirmation.section as section_login_and_confirmation
import tests.end_to_end_tests.journey_1.personal_details.section as section_personal_details
import tests.end_to_end_tests.journey_1.birth_registration.section as section_birth_registration
import tests.end_to_end_tests.journey_1.partnership_details.section as section_partnership_details
import tests.end_to_end_tests.journey_1.uploads.section as section_uploads
import tests.end_to_end_tests.journey_1.submit_and_pay.section as section_submit_and_pay


"""
To setup on docker container:
pip install playwright pytest-playwright asyncio
playwright install
apt-get install -y gstreamer1.0-libav libnss3-tools libatk-bridge2.0-0 libcups2-dev libxkbcommon-x11-0 libxcomposite-dev libxrandr2 libgbm-dev libgtk-3-0

To setup locally:
pip install playwright pytest-playwright asyncio
pip install -e .
playwright install --with-deps

To run test locally in debug mode:
PWDEBUG=1 pytest -s
"""

TEST_URL = os.getenv('TEST_URL', 'http://localhost:5000')
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

    # ------------------------------------------------
    # ---- PERSONAL DETAILS section
    # ------------------------------------------------
    await section_personal_details.run_checks_on_section(page, asserts, helpers)

    # ------------------------------------------------
    # ---- BIRTH REGISTRATION section
    # ------------------------------------------------
    await section_birth_registration.run_checks_on_section(page, asserts, helpers)

    # ------------------------------------------------
    # ---- PARTNERSHIP DETAILS section
    # ------------------------------------------------
    await section_partnership_details.run_checks_on_section(page, asserts, helpers)

    # ------------------------------------------------
    # ---- UPLOADS section
    # ------------------------------------------------
    await section_uploads.run_checks_on_section(page, asserts, helpers)

    # ------------------------------------------------
    # ---- SUBMIT AND PAY section
    # ------------------------------------------------
    await section_submit_and_pay.run_checks_on_section(page, asserts, helpers)

    # Tidy up
    await browser.close()
    asserts.run_final_accessibility_checks()


async def e2e_main():
    print("")  # Blank line to improve formatting
    async with async_playwright() as p:
        for browser_type in [p.chromium]: #, p.firefox, p.webkit]:
            await run_script_for_browser(browser_type)


def test_e2e_journey_1():
    asyncio.run(e2e_main())
