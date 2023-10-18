from datetime import datetime
from dateutil import tz


def convert_date_to_local_timezone(date_to_convert: datetime):
    return date_to_convert.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/London'))
