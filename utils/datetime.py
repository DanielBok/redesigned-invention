from datetime import datetime as dt, timedelta as td

from pytz import timezone

from configs.settings import TIMEZONE


def now():
    return dt.now(timezone(TIMEZONE))


def localize(d: dt):
    offset = d.replace(tzinfo=timezone(TIMEZONE)).utcoffset().total_seconds()
    return str(d.replace(tzinfo=timezone(TIMEZONE)) + td(seconds=offset))[:19]
