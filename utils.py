from datetime import datetime as dt
from pytz import timezone


from configs.settings import TIMEZONE


def now():
    return dt.now(timezone(TIMEZONE))