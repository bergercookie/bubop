"""Logging-oriented utilities."""
import logging
import logging.handlers
import sys
from typing import Mapping

import loguru
import tqdm
from loguru import logger  # pylint: disable=W0611
from typing_extensions import Literal

LoguruLogLevel = Literal[
    "FATAL",
    "ERROR",
    "WARNING",
    "INFO",
    "DEBUG",
    "TRACE",
]

_verbosity_int_to_str: Mapping[int, LoguruLogLevel] = {0: "INFO", 1: "DEBUG", 2: "TRACE"}


def verbosity_int_to_str(verbosity: int) -> LoguruLogLevel:
    """
    Map a verbosity integer to the corresponding Loguru Level.
    :param verbosity: 0 for >= INFO,
                      1 for >= DEBUG,
                      2 for >= TRACE
    """
    if verbosity < 0:
        raise RuntimeError("verbosity must be >= 0")
    elif verbosity > 2:
        verbosity = 2

    return _verbosity_int_to_str[verbosity]


def loguru_set_verbosity(verbosity: int):
    """
    Set the verbosity of the tqdm logger.
    :param verbosity: 0 for >= INFO,
                      1 for >= DEBUG,
                      2 for >= TRACE
    """
    loguru.logger.remove()
    loguru.logger.add(
        sys.stderr,  # type: ignore
        format=(
            "<green>{time:HH:mm:ss.SS}</green> | <level>{level}</level> \t|"
            " <level>{message}</level>"
        ),
        level=verbosity_int_to_str(verbosity),
    )


def loguru_tqdm_sink(verbosity: int):
    """Change the default loguru logger to use tqdm.

    :param verbosity: Set the verbosity of the tqdm logger.
                      0 for >= INFO,
                      1 for >= DEBUG,
                      2 for >= TRACE
    """
    loguru.logger.remove()
    loguru.logger.add(
        lambda msg: tqdm.tqdm.write(msg, end=""),  # type: ignore
        format=(
            "<green>{time:HH:mm:ss.SS}</green> | <level>{level}</level> \t|"
            " <level>{message}</level>"
        ),
        level=verbosity_int_to_str(verbosity),
        colorize=True,
    )


def log_to_syslog(name: str, level: LoguruLogLevel = "WARNING"):
    """Enable logging to syslog for the given logger.

    This method does not remove any of the existing logging handlers.
    """

    # (also) log to syslog
    _format_nocolor = "%s | {level:8} | {message}" % name  # pylint: disable=W1310,C0209
    address = "/dev/log" if sys.platform == "linux" else "/var/run/syslog"
    loguru.logger.add(
        logging.handlers.SysLogHandler(address=address),
        format=_format_nocolor,
        level=level,
    )


# Mapping from verbosity count (e.g. with -vvv from cli) to levels of logging in the standard
# library logging module.
_verbosity_to_logging_lvl = {
    0: logging.INFO,
    1: logging.DEBUG,
    2: logging.DEBUG,  # there's no trace level
}


def verbosity_int_to_std_logging_lvl(verbosity: int) -> int:
    """Map an integer to a corresponding python std logging module level
    :param verbosity: Set the verbosity of the tqdm logger.
                      0 for >= INFO,
                      1 for >= DEBUG,
    """
    if verbosity < 0:
        raise RuntimeError("verbosity must be >= 0")
    elif verbosity > 2:
        verbosity = 2

    return _verbosity_to_logging_lvl[verbosity]
