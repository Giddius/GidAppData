import pytest
import os
import shutil
from gidappdata import ParaStorageKeeper, AppdataProvider, ConfigHandler
from gidappdata.utility import pathmaker, loadjson, writejson, writeit, readit, readbin, linereadit, appendwriteit


def test_appinfo(deployed_supportkeeper):
    assert ParaStorageKeeper.dev == False
    assert ParaStorageKeeper.author_name == "BrocaProgs"
    assert ParaStorageKeeper.app_name == "Test_App"
    assert ParaStorageKeeper.uses_base64 == True
    assert str(ParaStorageKeeper.appdata) == deployed_supportkeeper[1]


def test_config_detection(deployed_supportkeeper):
    configs = ['solid_config', 'user_config', 'db_config']
    for config in configs:
        assert config in ParaStorageKeeper.configs
    assert isinstance(ParaStorageKeeper.solid_config, ConfigHandler)
    assert isinstance(ParaStorageKeeper.user_config, ConfigHandler)
    assert isinstance(ParaStorageKeeper.db_config, ConfigHandler)
