from datetime import datetime
from pytz import timezone


def convert_date_to_local_timezone(date_to_convert: datetime):
    return date_to_convert.astimezone(timezone('Europe/London'))
