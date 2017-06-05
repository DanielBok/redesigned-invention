from datetime import datetime as dt

import pandas as pd
from pytz import timezone
from os.path import abspath, dirname, join

from configs.settings import TIMEZONE


def _make_df():
    data_dir = abspath(join(dirname(__file__), 'data'))
    df_c = pd.read_pickle(join(data_dir, 'containers.p'))
    df_f = pd.read_pickle(join(data_dir, 'flights.p'))

    df_c.TIME = df_c.TIME.map(lambda x: x.tz_localize(timezone('Asia/Singapore')))
    df_f.TIME = df_f.TIME.map(lambda x: x.tz_localize(timezone('Asia/Singapore')))

    return df_c, df_f


# CONTAINERS, FLIGHTS = _make_df()


def now():
    return dt.now(timezone(TIMEZONE))
