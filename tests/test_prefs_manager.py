from pathlib import Path
from unittest.mock import patch

import pytest

import bubop.common_dir as common_dir
from bubop import OperatingSystemNotSupportedError, PrefsManager


class TestPrefsManager:
    @pytest.mark.parametrize("fs", [[None, [common_dir]]], indirect=True)
    def test_config_directory(self, fs):
        with PrefsManager(app_name="myapp", config_fname="custom_name.yaml") as prefs_manager:
            assert prefs_manager.config_directory.name == "myapp"
            assert prefs_manager.config_file.name == "custom_name.yaml"
            assert prefs_manager.config_file.parent.name == "myapp"

    @pytest.mark.parametrize("fs", [[None, [common_dir]]], indirect=True)
    def test_config_fname_no_ext(self, fs):
        with PrefsManager(app_name="myapp", config_fname="custom_name") as prefs_manager:
            assert prefs_manager.config_file.name == "custom_name.yaml"

    @pytest.mark.parametrize("fs", [[None, [common_dir]]], indirect=True)
    def test_app_name_ends_in_py(self, fs):
        with PrefsManager(app_name="myapp.py") as prefs_manager:
            assert prefs_manager.config_directory.name == "myapp"

    @pytest.mark.parametrize("fs", [[None, [common_dir]]], indirect=True)
    def test_dict_functions(self, fs):
        with PrefsManager(app_name="myapp") as prefs_manager:
            prefs_manager["a"] = 1
            prefs_manager["b"] = 2
            prefs_manager["c"] = 3
            assert prefs_manager.keys() == list("abc")
            assert list(prefs_manager.values()) == list([1, 2, 3])
            assert list(prefs_manager.items()) == list(zip("abc", [1, 2, 3]))
            assert len(prefs_manager) == 3

            assert "a" in prefs_manager
            assert "b" in prefs_manager
            assert "d" not in prefs_manager

    @pytest.mark.parametrize("fs", [[None, [common_dir]]], indirect=True)
    def test_multiple_cleanups(self, fs):
        prefs_manager = PrefsManager(app_name="myapp")
        prefs_manager._cleanup()
        prefs_manager._cleanup()

    @pytest.mark.parametrize("fs", [[None, [common_dir]]], indirect=True)
    def test_config_dir_is_file(self, fs):
        app = "app"
        Path("~/.config").expanduser().mkdir(parents=True)
        Path(f"~/.config/app").expanduser().touch()
        with pytest.raises(NotADirectoryError):
            PrefsManager(app_name=app)

    @pytest.mark.parametrize("fs", [[None, [common_dir]]], indirect=True)
    def test_set_get(self, fs):
        with PrefsManager(app_name="test_set_get") as prefs_manager:
            prefs_manager["myval"] = 1
            prefs_manager["myval2"] = "a_string"
            assert prefs_manager["myval"] == 1
            assert prefs_manager["myval2"] == "a_string"

    @pytest.mark.parametrize("fs", [[None, [common_dir]]], indirect=True)
    def test_set_close_get(self, fs):
        with PrefsManager(app_name="test_set_get") as prefs_manager:
            prefs_manager["myval"] = 1
            prefs_manager["myval2"] = "a_string"

        with PrefsManager(app_name="test_set_get") as prefs_manager:
            assert prefs_manager["myval"] == 1
            assert prefs_manager["myval2"] == "a_string"

        with PrefsManager(app_name="another_app") as prefs_manager:
            assert prefs_manager.empty()

    @pytest.mark.parametrize("fs", [[None, [common_dir]]], indirect=True)
    def test_get_from_empty(self, fs):
        with PrefsManager(app_name="test_get_from_empty") as prefs_manager:
            with pytest.raises(KeyError):
                prefs_manager["myval"]

    @pytest.mark.parametrize("fs", [[None, [common_dir]]], indirect=True)
    def test_set_get_attr(self, fs):
        with PrefsManager(app_name="test_set_get_attr") as prefs_manager:
            with pytest.raises(AttributeError):
                print(prefs_manager.myval)

            prefs_manager["myval"] = 1

        with PrefsManager(app_name="test_set_get_attr") as prefs_manager:
            assert prefs_manager.myval == 1

    @pytest.mark.parametrize("fs", [[None, [common_dir]]], indirect=True)
    def test_update_latest(self, fs):
        with PrefsManager(app_name="test_update_latest") as prefs_manager:
            prefs_manager["myval"] = 1
            assert prefs_manager.myval == 1
            prefs_manager.update_latest("kalimera")
            prefs_manager["myval"] = "kalimera"

    @pytest.mark.parametrize("fs", [[None, [common_dir]]], indirect=True)
    def test_update_latest_from_empty(self, fs):
        """
        You probably want:
        ehttp://jmcgeheeiv.github.io/pyfakefs/master/usage.html#modules-to-patch
        """
        prefs_manager = PrefsManager(app_name="test2")
        with pytest.raises(RuntimeError):
            prefs_manager.update_latest(new_val="val")

    def test_invalid_config_fname(self, fs):
        with pytest.raises(RuntimeError):
            PrefsManager(app_name="test", config_fname="cfg.toml")

    @patch("platform.system")
    def test_raise_unsupported_system(self, mock_system):
        mock_system.return_value = "random"
        with pytest.raises(OperatingSystemNotSupportedError):
            PrefsManager(app_name="test1")
