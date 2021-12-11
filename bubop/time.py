"""Time-related utilities."""

import datetime
from enum import Enum
from typing import List, cast

import dateutil.parser
import dateutil.tz


class TimePeriod(Enum):
    """Holds different units of measuring time."""

    Microsecond = 0
    Second = 1
    Minute = 2
    Hour = 3
    Day = 4
    Month = 5
    Year = 6

    def higher_to_this(self) -> List["TimePeriod"]:
        """
        Return all the periods that are bigger than the current one.

        >>> [p.name for p in TimePeriod.Year.higher_to_this()]
        []
        >>> [p.name for p in TimePeriod.Month.higher_to_this()]
        ['Year']
        >>> [p.name for p in TimePeriod.Day.higher_to_this()]
        ['Month', 'Year']
        """
        return [p for p in all_periods if p.value > self.value]

    def lower_to_this(self) -> List["TimePeriod"]:
        """
        Return all the periods that are smaller than the current one.

        >>> [p.name for p in TimePeriod.Microsecond.lower_to_this()]
        []
        >>> [p.name for p in TimePeriod.Minute.lower_to_this()]
        ['Microsecond', 'Second']
        >>> [p.name for p in TimePeriod.Day.lower_to_this()]
        ['Microsecond', 'Second', 'Minute', 'Hour']
        """
        return [p for p in all_periods if p.value < self.value]

    def lower_or_equal_to_this(self) -> List["TimePeriod"]:
        """
        Return all the periods that are smaller or equal than the current one.

        >>> [p.name for p in TimePeriod.Microsecond.lower_or_equal_to_this()]
        ['Microsecond']
        """

        out = self.lower_to_this()
        out.append(self)
        return out

    def higher_or_equal_to_this(self) -> List["TimePeriod"]:
        """
        Return all the periods that are higher or equal than the current one.

        >>> [p.name for p in TimePeriod.Month.higher_or_equal_to_this()]
        ['Year', 'Month']
        """

        out = self.higher_to_this()
        out.append(self)
        return out


all_periods = list(TimePeriod)


def get_datetime_up_to(period: TimePeriod, dt: datetime.datetime) -> datetime.datetime:
    """
    Create a new date with only the parts up to the period specified. The rest are
    discarded.

    >>> dt = datetime.datetime(year=1, month=2, day=3, hour=4, minute=5, second=6, microsecond=7)
    >>> get_datetime_up_to(period=TimePeriod.Year, dt=dt)
    Traceback (most recent call last):
    TypeError: Invalid TimePeriod...
    >>> get_datetime_up_to(period=TimePeriod.Month, dt=dt)
    Traceback (most recent call last):
    TypeError: Invalid TimePeriod...
    >>> get_datetime_up_to(period=TimePeriod.Day, dt=dt)
    datetime.datetime(1, 2, 3, 0, 0)
    >>> get_datetime_up_to(period=TimePeriod.Hour, dt=dt)
    datetime.datetime(1, 2, 3, 4, 0)
    >>> get_datetime_up_to(period=TimePeriod.Minute, dt=dt)
    datetime.datetime(1, 2, 3, 4, 5)
    >>> get_datetime_up_to(period=TimePeriod.Second, dt=dt)
    datetime.datetime(1, 2, 3, 4, 5, 6)
    >>> get_datetime_up_to(period=TimePeriod.Microsecond, dt=dt) == dt
    True
    """
    if period is TimePeriod.Year or period is TimePeriod.Month:
        raise TypeError("Invalid TimePeriod, cannot nullify years or months.")

    to_discard = {p.name.lower(): 0 for p in period.lower_to_this()}
    to_keep = {
        p.name.lower(): cast(int, getattr(dt, (p.name.lower())))
        for p in period.higher_or_equal_to_this()
    }

    return datetime.datetime(**to_keep, **to_discard)  # type: ignore


def is_same_datetime(
    dt1: datetime.datetime,
    dt2: datetime.datetime,
    tol: datetime.timedelta = datetime.timedelta(0),
) -> bool:
    """Compare two datetime.datetime objects.

    If the timezone is empty, assume local timezone.

    >>> dt = datetime.datetime
    >>> td = datetime.timedelta
    >>> dt1 = datetime.datetime.now()
    >>> dt2 = dt1 + td(minutes=5)
    >>> is_same_datetime(dt1, dt2)
    False
    >>> is_same_datetime(dt1, dt2, tol=td(minutes=2))
    False
    >>> is_same_datetime(dt1, dt2, tol=td(minutes=5))
    True
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

    return abs(dt1_ - dt2_) <= tol


def parse_datetime(s: str) -> datetime.datetime:
    """Parse a datetime from the given string.

    >>> parse_datetime("2019-03-05") == datetime.datetime(2019, 3, 5, 0, 0)
    True
    >>> is_same_datetime(parse_datetime("2019-03-05T00:03:09Z"), datetime.datetime(2019, 3, 5, 0, 3, 9))
    True
    >>> is_same_datetime(parse_datetime("2019-03-05T00:03:01.1234Z"), datetime.datetime(2019, 3, 5, 0, 3, 1, 123400))
    True
    >>> is_same_datetime(parse_datetime("2019-03-08T00:29:06.602Z"), datetime.datetime(2019, 3, 8, 0, 29, 6, 602000))
    True
    """
    return dateutil.parser.parse(s)


def format_datetime_tz(dt: datetime.datetime) -> str:
    """
    Format a datetime object according to the ISO specifications containing
    the 'T' and 'Z' separators

    Usage::

    >>> format_datetime_tz(datetime.datetime(2019, 3, 5, 0, 3, 9, 1234))
    '2019-03-05T00:03:09.001234Z'
    >>> format_datetime_tz(datetime.datetime(2019, 3, 5, 0, 3, 9, 123))
    '2019-03-05T00:03:09.000123Z'
    """
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
