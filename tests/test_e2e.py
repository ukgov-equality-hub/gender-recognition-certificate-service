import os
import asyncio
from playwright.async_api import async_playwright

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

async def main():
    async with async_playwright() as p:
        for browser_type in [p.chromium]: #, p.firefox, p.webkit]:
            browser = await browser_type.launch()
            page = await browser.new_page()
            await page.goto(TEST_URL)
            assert await page.inner_text('a.govuk-header__link.govuk-header__link--service-name') == 'Apply for a Gender Recognition Certificate'

            await page.type('#email', 'alistair@nts-graphics.co.uk')
            await page.click('button.govuk-button')
            #await page.wait_for_timeout(3000)
            assert await page.inner_text('h1.govuk-heading-l') == 'Enter security code'

            # If we need to test...
            #page.on('console', lambda msg: print(msg.text))
            #await page.screenshot(path=f'example-{browser_type.name}.png')

            await page.type('#code', '11111')
            await page.click('button.govuk-button')
            assert await page.inner_text('h1.govuk-fieldset__heading') == 'Have you already started an application?'

            await browser.close()

asyncio.run(main())
