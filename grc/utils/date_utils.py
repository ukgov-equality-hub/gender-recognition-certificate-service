from datetime import datetime, timedelta
from dateutil import tz
from dateutil.relativedelta import relativedelta


class DateUtil:

    def __init__(self, date_to_check, date_format, years=None, months=None, weeks=None, days=None, minutes=None,
                 hours=None, seconds=None):
        self.date_to_check_string: str = date_to_check
        self.date_format: str = date_format
        self.years: int = years if years else 0
        self.months: int = months if months else 0
        self.weeks: int = weeks if weeks else 0
        self.days: int = days if days else 0
        self.hours: int = hours if hours else 0
        self.minutes: int = minutes if minutes else 0
        self.seconds: int = seconds if seconds else 0

    def is_date_before_timeframe_specified(self) -> bool:
        date_to_check = datetime.strptime(self.date_to_check_string, self.date_format)
        now_date_string = datetime.now().replace(tzinfo=tz.gettz('UTC')).astimezone(
            tz.gettz('Europe/London')).strftime(self.date_format)
        now_date = datetime.strptime(now_date_string, self.date_format)
        date_to_check_against = now_date - relativedelta(years=self.years, months=self.months, weeks=self.weeks,
                                                         days=self.days, hours=self.hours, minutes=self.minutes,
                                                         seconds=self.seconds)

        return date_to_check < date_to_check_against
