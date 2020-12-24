from django.utils import timezone
from datetime import datetime


def convert_datetime_utc_to_local(utc_dt):
    return timezone.localtime(utc_dt)


def now():
    return convert_datetime_utc_to_local(timezone.now())


def convert_str_to_datetime(str_datetime):
    if len(str_datetime) != len('YYYY-mm-dd'):
        return None

    try:
        return convert_datetime_utc_to_local(datetime.strptime(str_datetime, "%Y-%m-%d").astimezone())
    except:
        return None
