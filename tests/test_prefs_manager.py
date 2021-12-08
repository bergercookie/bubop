import pytest

import bubop.common_dir as common_dir
from bubop import OperatingSystemNotSupportedError, PrefsManager

from .test_utils import set_system


class TestPrefsManager:
    @pytest.mark.parametrize("fs", [[None, [common_dir]]], indirect=True)
    def test_config_directory(self, fs):
        with PrefsManager(app_name="myapp", config_fname="custom_name.yaml") as prefs_manager:
            assert prefs_manager.config_directory.name == "myapp"
            assert prefs_manager.config_file.name == "custom_name.yaml"
            assert prefs_manager.config_file.parent.name == "myapp"

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

    def test_raise_unsupported_system(self, fs):
        with set_system("random os"):
            with pytest.raises(OperatingSystemNotSupportedError):
                PrefsManager(app_name="test1")
