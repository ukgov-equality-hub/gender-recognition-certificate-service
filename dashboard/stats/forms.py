from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from grc.utils.form_custom_validators import validateDateRange, Integer


class DateRangeForm(FlaskForm):
    start_date_day = StringField(
        validators=[
            DataRequired(message='Enter a start day'),
            Integer(min=1, max=31, message='Enter a start day as a number between 1 and 31')
        ]
    )

    start_date_month = StringField(
        validators=[
            DataRequired(message='Enter a start month'),
            Integer(min=1, max=12, message='Enter a start month as a number between 1 and 12')
        ]
    )

    start_date_year = StringField(
        validators=[
            DataRequired(message='Enter a start year'),
            Integer(min=1000, message='Enter a start year as a 4-digit number, like 2000',
                    validators=[validateDateRange])
        ]
    )

    end_date_day = StringField(
        validators=[
            DataRequired(message='Enter an end day'),
            Integer(min=1, max=31, message='Enter an end day as a number between 1 and 31')
        ]
    )

    end_date_month = StringField(
        validators=[
            DataRequired(message='Enter an end month'),
            Integer(min=1, max=12, message='Enter an end month as a number between 1 and 12')
        ]
    )

    end_date_year = StringField(
        validators=[
            DataRequired(message='Enter an end year'),
            Integer(min=1000, message='Enter an end year as a 4-digit number, like 2000',
                    validators=[validateDateRange])
        ]
    )
