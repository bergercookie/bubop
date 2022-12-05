"""Argparse-related utilities."""

from argparse import ArgumentParser
from typing import Optional


def add_bool_argument(
    parser: ArgumentParser,
    arg_name: str,
    default: Optional[bool] = None,
    true_help: Optional[str] = None,
):
    """Add a boolean CLI argument to the given ArgumentParser object.

    The flag defaults to *False* if no other is specified

    Usage::


    >>> import argparse
    >>> parser = argparse.ArgumentParser(description="SomeArgumentParser")
    >>> add_bool_argument(parser, "someflag")
    >>> add_bool_argument(parser, "someflag2", default=True)
    >>> add_bool_argument(parser, "someflag3", default=False)
    >>> add_bool_argument(parser, "someflag4", true_help="somehelp4")
    >>> add_bool_argument(parser, "a_flag")
    >>> add_bool_argument(parser, "b-flag")
    >>> config = parser.parse_args(["--someflag"]) # basic
    >>> config.someflag
    True
    >>> config = parser.parse_args(["--no-someflag"])
    >>> config.someflag
    False

    >>> config = vars(parser.parse_args([])) # defaults
    >>> config["someflag"] == False
    True
    >>> config["someflag2"] == True
    True
    >>> config["someflag3"] == False
    True
    >>> config["someflag4"] == False
    True
    >>> "somehelp4" in parser.format_help()
    True
    >>> parser.parse_args(["--someflag", "--no-someflag"]) # exception
    Traceback (most recent call last):
    ...
    SystemExit: 2

    >>> config = vars(parser.parse_args(["--a_flag"]))
    >>> config["a_flag"] == True
    True
    >>> config = vars(parser.parse_args(["--b-flag"]))
    >>> config["b-flag"] == True
    True
    """

    def _format(s: str):
        return f"{s}{arg_name}"

    group = parser.add_mutually_exclusive_group()

    true_help = true_help if default is False else f"{true_help} [default]"
    false_help = "" if default is True else "[default]"

    group.add_argument(_format("--"), dest=arg_name, action="store_true", help=true_help)
    group.add_argument(_format("--no-"), dest=arg_name, action="store_false", help=false_help)

    if default:
        kwargs = {arg_name: default}
        group.set_defaults(**kwargs)
