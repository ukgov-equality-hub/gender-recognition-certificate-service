from datetime import date
from dateutil.relativedelta import relativedelta
from grc import create_app
from grc.config import TestConfig
from grc.utils.form_custom_validators import validate_date_range_form, validate_date_ranges
from grc.personal_details.forms import ContactDatesForm, DateRangeForm
from grc.business_logic.data_structures.personal_details_data import ContactDatesAvoid
from tests.helpers.personal_details.helpers import remove_date_ranges, single_date_mock, date_range_mock


def create_test_app():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app(TestConfig)
    flask_app.config['WTF_CSRF_ENABLED'] = False
    return flask_app


def test_contact_single_date():
    flask_app = create_test_app()

    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        contact_dates_form = ContactDatesForm()
        contact_dates_form.contactDatesCheck.data = ContactDatesAvoid.SINGLE_DATE.value

        # Single date valid
        valid_date = date.today() + relativedelta(days=7)
        single_date_mock(contact_dates_form, valid_date)
        assert contact_dates_form.validate()

        # Single date invalid in the past
        invalid_date = date.today() - relativedelta(days=7)
        single_date_mock(contact_dates_form, invalid_date)
        assert not contact_dates_form.validate()
        assert contact_dates_form.errors['year'][0] == 'Enter a date in the future'

        # Single date missing input
        invalid_date = date.today() + relativedelta(days=7)
        single_date_mock(contact_dates_form, invalid_date, **{'year': ''})
        assert not contact_dates_form.validate()
        assert contact_dates_form.errors['year'][0] == 'Enter a year'

        # Single date invalid input
        invalid_date = date.today() + relativedelta(days=7)
        single_date_mock(contact_dates_form, invalid_date, **{'month': '14'})
        assert not contact_dates_form.validate()
        assert contact_dates_form.errors['month'][0] == 'Enter a month as a number between 1 and 12'


