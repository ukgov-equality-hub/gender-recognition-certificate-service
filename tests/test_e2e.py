


def test_example_is_working(page):
    page.goto("http://localhost:5000")
    assert page.inner_text('a.govuk-header__link') == 'Apply for a Gender Recognition Certificate'
