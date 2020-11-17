# region [Imports]


import lzma
import os

import zipfile
import os
import base64

import gidlogger as glog
from gidconfig.standard import ConfigRental
from gidappdata.standard_appdata.appdata_storager import AppDataStorageUtility
from gidappdata.utility.functions import pathmaker

# endregion [Imports]

__updated__ = '2020-11-17 11:57:33'

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]

# region [Constants]


# endregion [Constants]


# region [Configs]

def unzip(root_dir, zip_file, overwrite: bool = False):
    # sourcery skip: simplify-boolean-comparison
    with zipfile.ZipFile(zip_file, 'r') as zipf:
        for item in zipf.namelist():
            _info = zipf.getinfo(item)
            if _info.is_dir() is True:
                if os.path.isdir(pathmaker(root_dir, item)) is False:
                    os.makedirs(pathmaker(root_dir, item))
                    log.debug("created folder '%s' because it did not exist", pathmaker(root_dir, item))
                else:
                    log.debug("folder '%s' already exists", pathmaker(root_dir, item))
            else:
                if os.path.isfile(pathmaker(root_dir, item)) is False:
                    zipf.extract(item, pathmaker(root_dir))
                    log.debug("extracted file '%s' because it didn't exist", pathmaker(root_dir, item))
                elif overwrite is True:
                    log.debug("file '%s' already exist and is overwriten because overwrite is 'True'", pathmaker(root_dir, item))
                    zipf.extract(item, pathmaker(root_dir))
                else:
                    log.debug("file '%s' is already existing and overwrite is 'False' so file was not extracted", pathmaker(root_dir, item))


# endregion [Configs]


# region [Factories]

class AppdataProvider:
    handler = None

    @classmethod
    def setup_appdata(cls, author_name: str, app_name: str, folderlist: list = None, filelist: list = None, configs: dict = None, dev=None, redirect=None):
        if cls.handler is None:
            cls.handler = AppDataStorageUtility(author_name, app_name, dev, redirect)
        if folderlist is not None:
            for _item in folderlist:
                if isinstance(_item, str):
                    cls.handler.add_folder(_item)
                elif isinstance(_item, tuple):
                    cls.handler.add_folder(_item[0], _item[1])
        if filelist is not None:
            for _item in filelist:
                if _item[0].endswith('.json'):
                    cls.handler.write_json(*_item)
                else:
                    cls.handler.write(*_item)

        if configs is not None:

            cls.handler.generate_configs(**configs)
        ConfigRental.set_appdata(cls.handler)
        return cls.handler

    @classmethod
    def archive_from_bin(cls, bin_data: str, name: str = 'user_data_archive', ext: str = 'zip', uses_base64: bool = False):
        _file = pathmaker(str(cls.handler), name + '.' + ext)
        with open(_file, 'wb') as archfile:
            if uses_base64 is True:
                bin_data = base64.b64decode(bin_data)
            archfile.write(bin_data)
        return _file

    @classmethod
    def unpack_archive(cls, in_archive_file, clean: bool):
        unzip(str(cls.handler), in_archive_file, False)
        if clean:
            os.remove(in_archive_file)

    @classmethod
    def setup_from_binarchive(cls, author_name: str, app_name: str, in_archive: str, uses_base64: bool, dev=None, redirect=None, clean=True):

        if cls.handler is None:
            log.info("appdata, does not exist, creating from scratch")
            cls.handler = AppDataStorageUtility(author_name, app_name, dev, redirect)
            _archive = cls.archive_from_bin(in_archive, uses_base64=uses_base64)
            cls.unpack_archive(_archive, clean=clean)
            ConfigRental.set_appdata(cls.handler)
        else:
            log.info("appdata, already existing so returning existing object")

        return cls.handler

    @classmethod
    def get_handler(cls):
        if cls.handler is not None:
            return cls.handler
        else:
            raise LookupError('AppDataStorage object has to be created first via "get_handler" of this factory')

# endregion [Factories]


# region [Main_Exec]
if __name__ == '__main__':
    pass


# endregion [Main_Exec]
