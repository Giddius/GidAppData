# region [Imports]


# * Standard Library Imports -->
import os
import json
import shutil
import pickle
# * Gid Imports -->
import gidlogger as glog
from functools import partial
import base64
# import numpy as np
# endregion[Imports]


# region [Logging]

log = glog.logging.getLogger('gidappdata')
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


def create_folder(in_folder, overwrite=False):
    if os.path.isdir(in_folder) is True:
        if overwrite is True:
            shutil.rmtree(in_folder)
        elif overwrite is False:
            log.debug('folder "%s" already exists', in_folder)
    if os.path.isdir(in_folder) is False:
        os.makedirs(in_folder)
        log.debug('created folder "%s"', in_folder)


def create_file(in_file, file_content, overwrite=False):
    if os.path.isfile(in_file) is False or overwrite is True:
        if os.path.splitext(in_file)[1] == '.json':
            writejson(file_content, in_file, sort_keys=False, indent=2)
        else:
            _write_mode = 'wb' if isinstance(file_content, bytes) else 'w'
            content = file_content if isinstance(file_content, bytes) else str(file_content)
            with open(in_file, _write_mode) as outfile:
                outfile.write(content)
        log.debug('created file "%s"', in_file)
    else:
        log.debug('file "%s" already exists', in_file)


def pathmaker(first_segment, *in_path_segments, rev=False):
    """
    Normalizes input path or path fragments, replaces '\\\\' with '/' and combines fragments.

    Parameters
    ----------
    first_segment : str
        first path segment, if it is 'cwd' gets replaced by 'os.getcwd()'
    rev : bool, optional
        If 'True' reverts path back to Windows default, by default None

    Returns
    -------
    str
        New path from segments and normalized.
    """
    _first = os.getcwd() if first_segment == 'cwd' else first_segment
    _path = os.path.join(_first, *in_path_segments)
    _path = _path.replace('\\\\', '/')
    _path = _path.replace('\\', '/')
    if rev is True:
        _path = _path.replace('/', '\\')

    return _path.strip()


def writebin(in_file, in_data):
    """
    Writes a string to binary.

    Parameters
    ----------
    in_file : str
        The target file path
    in_data : str
        The data to write
    """
    with open(in_file, 'wb') as outbinfile:
        outbinfile.write(in_data)


def writeit(in_file, in_data, append=False, in_encoding='utf-8', in_errors=None):
    """
    Writes to a file.

    Parameters
    ----------
    in_file : str
        The target file path
    in_data : str
        The data to write
    append : bool, optional
        If True appends the data to the file, by default False
    in_encoding : str, optional
        Sets the encoding, by default 'utf-8'
    """
    _write_type = 'w' if append is False else 'a'
    with open(in_file, _write_type, encoding=in_encoding, errors=in_errors,) as _wfile:
        _wfile.write(in_data)


def appendwriteit(in_file, in_data, in_encoding='utf-8'):
    with open(in_file, 'a', encoding=in_encoding) as appendwrite_file:
        appendwrite_file.write(in_data)


def readbin(in_file):
    """
    Reads a binary file.

    Parameters
    ----------
    in_file : str
        A file path

    Returns
    -------
    str
        the decoded file as string
    """
    with open(pathmaker(in_file), 'rb') as binaryfile:
        return binaryfile.read()


def readit(in_file, per_lines=False, in_encoding='utf-8', in_errors='replace'):
    """
    Reads a file.

    Parameters
    ----------
    in_file : str
        A file path
    per_lines : bool, optional
        If True, returns a list of all lines, by default False
    in_encoding : str, optional
        Sets the encoding, by default 'utf-8'
    in_errors : str, optional
        How to handle encoding errors, either 'strict' or 'ignore', by default 'strict'

    Returns
    -------
    str/list
        the read in file as string or list (if per_lines is True)
    """
    with open(in_file, 'r', encoding=in_encoding, errors=in_errors) as _rfile:
        _content = _rfile.read()
    if per_lines is True:
        _content = _content.splitlines()

    return _content


def linereadit(in_file, in_encoding='utf-8', in_errors='strict'):
    with open(in_file, 'r', encoding=in_encoding, errors=in_errors) as lineread_file:
        _out = lineread_file.read().splitlines()
    return _out


def clearit(in_file):
    """
    Deletes the contents of a file.

    Parameters
    ----------
    in_file : str
        The target file path
    """
    with open(in_file, 'w') as file_to_clear:
        file_to_clear.write('')
    log.debug(f"contents of file '{in_file}' was cleared")


def loadjson(in_file):
    with open(in_file, 'r') as jsonfile:
        _out = json.load(jsonfile)
    return _out


def writejson(in_object, in_file, sort_keys=True, indent=0):
    with open(in_file, 'w') as jsonoutfile:
        json.dump(in_object, jsonoutfile, sort_keys=sort_keys, indent=indent)


def pickleit(obj, in_path):
    """
    saves an object as pickle file.

    Parameters
    ----------
    obj : object
        the object to save
    in_name : str
        the name to use for the pickled file
    in_dir : str
        the path to the directory to use
    """
    with open(pathmaker(in_path), 'wb') as filetopickle:
        log.debug(f"saved object [{str(obj)}] as pickle file [{in_path}]")
        pickle.dump(obj, filetopickle, pickle.HIGHEST_PROTOCOL)


def get_pickled(in_path):
    """
    loads a pickled file.

    Parameters
    ----------
    in_path : str
        the file path to the pickle file

    Returns
    -------
    object
        the pickled object
    """
    with open(pathmaker(in_path), 'rb') as pickletoretrieve:
        log.debug(f"loaded pickle file [{in_path}]")
        return pickle.load(pickletoretrieve)


# def np_readbin(in_path):
#     return np.frombuffer(readbin(in_path))


def read_file(in_file):
    _read_strategies = {'.txt': readit,
                        '.ini': readit,
                        '.json': loadjson,
                        '.jpg': readbin,
                        '.png': readbin,
                        '.tga': readbin,
                        '.ico': readbin,
                        '.pkl': readbin,
                        '.py': readit,
                        '.cmd': readit,
                        '.exe': np_readbin,
                        '.env': readit,
                        '.log': readit,
                        '.errors': readit,
                        '.bat': readit,
                        '.md': readit}
    _ext = os.path.splitext(in_file)[1]
    return _read_strategies.get(_ext, readbin)(in_file)


def to_attr_name(in_name):

    replace_dict = {' ': '_',
                    '-': '_',
                    '.': '__',
                    '/': '_',
                    '\\': '_',
                    '*': '',
                    '{': '_',
                    '}': '_',
                    '[': '_',
                    ']': '_',
                    '(': '_',
                    ')': '_',
                    '>': '_',
                    '<': '_',
                    '#': '_',
                    '+': '_',
                    '&': '_',
                    '$': '_',
                    "'": '',
                    '"': '', }

    attr_name = in_name.strip()

    for to_replace, replacement in replace_dict.items():
        if to_replace in attr_name:
            for amount in reversed(range(1, 10)):
                if to_replace * amount in attr_name:

                    attr_name = attr_name.lstrip(to_replace * amount).rstrip(to_replace * amount).replace(to_replace * amount, replacement)
    return attr_name.casefold()


def filename_to_attr_name(in_file, keep_ext=False):
    attr_name = in_file
    if os.path.sep in attr_name or '/' in attr_name:
        attr_name = os.path.basename(attr_name)
    if keep_ext is False:
        attr_name = os.path.splitext(attr_name)[0]
    return to_attr_name(attr_name)
# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
