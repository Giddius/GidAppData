# region [Imports]


import lzma
import os
from dotenv import load_dotenv
import zipfile
import os
import base64
import logging
import gidlogger as glog

from configparser import ConfigParser

from gidappdata.standard_appdata.appdata_storager import AppDataStorager
from gidappdata.utility.functions import pathmaker, to_attr_name, filename_to_attr_name, create_folder, create_file, readit, writeit
from gidappdata.utility.extended_dotenv import find_dotenv_everywhere
from gidappdata.utility.exceptions import ConstructionEnvDataMissing, DevSettingError
from gidappdata.cli.pack_and_bin_and_py_data import generate_user_data_binfile
from gidappdata.utility.bridge_configparser import AdaptedConfigParser
# endregion [Imports]


# region [Logging]

log = logging.getLogger('gidappdata')
log.info(glog.imported(__name__))

# endregion [Logging]


class ParaStorageKeeperMetaHelper(type):
    def __getattr__(cls, name):
        _out = ParaStorageKeeper.configs.get(name, None)
        if _out is None:
            _out = ParaStorageKeeper.app_info.get(name)
        if _out is None:
            raise AttributeError
        return _out


class ParaStorageKeeper(metaclass=ParaStorageKeeperMetaHelper):
    # region [ClassAttributes]

    is_init = False
    appdata = None
    configs = {}
    construction_env_filename = 'construction_info.env'
    app_info = {'app_name': None, 'author_name': None, 'uses_base64': None, 'clean': True, 'dev': False, 'redirect': '', 'log_folder': '', "is_unpacked": False}
    config_handler = AdaptedConfigParser
    archive_data = None
    # endregion[ClassAttributes]

    @staticmethod
    def _unzip(root_dir, zip_file, overwrite: bool = False):
        # sourcery skip: simplify-boolean-comparison
        with zipfile.ZipFile(zip_file, 'r') as zipf:
            for item in zipf.namelist():
                _info = zipf.getinfo(item)
                if _info.is_dir() is True:
                    create_folder(pathmaker(root_dir, item))
                else:
                    if os.path.isfile(pathmaker(root_dir, item)) is False or overwrite is True:
                        zipf.extract(item, pathmaker(root_dir))
                        log.debug("extracted file '%s' because it didn't exist", pathmaker(root_dir, item))
                    else:
                        log.debug("file '%s' is already existing and overwrite is 'False' so file was not extracted", pathmaker(root_dir, item))
        log.info('unzipping finished')

    @classmethod
    def set_special_config_handler(cls, handler_class):
        cls.config_handler = handler_class

    @classmethod
    def set_clean(cls, setting: bool):
        cls.app_info['clean'] = setting

    @classmethod
    def set_dev(cls, setting: bool, redirect=None, log_folder=None):
        # sourcery skip: simplify-boolean-comparison
        cls.app_info['dev'] = setting
        if setting is True:
            if redirect is None:
                raise DevSettingError()
            cls.app_info['redirect'] = pathmaker(redirect)
            cls.app_info['log_folder'] = pathmaker(log_folder)

    @classmethod
    def set_archive_data(cls, archive_data: bytes):
        cls.archive_data = archive_data

    @staticmethod
    def checked_get_env(env_var_name):
        _out = os.getenv(env_var_name)
        if _out is None:
            raise ConstructionEnvDataMissing(env_var_name)
        if _out.casefold() in ['true', 'yes', '1']:
            _out = True
        elif _out.casefold() in ['false', 'no', '0']:
            _out = False
        else:
            _out = _out
        return _out

    @classmethod
    def _archive_from_bin(cls, bin_data, name: str = 'user_data_archive', ext: str = 'zip', uses_base64: bool = False):
        _file = pathmaker(str(cls.appdata), name + '.' + ext)
        with open(_file, 'wb') as archfile:
            _bin_data = bin_data if not uses_base64 else base64.b64decode(bin_data)
            archfile.write(_bin_data)
        return _file

    @classmethod
    def unpack_archive(cls, in_archive, clean: bool, uses_base64: bool):
        _file = cls._archive_from_bin(in_archive, uses_base64=uses_base64)
        cls._unzip(str(cls.appdata), _file, False)
        if clean:
            os.remove(_file)

    @classmethod
    def find_construct_env(cls):
        for dirname, folderlist, filelist in os.walk(os.getcwd()):
            for file in filelist:
                if file == cls.construction_env_filename:
                    return pathmaker(dirname, file)

    @classmethod
    def set_unpacked(cls):
        cls.app_info['is_unpacked'] = True

    @classmethod
    def initialize(cls, archive_data=None):
        if cls.is_init is True:
            return
        load_dotenv(find_dotenv_everywhere(cls.construction_env_filename))
        for info in cls.app_info:
            if cls.app_info[info] is None:
                cls.app_info[info] = cls.checked_get_env(info.upper())
        redirect = None if cls.app_info['redirect'] == '' else cls.app_info['redirect']
        log_folder = None if cls.app_info['log_folder'] == '' else cls.app_info['log_folder']
        archive_data = cls.archive_data if archive_data is None else archive_data
        cls.appdata = AppDataStorager(cls.app_info['author_name'], cls.app_info['app_name'], cls.app_info['dev'], redirect, log_folder)

        if cls.app_info['dev'] is False or cls.app_info.get('is_unpacked') is False:
            cls.unpack_archive(archive_data, cls.app_info['clean'], cls.app_info['uses_base64'])
            cls.set_unpacked()
        if os.path.isdir(cls.appdata['config']) is True:
            for file in os.scandir(cls.appdata['config']):
                if file.name.endswith('.ini') and 'config' in file.name:
                    name = filename_to_attr_name(file.name)
                    cls.configs[name] = cls.config_handler.from_defaults(cls.appdata[file.name])
        cls.is_init = True

    @classmethod
    def get_appdata(cls):
        if cls.is_init is False:
            cls.initialize()
        return cls.appdata

    @classmethod
    def get_config(cls, config_name):
        if cls.is_init is False:
            cls.initialize()
        return cls.configs.get(config_name)


if __name__ == '__main__':
    pass
