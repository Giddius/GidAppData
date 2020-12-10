# taskarg: ${fileDirname}

import os
import json
import shutil
import base64
from dotenv import load_dotenv
from gidappdata.utility.functions import pathmaker, writebin, writeit, writejson, readbin, readit
from time import sleep, time
import gidlogger as glog
import click

log = glog.main_logger_stdout('debug')
log.info(glog.NEWRUN())


def as_kb(in_size: int) -> int:
    """
    Converter functions to convert the size in bytes to kilobytes.
    """
    conv = 1024
    return in_size // conv


def as_mb(in_size: int) -> int:
    """
    Converter functions to convert the size in bytes to megabytes.
    """
    conv = 1024 * 1024
    return in_size // conv


def as_gb(in_size: int) -> int:
    """
    Converter functions to convert the size in bytes to gigabytes.
    """
    conv = 1024 * 1024 * 1024
    return in_size // conv


def find_files():
    # sourcery skip: inline-immediately-returned-variable, list-comprehension
    _out = []
    for _file in os.scandir():
        if not _file.name.endswith('.py') and not os.path.isdir(_file.path):
            _out.append(_file.path)
    return _out


def pack_data(in_path):
    _folder = pathmaker(in_path, 'data_pack')
    archive_path = pathmaker(shutil.make_archive(pathmaker(in_path, 'base_userdata_archive'), format='zip', root_dir=_folder, logger=log))
    log.info('data was archived with size of %s%s', *convert_file_size(archive_path))
    return archive_path


def convert_to_bin(archive, use_base64):
    with open(archive, 'rb') as binf:
        _content = binf.read()
    if use_base64 is True:
        _content = base64.b64encode(_content)
    return _content


def write_to_pyfile(in_path, **kwargs):
    _path = pathmaker(in_path, 'bin_data.py')
    with open(_path, 'w') as _file:
        for key, value in kwargs.items():
            _content = value
            _file.write(f'{key.strip()} = {_content.strip()}\n\n')
    log.info("bin data was written to python file: '%s'", _path)
    return _path


def write_construction_info(in_path, appname, author='BrocaProgs', uses_base64=True):
    _path = pathmaker(in_path, 'construction_info.env')
    with open(_path, 'w') as confo_file:
        confo_file.write(f"USES_BASE64 = {str(uses_base64)}\n")
        confo_file.write(f"AUTHOR_NAME = {str(author)}\n")
        confo_file.write(f"APP_NAME = '{str(appname)}'\n")
    log.info("construction info file was written to python file: '%s'", _path)
    return _path


def convert_file_size(in_file_path):
    size = os.stat(in_file_path).st_size
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
    return log_size, log_size_type


def post_clean_zip_file(file_path):
    log.info("starting cleanup of zip file")
    os.remove(file_path)
    if os.path.isfile(file_path) is False:
        log.info("cleanup of zip file successfully done")
    else:
        log.critical("was not able to remove zip file '%s'", file_path)


def read_const_file(const_file):
    _out = []
    with open(const_file, 'r') as c_file:
        content = c_file.read().splitlines()
    for line in content:
        if line != '' and ' = ' in line:
            _name, _value = line.split(' = ')
            _out.append((_name, _value))
    return _out


def post_checks(bin_py_file, const_file):

    log.info('checking existance of binary pyfile:')

    if os.path.exists(bin_py_file) is True:
        log.info("binary pyfile does exist at '%s'", bin_py_file)
        log.info("--> size: %s%s", *convert_file_size(bin_py_file))
    else:
        log.critical("binary pyfile does NOT exist! should be at '%s'", bin_py_file)

    log.info('checking existance of construction info file:')
    if os.path.exists(const_file) is True:
        log.info("construction info file does exist at '%s'", const_file)
        log.info("set variables found in construction info file: ")
        log.info("-----------------------")
        for name, value in read_const_file(const_file):
            log.info("%s = '%s'", name, value)
            log.info("-----------------------")
    else:
        log.critical("construction info file does NOT exist! should be at '%s'", const_file)


@click.command()
@click.argument('init_userdata_dir')
@click.option('-n', '--appname', default=os.getenv('PROJECT_NAME'))
@click.option('-a', '--author', default='BrocaProgs')
@click.option('--use-base64/--dont-base64', '-64/-no64', default=True)
@click.option('--clean-zip-file/--keep-zip-file', '-cz/-kz', default=True)
def generate_user_data_binfile(init_userdata_dir, appname, author, use_base64, clean_zip_file):
    start_time = time()
    if appname is None or appname == '':
        print('Unable to obtain "appname" from env variable, please set "PROJECT_NAME" env variable or provide appname as cli-option')
        return
    appname = appname.replace(' ', '-').replace('_', '-').title()
    log.info("Starting conversion for data_pack in '%s'")
    _archive = pack_data(init_userdata_dir)

    log.info('converted archive to bin')

    _py_file = write_to_pyfile(init_userdata_dir, bin_archive_data=convert_to_bin(_archive, use_base64))

    _const_file = write_construction_info(in_path=init_userdata_dir, appname=appname, author=author, uses_base64=use_base64)

    if clean_zip_file is True:
        post_clean_zip_file(_archive)

    log.info('running post-checks')
    post_checks(_py_file, _const_file)

    log.debug('overall time taken: %s seconds', str(round(time() - start_time, 3)))
    log.info('---done---')


if __name__ == '__main__':
    # THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
    # _archive = pack_data(r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\GidAppData\gidappdata\data\skeletons\prebuilt_standard\basic")
    # _py_file = write_to_pyfile(THIS_FILE_DIR, bin_archive_data=convert_to_bin(_archive, True))
    pass
