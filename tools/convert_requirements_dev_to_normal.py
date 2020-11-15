# * Standard Library Imports -->
import os
import re
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
REQU_DEV_FILE = "../requirements_dev.txt"
REQU_NORM_FILE = "../requirements.txt"
PYPROJECTTOML = "../pyproject.toml"
old_cwd = os.getcwd()
REQUIRES_REGEX = re.compile(r"(?<=\[tool\.flit\.metadata\]\n)(?:.*?)(requires = \[.*?\])", re.DOTALL)


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


def readit(in_file, per_lines=False, in_encoding='utf-8', in_errors=None):
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


def convert(use_requirements_txt: bool):
    os.chdir(THIS_FILE_DIR)
    _out_list = []
    dev_lines = readit(REQU_DEV_FILE, per_lines=True)
    for line in dev_lines:
        if line != '' and 'git+' not in line and '#' not in line:
            _out_list.append(line.strip())
    if use_requirements_txt is True:
        writeit(REQU_NORM_FILE, '\n'.join(_out_list))
    else:
        convert_and_replace_to_toml(_out_list)
    os.chdir(old_cwd)


def convert_and_replace_to_toml(in_list):
    toml_content = readit(PYPROJECTTOML)
    _requires_part = REQUIRES_REGEX.search(toml_content).group(1)
    _new_requires = "requires = [\n"
    for line in in_list:
        line = line.split('==')[0]
        line = f'\t"{line}",\n'
        _new_requires += line
    _new_requires += ']\n'
    _new_content = toml_content.replace(_requires_part, _new_requires)
    writeit(PYPROJECTTOML, _new_content)


if __name__ == '__main__':
    convert(True)
