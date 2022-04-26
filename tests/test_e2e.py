import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            browser = await browser_type.launch()
            page = await browser.new_page()
            page.goto('http://localhost:8080')
            #await page.screenshot(path=f'example-{browser_type.name}.png')
            assert page.inner_text('a.govuk-header__link.govuk-header__link--service-name') == 'Apply for a Gender Recognition Certificate'

            await page.fill('#email', 'test@test.com')
            await page.click('button.govuk-button')
            assert page.inner_text('h1.govuk-heading-l') == 'Enter security code'

            await browser.close()

asyncio.run(main())