def test_contact_single_date_range():
    flask_app = create_test_app()

    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        contact_dates_form = ContactDatesForm()
        contact_dates_form.contactDatesCheck.data = ContactDatesAvoid.DATE_RANGE.value

        # SINGLE DATE RANGE VALID
        date_range_form = DateRangeForm()
        valid_from_date = date.today() + relativedelta(days=7)
        valid_to_date = valid_from_date + relativedelta(days=7)
        date_range_mock(date_range_form, valid_from_date, valid_to_date)
        contact_dates_form.date_ranges.append_entry(date_range_form)
        assert contact_dates_form.validate()
        assert validate_date_range_form(date_range_form) == {}
        remove_date_ranges(contact_dates_form)

        # SINGLE DATE RANGE INVALID INPUTS
        invalid_from_date = date.today() + relativedelta(days=7)
        invalid_to_date = valid_from_date + relativedelta(days=7)
        erroneous_fields = {
            'from_day': '',
            'to_year': '100'
        }
        date_range_mock(date_range_form, invalid_from_date, invalid_to_date, **erroneous_fields)
        contact_dates_form.date_ranges.append_entry(date_range_form)

        # wtf validation is not used on date ranges. It is conducted in the controller so validate() will return True
        assert contact_dates_form.validate()
        form_errors = validate_date_range_form(date_range_form)

        assert form_errors == {
            'from_date_day': 'Enter a day',
            'to_date_year': 'Enter a year as a 4-digit number, like 2000'
        }
        remove_date_ranges(contact_dates_form)

        # SINGLE DATE RANGE INVALID FROM DATE IN PAST
        date_range_form = DateRangeForm()
        invalid_from_date = date.today() - relativedelta(days=7)
        valid_to_date = valid_from_date + relativedelta(days=14)
        date_range_mock(date_range_form, invalid_from_date, valid_to_date)
        contact_dates_form.date_ranges.append_entry(date_range_form)

        # wtf validation is not used on date ranges. It is conducted in the controller so validate() will return True
        assert contact_dates_form.validate()
        form_errors = validate_date_range_form(date_range_form)
        assert form_errors == {}
        form_errors = validate_date_ranges(invalid_from_date, valid_to_date)
        assert form_errors == {
            'from_date_year': '\'From\' date is in the past'
        }
        remove_date_ranges(contact_dates_form)

        # SINGLE DATE RANGE INVALID TO DATE BEFORE FROM DATE
        date_range_form = DateRangeForm()
        valid_from_date = date.today() + relativedelta(days=14)
        invalid_to_date = valid_from_date - relativedelta(days=7)
        date_range_mock(date_range_form, valid_from_date, invalid_to_date)
        contact_dates_form.date_ranges.append_entry(date_range_form)

        # wtf validation is not used on date ranges. It is conducted in the controller so validate() will return True
        assert contact_dates_form.validate()
        form_errors = validate_date_range_form(date_range_form)
        assert form_errors == {}
        form_errors = validate_date_ranges(valid_from_date, invalid_to_date)
        assert form_errors == {
            'to_date_year': '\'From\' date is after the \'To\' date'
        }
        remove_date_ranges(contact_dates_form)

        # MULTI DATE RANGE VALID
        date_range_form_1 = DateRangeForm()
        date_range_form_2 = DateRangeForm()
        valid_from_date_1 = date.today() + relativedelta(days=7)
        valid_to_date_1 = valid_from_date + relativedelta(days=7)
        date_range_mock(date_range_form_1, valid_from_date_1, valid_to_date_1)

        valid_from_date_2 = date.today() + relativedelta(months=3)
        valid_to_date_2 = valid_from_date_2 + relativedelta(months=1)
        date_range_mock(date_range_form_2, valid_from_date_2, valid_to_date_2)

        contact_dates_form.date_ranges.append_entry(date_range_form_1)
        contact_dates_form.date_ranges.append_entry(date_range_form_2)

        date_range_forms = [date_range_form_1, date_range_form_2]
        date_ranges = {
            0: {'from_date': valid_from_date_1, 'to_date': valid_to_date_1},
            1: {'from_date': valid_from_date_2, 'to_date': valid_to_date_2}
        }

        assert contact_dates_form.validate()
        form_errors = {
            i: validate_date_range_form(date_range_form) for i, date_range_form in enumerate(date_range_forms)
        }
        assert form_errors == {0: {}, 1: {}}

        form_errors = {
            i: validate_date_ranges(
                date_range['from_date'], date_range['to_date']) for i, date_range in date_ranges.items()
        }
        assert form_errors == {0: {}, 1: {}}
        remove_date_ranges(contact_dates_form)

        # MULTI DATE RANGE INVALID
        date_range_form_1 = DateRangeForm()
        date_range_form_2 = DateRangeForm()
        invalid_from_date_1 = date.today() + relativedelta(days=7)
        invalid_to_date_1 = valid_from_date + relativedelta(days=7)
        erroneous_fields = {
            'from_month': '14',
            'to_day': ''
        }
        date_range_mock(date_range_form_1, invalid_from_date_1, invalid_to_date_1, **erroneous_fields)

        valid_from_date_2 = date.today() + relativedelta(months=3)
        invalid_to_date_2 = valid_from_date_2 - relativedelta(months=1)
        date_range_mock(date_range_form_2, valid_from_date_2, invalid_to_date_2)

        contact_dates_form.date_ranges.append_entry(date_range_form_1)
        contact_dates_form.date_ranges.append_entry(date_range_form_2)

        date_range_forms = [date_range_form_1, date_range_form_2]
        date_ranges = {
            0: {'from_date': invalid_from_date_1, 'to_date': invalid_to_date_1},
            1: {'from_date': valid_from_date_2, 'to_date': invalid_to_date_2}
        }

        assert contact_dates_form.validate()
        form_errors = {i: validate_date_range_form(date_range_form) for i, date_range_form in enumerate(date_range_forms)}
        assert form_errors == {
            0: {'from_date_month': 'Enter a month as a number between 1 and 12', 'to_date_day': 'Enter a day'},
            1: {}
        }
        form_errors = {
            i: validate_date_ranges(
                date_range['from_date'], date_range['to_date']) for i, date_range in date_ranges.items()
        }
        assert form_errors == {0: {}, 1: {'to_date_year': '\'From\' date is after the \'To\' date'}}
        remove_date_ranges(contact_dates_form)
