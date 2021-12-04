"""Time-related utilities"""

import datetime

import dateutil
import dateutil.tz


def is_same_datetime(dt1: datetime.datetime, dt2: datetime.datetime) -> bool:
    """Compare two datetime.datetime objects.

    If the timezone is empty, assume local timezone
    """

    assert isinstance(dt1, datetime.datetime)
    assert isinstance(dt2, datetime.datetime)

    # if there is no timezone, assume local timezone
    if dt1.tzinfo is None:
        dt1_ = dt1.replace(tzinfo=dateutil.tz.tzlocal())
    else:
        dt1_ = dt1

    if dt2.tzinfo is None:
        dt2_ = dt2.replace(tzinfo=dateutil.tz.tzlocal())
    else:
        dt2_ = dt2

    return dt1_ == dt2_


def parse_datetime(s: str) -> datetime.datetime:
    """Parse a datetime from the given string.

    >>> GCalSide.parse_datetime("2019-03-05T00:03:09Z")
    datetime.datetime(2019, 3, 5, 0, 3, 9)
    >>> GCalSide.parse_datetime("2019-03-05")
    datetime.datetime(2019, 3, 5, 0, 0)
    >>> GCalSide.parse_datetime("2019-03-05T00:03:01.1234Z")
    datetime.datetime(2019, 3, 5, 0, 3, 1, 123400)
    >>> GCalSide.parse_datetime("2019-03-08T00:29:06.602Z")
    datetime.datetime(2019, 3, 8, 0, 29, 6, 602000)
    """
    return dateutil.parser.parse(s)


def format_datetime_tz(dt: datetime.datetime) -> str:
    """
    Format a datetime object according to the ISO specifications containing
    the 'T' and 'Z' separators

    Usage::

    >>> format_datetime_tz(datetime.datetime(2019, 3, 5, 0, 3, 9, 1234))
    '2019-03-05T00:03:09.001234Z'
    >>> GCalSide.format_datetime_tz(datetime.datetime(2019, 3, 5, 0, 3, 9, 123))
    '2019-03-05T00:03:09.000123Z'
    """
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
