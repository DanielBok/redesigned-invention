from datetime import datetime as dt, timedelta as td

from pytz import timezone

from configs.settings import TIMEZONE


def now():
    return dt.now(timezone(TIMEZONE))


def localize(d: dt):
    offset = d.replace(tzinfo=TIMEZONE).utcoffset().total_seconds()
    return d.replace(tzinfo=TIMEZONE) + td(seconds=offset)
