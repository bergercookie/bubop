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
