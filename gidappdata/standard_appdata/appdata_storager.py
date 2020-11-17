# region [Imports]


from pprint import pformat

import os
import sys


from gidappdata.utility.functions import appendwriteit, linereadit, pathmaker, readit, writeit, writejson, loadjson

import gidlogger as glog

import appdirs

# endregion [Imports]

__updated__ = '2020-11-17 11:37:56'


# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]


# region [Constants]


# endregion [Constants]


# region [Misc]


# endregion [Misc]


# region [Global_Functions]


# endregion [Global_Functions]


# region [Class_1]

# endregion [Class_1]


# region [Class_2]

class AppDataStorager:
    def __init__(self, author_name: str, app_name: str, dev: str = None, redirect=None):
        # sourcery skip: simplify-boolean-comparison
        self.dev = dev
        self.author_name = author_name
        self.app_name = app_name
        self.redirect = redirect
        self._manipulate_enviroment(redirect)
        self.operating_system = sys.platform
        self.general_data_folder = None if self.dev is None else os.path.split(self.dev)[0]
        self.appstorage_folder = None if self.dev is None else self.dev
        self.log_folder = None if self.dev is None else pathmaker(self.dev, 'Logs')
        if self.dev is None:
            self.setup_app_storage_base()
            self.find_general_data_folder()

    def _manipulate_enviroment(self, redirect):
        if redirect is not None:
            os.environ['APPDATA'] = redirect

    def setup_app_storage_base(self):
        self.find_general_data_folder()
        self.appstorage_folder = pathmaker(appdirs.user_data_dir(appauthor=self.author_name, appname=self.app_name, roaming=True))
        if os.path.isdir(self.appstorage_folder) is False:
            os.makedirs(self.appstorage_folder)
        self.log_folder = pathmaker(appdirs.user_log_dir(appauthor=self.author_name, appname=self.app_name, opinion=True))
        if os.path.isdir(self.log_folder) is False:
            os.makedirs(self.log_folder)

    def find_general_data_folder(self):
        if self.redirect is not None:
            self.general_data_folder = pathmaker(self.redirect)
        else:
            self.general_data_folder = pathmaker(appdirs.user_data_dir(roaming=True))

    def add_folder(self, folder_name, parent_folder=None):
        if parent_folder is None:
            _folder = pathmaker(self.appstorage_folder, folder_name)
        else:
            _folder = pathmaker(self.appstorage_folder, parent_folder, folder_name)
        if os.path.isdir(_folder) is False:
            os.makedirs(_folder)

    def write(self, filename, filecontent, folder=None, append=False, overwrite=False):
        _path = self._get_filepath(filename, folder)
        if append is False:
            if os.path.isfile(_path) is False or overwrite is True:
                writeit(_path, filecontent)
        elif append is True:
            appendwriteit(_path, filecontent)

    def read(self, filename, folder=None, perline=False):
        _path = self._get_filepath(filename, folder)
        return linereadit(_path) if perline is True else readit(_path)

    def write_json(self, filename, data, folder=None, overwrite=False, **kwargs):
        _path = self._get_filepath(filename, folder)
        if os.path.isfile(_path) is False or overwrite is True:
            writejson(data, _path, **kwargs)

    def load_json(self, filename, folder=None):
        _path = self._get_filepath(filename, folder)
        return loadjson(_path)

    def copy_file(self, source, target_filename, folder=None, overwrite=False):
        _path = self._get_filepath(target_filename, folder)
        if os.path.isfile(_path) is False or overwrite is True:
            shutil.copyfile(source, _path)

    def _get_filepath(self, filename, folder):
        if folder is not None:
            _path = pathmaker(self.folder[folder], filename)
        else:
            _path = pathmaker(self.appstorage_folder, filename)
        return _path

    def __getitem__(self, key):
        _out = None
        if key in self.files:
            _out = self.files[key]
        elif key in self.folder:
            _out = self.folder[key]
        return _out

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

    def __str__(self):
        return self.appstorage_folder

# endregion [Class_2]


# region [Main_Exec]
if __name__ == '__main__':
    pass

# endregion [Main_Exec]
