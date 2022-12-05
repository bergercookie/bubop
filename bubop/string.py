"""String-related utilities."""

import random
import string
from typing import Any, List, Mapping, Sequence


def camel_case_to_dashed(s: str) -> str:
    """
    Convert a CamelCase string into the dashed representation.

    >>> camel_case_to_dashed("KalimeraKalinuxta")
    'kalimera-kalinuxta'
    >>> camel_case_to_dashed("somethingIsRotten")
    'something-is-rotten'
    >>> camel_case_to_dashed("SLAM")
    'slam'
    """
    new_chars: List[str] = []
    last_char = ""
    for char in s:
        if char.isupper():
            if not last_char.isupper():
                new_chars.append("-")
            new_chars.append(char.lower())
        else:
            new_chars.append(char)

        last_char = char
    return "".join(new_chars).lstrip("-")


def non_empty(title: str, value: str, join_with: str = " -> ", newline=True) -> str:
    """
    Return a one-line formatted string of "title -> value" but only if value is a
    non-empty string. Otherwise return an empty string

    >>> non_empty(title="title", value="value")
    'title -> value\\n'
    >>> non_empty(title="title", value=None)
    ''
    """

    if value:
        s = f"{title}{join_with}{value}"
        if newline:
            s = f"{s}\n"

        return s
    else:
        return ""


def format_list(  # pylint: disable=R0913
    items: Sequence[str],
    header: str,
    indent=2,
    bullet_char="-",
    header_sep="=",
    prefix: str = "",
    suffix: str = "",
) -> str:
    """
    Format and return a string with the corresponding header and all the items each occupying a
    single line and with the specified indentation.
    """
    s = f"{header}: "
    if not items:
        s += " None."
        return s

    s += "\n" + len(s) * header_sep
    s += "\n\n"
    s += "\n".join(f'{" " * indent}{bullet_char} {item}' for item in items)
    s += "\n\n"
    return f"{prefix}{s}{suffix}"


def format_dict(items: Mapping[Any, Any], align_items: bool = True, **kargs) -> str:
    """
    Utility for formatting a dictionary - similar to print.pformat.

    Accepts mostly the same arguments as format_list.
    """

    items_: Sequence[str]
    if align_items:
        keys_length = max(len(str(key)) for key in items.keys())
        format_ = "{0: <%d}" % keys_length  # pylint: disable=C0209
        items_ = [f"{format_.format(k)}: {v}" for k, v in items.items()]
    else:
        items_ = [f"{k}: {v}" for k, v in items.items()]

    return format_list(items=items_, **kargs)  # type: ignore


def get_random_string(len_=10) -> str:
    """Return a random string containing ascii characters, digits and punctuation marks."""
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(len_))
