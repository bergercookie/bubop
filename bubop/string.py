"""String-related utilities."""


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
