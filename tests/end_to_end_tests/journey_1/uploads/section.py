from playwright.async_api import Page
from tests.helpers.e2e_assert_helpers import AssertHelpers
from tests.helpers.e2e_page_helpers import PageHelpers
import tests.end_to_end_tests.journey_1.data as data
import tests.end_to_end_tests.journey_1.uploads.page_name_change_documents as page_name_change_documents
import tests.end_to_end_tests.journey_1.uploads.page_marriage_documents as page_marriage_documents
import tests.end_to_end_tests.journey_1.uploads.page_overseas_documents as page_overseas_documents
import tests.end_to_end_tests.journey_1.uploads.page_statutory_declarations as page_statutory_declarations


async def run_checks_on_section(page: Page, asserts: AssertHelpers, helpers: PageHelpers):

    # ------------------------------------------------
    # ---- Name Change Documents page
    # ------------------------------------------------
    await page_name_change_documents.run_checks_on_page(page, asserts, helpers)

    # ------------------------------------------------
    # ---- Marriage Documents page
    # ------------------------------------------------
    await page_marriage_documents.run_checks_on_page(page, asserts, helpers)

    # ------------------------------------------------
    # ---- Overseas Documents page
    # ------------------------------------------------
    await page_overseas_documents.run_checks_on_page(page, asserts, helpers)

    # ------------------------------------------------
    # ---- Statutory Declarations page
    # ------------------------------------------------
    await page_statutory_declarations.run_checks_on_page(page, asserts, helpers)
