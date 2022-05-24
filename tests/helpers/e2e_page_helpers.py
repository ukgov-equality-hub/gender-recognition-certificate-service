from playwright.async_api import Page


class PageHelpers:
    def __init__(self, page: Page):
        self.page: Page = page

    async def click_button(self, link_text):
        links_and_buttons = self.page.locator('a, button')
        number_of_links_and_buttons = await links_and_buttons.count()
        for n in range(number_of_links_and_buttons):
            link_or_button = links_and_buttons.nth(n)
            link_or_button_inner_text = await link_or_button.inner_text()
            normalised_inner_text = clean_string(link_or_button_inner_text)
            if normalised_inner_text == link_text:
                await link_or_button.click()
                return

    async def check_radio(self, field, value):
        await self.page.check(f"input[type=\"radio\"][name=\"{field}\"][value=\"{value}\"]")

    async def check_checkbox(self, field, value=None):
        if value:
            await self.page.check(f"input[type=\"checkbox\"][name=\"{field}\"][value=\"{value}\"]")
        else:
            await self.page.check(f"input[type=\"checkbox\"][name=\"{field}\"]")

    async def uncheck_checkbox(self, field, value=None):
        if value:
            await self.page.uncheck(f"input[type=\"checkbox\"][name=\"{field}\"][value=\"{value}\"]")
        else:
            await self.page.uncheck(f"input[type=\"checkbox\"][name=\"{field}\"]")

    async def fill_textbox(self, field, value):
        selector = f"input[type=\"text\"][name=\"{field}\"], input[type=\"tel\"][name=\"{field}\"], textarea[name=\"{field}\"]"
        await self.page.fill(selector, value)


# Removes multiple sequential whitespace characters from the string
def clean_string(value: str):
    return " ".join(value.split())