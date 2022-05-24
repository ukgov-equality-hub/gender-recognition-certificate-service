from playwright.async_api import Page
from tests.accessibility.accessibility_checks import AccessibilityChecks
from tests.helpers.e2e_page_helpers import PageHelpers, clean_string


class AssertHelpers:
    def __init__(self, page: Page, helpers: PageHelpers, base_url: str):
        self.page: Page = page
        self.helpers: PageHelpers = helpers
        self.base_url = base_url
        self.accessibility_checks = AccessibilityChecks()

    async def new_page(self, url: str, h1: str, errors: int):
        await self.url(expected_url=url)
        await self.accessibility()
        await self.h1(expected_h1_text=h1)
        await self.number_of_errors(expected_nuber_of_errors=errors)

    async def url(self, expected_url: str):
        await self.page.wait_for_load_state()
        actual_url = self.page.url[len(self.base_url):]
        assert_equal(actual_url, expected_url)

    async def error(self, field: str, message: str):
        error_summary_message = clean_string(await self.page.inner_text(f".govuk-error-summary__list a[href=\"#{field}\"]"))
        assert_equal(error_summary_message, message)

        field_error_message = clean_string(await self.page.inner_text(f"#{field}-error"))
        expected_field_error_message = f"Error: {message}"
        assert_equal(field_error_message, expected_field_error_message)

    async def number_of_errors(self, expected_nuber_of_errors: int):
        number_of_errors_in_error_summary = await self.page.locator('.govuk-error-summary__list li').count()
        assert_equal(number_of_errors_in_error_summary, expected_nuber_of_errors)

        number_of_error_messages_on_page = await self.page.locator('.govuk-error-message').count()
        assert_equal(number_of_error_messages_on_page, expected_nuber_of_errors)

        if expected_nuber_of_errors == 0:
            number_of_elements_with_error_class = await self.page.locator('*[class$="--error"]').count()
            assert_equal(number_of_elements_with_error_class, 0)

    async def h1(self, expected_h1_text: str):
        actual_h1_text = clean_string(await self.page.inner_text('h1'))
        assert_equal(actual_h1_text, expected_h1_text)

    async def fieldset_legend(self, expected_fieldset_legend_text: str):
        actual_fieldset_legend_text = clean_string(await self.page.inner_text('.govuk-fieldset__legend'))
        assert_equal(actual_fieldset_legend_text, expected_fieldset_legend_text)

    async def accessibility(self, page_description: str = None):
        await self.accessibility_checks.run_checks_on_page(self.page, page_description)

    def run_final_accessibility_checks(self):
        self.accessibility_checks.run_final_checks()

    async def task_list_sections(self, expected_number_of_sections: int):
        number_of_sections = await self.page.locator('.app-task-list__item').count()
        assert_equal(number_of_sections, expected_number_of_sections)

    async def task_list_section(self, section: str, expected_status: str):
        selector = f".app-task-list__item:has(.app-task-list__task-name:text-is(\"{section}\")) .app-task-list__tag, " \
                   f".app-task-list__item:has(.app-task-list__task-name a:text-is(\"{section}\")) .app-task-list__tag"
        status = await self.page.inner_text(selector)
        assert_equal(status, expected_status)

    async def field_value(self, field: str, expected_value: str):
        selector = f"input[name=\"{field}\"], textarea[name=\"{field}\"]"
        actual_value = await self.page.input_value(selector)
        assert_equal(actual_value, expected_value)

    async def is_checked(self, field: str, value: str):
        selector = f"input[type=\"radio\"][name=\"{field}\"][value=\"{value}\"], " \
                   f"input[type=\"checkbox\"][name=\"{field}\"][value=\"{value}\"]"
        element_is_checked = await self.page.is_checked(selector)
        assert_equal(element_is_checked, True)

    async def not_checked(self, field: str, value: str):
        selector = f"input[type=\"radio\"][name=\"{field}\"][value=\"{value}\"], " \
                   f"input[type=\"checkbox\"][name=\"{field}\"][value=\"{value}\"]"
        element_is_checked = await self.page.is_checked(selector)
        assert_equal(element_is_checked, False)

    async def check_your_answers_rows(self, expected_number_of_rows: int):
        actual_number_of_rows = await self.page.locator('.govuk-summary-list__row').count()
        assert_equal(actual_number_of_rows, expected_number_of_rows)

    async def check_your_answers_row(self, row_name: str, expected_value: str):
        selector = f".govuk-summary-list__row:has(.govuk-summary-list__key:text-is(\"{row_name}\")) .govuk-summary-list__value"
        status = await self.page.inner_text(selector)
        assert_equal(status, expected_value)

    async def check_your_answers_row_missing(self, row_name: str):
        selector = f".govuk-summary-list__key:text-is(\"{row_name}\")"
        number_of_matching_rows = await self.page.locator(selector).count()
        assert_equal(number_of_matching_rows, 0)

    async def change_links_to_url(self, link_text: str, expected_url: str):
        url_before = self.page.url
        await self.helpers.click_button(link_text)
        await self.url(expected_url)

        # TODO: Really, we should be clicking on the "Back" link,
        #  rather than going back in the browser's history
        #  But, "Back" doesn't currently always take the user to where they'd expect :-(
        # await self.helpers.click_button('Back')  # <-- What we'd like to use
        await self.page.go_back()  # <-- What we use instead

        await self.page.wait_for_load_state()
        url_after = self.page.url
        assert_equal(url_after, url_before)


# This method looks pointless, but helps give informative stack traces
# The parameter values are shown in the stack trace,
#   so it's really clear to see what the expected and actual values are
def assert_equal(actual_value, expected_value):
    if actual_value != expected_value:
        print(f"Actual value does not equal expected value\n"
              f"- actual value: ({actual_value})\n"
              f"- expected value: ({expected_value})", flush=True)
    assert actual_value == expected_value
