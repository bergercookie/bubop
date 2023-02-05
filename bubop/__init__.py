"""Init."""
from bubop.arg_parser import add_bool_argument
from bubop.classes import all_subclasses
from bubop.cli import check_optional_mutually_exclusive, check_required_mutually_exclusive
from bubop.common_dir import CommonDir
from bubop.crypto import read_gpg_token, write_gpg_token
from bubop.exceptions import (
    AuthenticationError,
    CliIncompatibleOptionsError,
    NoSuchFileOrDirectoryError,
    NotEnoughArgumentsError,
    OperatingSystemNotSupportedError,
)
from bubop.fs import FileType, get_valid_filename, valid_dir, valid_file, valid_path
from bubop.inspect import inspect_var_name
from bubop.logging import (
    log_to_syslog,
    logger,
    loguru_set_verbosity,
    loguru_tqdm_sink,
    verbosity_int_to_std_logging_lvl,
    verbosity_int_to_str,
)
from bubop.misc import get_object_unique_name, xor
from bubop.prefs_manager import PrefsManager
from bubop.serial import pickle_dump, pickle_load
from bubop.string import (
    camel_case_to_dashed,
    format_dict,
    format_list,
    get_random_string,
    non_empty,
)
from bubop.time import (
    assume_local_tz_if_none,
    format_datetime_tz,
    is_same_datetime,
    parse_datetime,
)

__all__ = [
    "AuthenticationError",
    "CliIncompatibleOptionsError",
    "CommonDir",
    "FileType",
    "NoSuchFileOrDirectoryError",
    "NotEnoughArgumentsError",
    "OperatingSystemNotSupportedError",
    "PrefsManager",
    "add_bool_argument",
    "all_subclasses",
    "assume_local_tz_if_none",
    "camel_case_to_dashed",
    "check_optional_mutually_exclusive",
    "check_required_mutually_exclusive",
    "format_datetime_tz",
    "format_dict",
    "format_list",
    "get_random_string",
    "get_object_unique_name",
    "get_valid_filename",
    "inspect_var_name",
    "is_same_datetime",
    "log_to_syslog",
    "logger",
    "loguru_set_verbosity",
    "loguru_tqdm_sink",
    "non_empty",
    "parse_datetime",
    "pickle_dump",
    "pickle_load",
    "read_gpg_token",
    "write_gpg_token",
    "valid_dir",
    "valid_file",
    "valid_path",
    "verbosity_int_to_std_logging_lvl",
    "verbosity_int_to_str",
    "xor",
]

__version__ = "0.1.10"
