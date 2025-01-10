"""Exit hooks class."""
import sys
import traceback
from collections.abc import Callable
from io import StringIO


class ExitHooks:
    """
    Monkeypatch sys.exit + set the excepthook to figure out when an exception or an exit event
    was raised.

    Set this during program execution and then, e.g., during program teardown, e.g.,  using
    atexit, figure out whether an exception was raised or whether the program exited
    successfully or failed.
    """

    def __init__(self, print_fn=print):
        self.exit_code = None
        self.exception: Exception | None = None
        self.exc_type = None
        self._print_fn = print_fn
        self._orig_exit: Callable[[int], None]

    def register(self):
        """Register the exit hook."""
        self._orig_exit = sys.exit
        sys.exit = self.exit
        sys.excepthook = self.exc_handler

    def exit(self, code=0):
        """Exit function override."""
        self.exit_code = code
        self._orig_exit(code)

    def exc_handler(self, exc_type, exc_value, tb, *args):
        """Exception handler override."""
        self.exception = exc_value
        self.exc_type = exc_type

        io_stream = StringIO()
        traceback.print_tb(tb=tb, file=io_stream)

        self._print_fn(
            f"Exception was raised during program execution.\n\n{io_stream.getvalue()}\n\n"
            f"{exc_value.with_traceback(tb)}"
        )
        self.exit(1)
