import sys
import traceback
from io import StringIO
from typing import Optional


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
        self.exception: Optional[Exception] = None
        self.exc_type = None
        self._print_fn = print_fn

    def register(self):
        self._orig_exit = sys.exit
        sys.exit = self.exit
        sys.excepthook = self.exc_handler

    def exit(self, code=0):
        self.exit_code = code
        self._orig_exit(code)

    def exc_handler(self, exc_type, exc_value, tb, *args):
        self.exception = exc_value
        self.exc_type = exc_type

        io_stream = StringIO()
        traceback.print_tb(tb=tb, file=io_stream)

        self._print_fn(
            f"Exception was raised during program execution.\n\n{io_stream.getvalue()}\n\n"
            f"{exc_value.with_traceback(tb)}"
        )
        self.exit(1)
