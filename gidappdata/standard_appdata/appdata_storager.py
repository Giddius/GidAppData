# region [Imports]


from pprint import pformat
from enum import Enum, auto
import os
import sys
import shutil

from gidappdata.utility.functions import appendwriteit, linereadit, pathmaker, readit, writeit, writejson, loadjson

import gidlogger as glog

import appdirs

# endregion [Imports]

__updated__ = '2020-12-01 00:34:33'


# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]


# region [Constants]


# endregion [Constants]


class _AppDataFolder(Enum):
    AllFolder = auto()
    LogFolder = "log_folder"
    AppStorageFolder = "appstorage_folder"


class AppDataStorager:
    # region [ClassAttributes]

    AllFolder = _AppDataFolder.AllFolder
    LogFolder = _AppDataFolder.LogFolder
    AppStorageFolder = _AppDataFolder.AppStorageFolder

# endregion[ClassAttributes]
# region [Init]

    def __init__(self, author_name: str, app_name: str, dev: bool = False, redirect: str = None):
        # sourcery skip: simplify-boolean-comparison
        self.dev = dev
        self.author_name = author_name
        self.app_name = app_name
        self.redirect = redirect
        self.managed_folder = []
        self.operating_system = sys.platform
        self.appstorage_folder = None if self.dev is False else self.redirect
        self.log_folder = None if self.dev is False else pathmaker(self.redirect, 'Logs')
        if self.dev is False:
            self.setup_app_storage_base()

# endregion[Init]
# region [Properties]

    @property
    def folder(self):
        _out = {}
        for dirname, dirlist, _ in os.walk(self.appstorage_folder):
            for _dir in dirlist:
                _out[_dir] = pathmaker(dirname, _dir)
        return _out

    @property
    def files(self):
        _out = {}
        for dirname, _, filelist in os.walk(self.appstorage_folder):
            for _file in filelist:
                _out[_file] = pathmaker(dirname, _file)
        return _out

# endregion[Properties]

    def setup_app_storage_base(self):
        self.appstorage_folder = pathmaker(appdirs.user_data_dir(appauthor=self.author_name, appname=self.app_name, roaming=True))
        self.managed_folder.append(self.appstorage_folder)
        if os.path.isdir(self.appstorage_folder) is False:
            os.makedirs(self.appstorage_folder)

        self.log_folder = pathmaker(appdirs.user_log_dir(appauthor=self.author_name, appname=self.app_name, opinion=True))
        self.managed_folder.append(self.log_folder)
        if os.path.isdir(self.log_folder) is False:
            os.makedirs(self.log_folder)

    def add_folder(self, folder_name, parent_folder=None):
        if parent_folder is None:
            _folder = pathmaker(self.appstorage_folder, folder_name)
        else:
            _folder = pathmaker(self[parent_folder], folder_name)
        if os.path.isdir(_folder) is False:
            os.makedirs(_folder)

    def copy_file(self, source, target_filename, folder=None, overwrite=False):
        _path = self._get_filepath(target_filename, folder)
        if os.path.isfile(_path) is False or overwrite is True:
            shutil.copyfile(source, _path)

    def _get_filepath(self, filename, folder):
        if folder is not None:
            return pathmaker(self.folder[folder], filename)
        else:
            return pathmaker(self.appstorage_folder, filename)

    def _get_app_base_folder(self, in_folder):
        _folder = in_folder
        while os.path.basename(_folder) != self.author_name:
            _folder = _folder.rsplit('/', 1)[0]
        return _folder

    def clean(self, folder_to_clean: _AppDataFolder):
        _to_delete = []
        if folder_to_clean is self.AllFolder:
            _to_delete = self.managed_folder
        else:
            _to_delete.append(getattr(self, folder_to_clean.value))

        for _folder in _to_delete:
            _base_folder = self._get_app_base_folder(_folder)
            shutil.rmtree(_base_folder)
            log.info('deleted appdata folder "%s"', _base_folder)

# region [SpecialMethods]

    def __getitem__(self, key):
        _out = None
        if key in self.files:
            _out = self.files[key]
        elif key in self.folder:
            _out = self.folder[key]
        return _out

    def __str__(self):
        return self.appstorage_folder

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.author_name}, {self.app_name}, {str(self.dev)}, {str(self.redirect)})"

# endregion[SpecialMethods]
