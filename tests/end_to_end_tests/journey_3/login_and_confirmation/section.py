from playwright.async_api import Page
from tests.helpers.e2e_assert_helpers import AssertHelpers
from tests.helpers.e2e_page_helpers import PageHelpers
import tests.end_to_end_tests.journey_3.data as data


async def run_checks_on_section(page: Page, asserts: AssertHelpers, helpers: PageHelpers):
    # ------------------------------------------------
    # ---- Homepage / Email address page
    # ------------------------------------------------
    await asserts.url('/')
    await asserts.accessibility()
    assert await page.inner_text('a.govuk-header__link.govuk-header__link--service-name') == 'Apply for a Gender Recognition Certificate'
    await asserts.h1('Email address')
    await asserts.a("applying for a Gender Recognition Certificate (opens in a new tab)")
    await asserts.number_of_errors(0)


