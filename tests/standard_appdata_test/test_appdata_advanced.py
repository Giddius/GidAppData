import pytest
import os
import shutil
from gidappdata import SupportKeeper, AppdataProvider, ConfigHandler
from gidappdata.utility import pathmaker, loadjson, writejson, writeit, readit, readbin, linereadit, appendwriteit


def test_appinfo(deployed_supportkeeper):
    assert SupportKeeper.dev == False
    assert SupportKeeper.author_name == "BrocaProgs"
    assert SupportKeeper.app_name == "Test_App"
    assert SupportKeeper.uses_base64 == True
    assert str(SupportKeeper.appdata) == deployed_supportkeeper[1]


def test_config_detection(deployed_supportkeeper):
    configs = ['solid_config', 'user_config', 'db_config']
    for config in configs:
        assert config in SupportKeeper.configs
    assert isinstance(SupportKeeper.solid_config, ConfigHandler)
    assert isinstance(SupportKeeper.user_config, ConfigHandler)
    assert isinstance(SupportKeeper.db_config, ConfigHandler)
