# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from datetime import timedelta
from django.utils.timezone import is_naive, get_default_timezone, make_aware, now
from datetime import datetime as py_time

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
STRATEGY_TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = "%s %s" % (DATE_FORMAT, TIME_FORMAT)


def datetime_to_str(datetime, format=DATETIME_FORMAT):
    if is_naive(datetime):
        datetime = to_aware_datetime(datetime)

    return datetime.strftime(format)


def datetime_delta(datetime, **kwargs):
    delta = timedelta(**kwargs)
    return datetime + delta


def str_to_datetime(str, format=DATETIME_FORMAT):
    if isinstance(str, py_time):
        if is_naive(str):
            return to_aware_datetime(str)
        else:
            return str

    return to_aware_datetime(py_time.strptime(str, format))


def to_aware_datetime(value):
    time_zone = get_default_timezone()
    return make_aware(value, time_zone)


def datetime_now():
    return now()


def dates_during(from_date, to_date, weekdays=None):
    if not weekdays:
        return []

    dates = []
    delta_day = (to_date - from_date).days
    for delta in range(1, delta_day+1):
        date = from_date + timedelta(days=delta)
        if date.weekday() + 1 in weekdays:
            dates.append(date)
    return dates


def get_weekday(datetime):
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    return days[datetime.weekday()]