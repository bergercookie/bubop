from pathlib import Path

import pytest

from bubop import CommonDir, OperatingSystemNotSupportedError

from .test_utils import set_system


def test_common_dir_windows():
    with set_system("Windows"):
        with pytest.raises(OperatingSystemNotSupportedError):
            CommonDir.config()
        with pytest.raises(OperatingSystemNotSupportedError):
            CommonDir.share()
        with pytest.raises(OperatingSystemNotSupportedError):
            CommonDir.cache()


@pytest.mark.parametrize("os", ["Linux", "Darwin"])
def test_common_dir(os):
    with set_system(os):
        config = CommonDir.config()
        share = CommonDir.share()
        cache = CommonDir.cache()

        home = str(Path().home())
        assert str(config).startswith(home)
        assert str(share).startswith(home)
        assert str(cache).startswith(home)
