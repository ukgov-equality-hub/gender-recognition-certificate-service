


def test_example_is_working(page):
    page.goto("http://localhost:8080")
    assert page.inner_text('a.govuk-header__link') == 'Apply for a Gender Recognition Certificate'
