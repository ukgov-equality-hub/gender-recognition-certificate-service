from flask_wtf import FlaskForm
from datetime import date
from grc.personal_details.forms import DateRangeForm


def single_date_mock(form: FlaskForm, form_date: date, **kwargs):
    form.day.data = str(form_date.day)
    form.month.data = str(form_date.month)
    form.year.data = str(form_date.year)

    if 'day' in kwargs:
        form.day.data = kwargs.get('day')

    if 'month' in kwargs:
        form.month.data = kwargs.get('month')

    if 'year' in kwargs:
        form.year.data = kwargs.get('year')


def date_range_mock(form: DateRangeForm, from_date: date, to_date: date, **kwargs):
    form.from_date_day.data = str(from_date.day)
    form.from_date_month.data = str(from_date.month)
    form.from_date_year.data = str(from_date.year)

    form.to_date_day.data = str(to_date.day)
    form.to_date_month.data = str(to_date.month)
    form.to_date_year.data = str(to_date.year)

    if 'from_day' in kwargs:
        form.from_date_day.data = kwargs.get('from_day')

    if 'from_month' in kwargs:
        form.from_date_month.data = kwargs.get('from_month')

    if 'from_year' in kwargs:
        form.from_date_year.data = kwargs.get('from_year')

    if 'to_day' in kwargs:
        form.to_date_day.data = kwargs.get('to_day')

    if 'to_month' in kwargs:
        form.to_date_month.data = kwargs.get('to_month')

    if 'to_year' in kwargs:
        form.to_date_year.data = kwargs.get('to_year')


def remove_date_ranges(form: FlaskForm):
    for _ in range(len(form.date_ranges)):
        form.date_ranges.pop_entry()
