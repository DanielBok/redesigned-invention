from collections import defaultdict
from datetime import datetime as dt

import pandas as pd
from pandas import Timedelta as td


def fcfs(df: pd.DataFrame, curr: dt = None, forecast=6, num_drivers=40, containers_per_driver=4):
    """
    A greedy optimization algorithm to determine which driver fetches which containers
    :param df: Current Dataframe of all data 
    :param curr: current time
    :param forecast: amount of hours to forecast to the future
    :param num_drivers: number of drivers
    :param containers_per_driver: number of containers each driver can fetch
    :return: dataframe
    """

    start = dt.now() if curr is None else curr
    end = start + td(hours=forecast)
    df = df.ix[(df.TIME >= start) & (df.TIME <= end)].reset_index(drop=1)
    tasks = []

    for _, row in df.iterrows():
        _items = [i.strip() for i in row.CONTAINER_INFO.split(';') if i.strip()]
        if len(_items) == 0:
            continue

        for n in range(0, len(_items), containers_per_driver):
            tasks.append([row.TIME,  # flight time of arrival/task available time
                          'ARRIVAL',  # type of event
                          row.FL,  # which flight number
                          'HOTA',
                          _items[n: n + containers_per_driver]])  # containers allocated

    # START Departure Task
    # This runs based on some assumptions
    dep_task = defaultdict(list)
    for task in tasks:
        start_time = task[0] + td(minutes=32)  # start time is the time where the baggage arrives
        # 32 is a magic number, 20 minutes process + 12 minutes transport from arrival to HOTA

        for item in task[-1]:
            flight = item.split()[3]
            dep_task[flight].append((start_time, item))

    for key, value in dep_task.items():
        _items = sorted(value, key=lambda x: x[0])  # sort according to the time started
        for n in range(0, len(_items), containers_per_driver):
            subset = _items[n: n + containers_per_driver]
            ready_time = subset[-1][0]
            tasks.append([ready_time,  # time of container is ready at HOTA
                          'DEPARTURE',  # type of event
                          'HOTA',  # from hot transfer area
                          key,  # to departure flight
                          [i[1] for i in subset]])  # container info
            # END Departure Task

    tasks = sorted(tasks, key=lambda x: x[0])

    # for each task, assign a driver, and count how many rounds the driver has been working.
    for index in range(len(tasks)):
        tasks[index].append(index % num_drivers)

    return pd.DataFrame(tasks, columns=["TIME", "TYPE", "FROM", "TO", "CONTAINERS", "DRIVER"]).to_dict('records')
