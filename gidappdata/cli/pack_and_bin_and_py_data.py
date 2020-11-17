# taskarg: ${fileDirname}

import os
import json
import shutil
import base64
from dotenv import load_dotenv
from gidappdata.utility.functions import pathmaker, writebin, writeit, writejson, readbin, readit

import gidlogger as glog

log = glog.main_logger_stdout('debug')
log.info(glog.NEWRUN())


def as_kb(in_size: int):
    conv = 1024
    return in_size / conv


def as_mb(in_size: int):
    conv = 1024 * 1024
    return in_size / conv


def as_gb(in_size: int):
    conv = 1024 * 1024 * 1024
    return in_size / conv


def find_files():
    # sourcery skip: inline-immediately-returned-variable, list-comprehension
    _out = []
    for _file in os.scandir():
        if not _file.name.endswith('.py') and not os.path.isdir(_file.path):
            _out.append(_file.path)
    return _out


def pack_data():
    _folder = pathmaker('cwd', 'data_pack')

    a = shutil.make_archive(pathmaker('cwd', 'base_userdata_archive'), format='zip', root_dir=_folder, logger=log)
    return pathmaker(a)


def convert_to_bin(archive, use_base64=False):
    with open(archive, 'rb') as binf:
        _content = binf.read()
    if use_base64 is True:
        _content = base64.b64encode(_content)
    return _content


def write_to_pyfile(**kwargs):
    with open('bin_data.py', 'w') as _file:
        for key, value in kwargs.items():
            _content = value
            _file.write(f'{key} = {_content}\n\n')
    return pathmaker(os.path.abspath('bin_data.py'))


def write_construction_info(uses_base64=False):
    with open('construction_info.py', 'w') as confo_file:
        _appname = "PyQt_Socius"  # input('Name of the Application: ')
        _author = "BrocaProgs"  # input('Author or Organization [Default=BrocaProgs]: ')
        _author = _author if _author != '' else 'BrocaProgs'
        confo_file.write(f"USES_BASE64 = {str(uses_base64)}\n")
        confo_file.write("REDIRECT = None\n")
        confo_file.write(f"AUTHOR = '{str(_author)}'\n")
        confo_file.write(f"APPNAME = '{str(_appname)}'\n")


def generate_user_data_binfile(use_base64):
    this_file_dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(pathmaker(this_file_dir))
    _archive = pack_data()
    size = os.stat(_archive).st_size
    if as_gb(size) > 1:
        log_size = round(as_gb(size), 3)
        log_size_type = 'gb'
    elif as_mb(size) > 1:
        log_size = round(as_mb(size), 3)
        log_size_type = 'mb'
    elif as_kb(size) > 1:
        log_size = round(as_kb(size), 1)
        log_size_type = 'kb'
    else:
        log_size = size
        log_size_type = 'b'

    log.info('data was archived with size of %s%s', log_size, log_size_type)
    log.info('converted archive to bin')
    _py_file = write_to_pyfile(bin_archive_data=convert_to_bin(_archive, use_base64))
    write_construction_info(use_base64)
    log.info('bin data was written to python file: %s', _py_file)
    log.info("starting cleanup!")
    os.remove(_archive)
    log.info("cleanup done")
    log.info('---done---')


if __name__ == '__main__':
    pass
