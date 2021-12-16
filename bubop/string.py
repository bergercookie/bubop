"""String-related utilities."""

from typing import Sequence


def non_empty(title: str, value: str, join_with: str = " -> ", newline=True) -> str:
    """
    Return a one-line formatted string of "title -> value" but only if value is a
    non-empty string. Otherwise return an empty string
    """

    if value:
        s = f"{title}{join_with}{value}"
        if newline:
            s = f"{s}\n"

        return s
    else:
        return ""


def format_items(
    items: Sequence[str], header: str, indent=2, bullet_char="-", header_sep="="
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
    return s
