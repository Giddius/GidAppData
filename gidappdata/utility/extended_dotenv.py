import os
from dotenv import load_dotenv, find_dotenv


def _is_appdata_object(in_object):
    try:
        _name = in_object.__class__.__name__
        return _name == 'AppDataStorager'
    except AttributeError:
        return False


def find_dotenv_everywhere(filename: str = '.env', start_dir=None, lower_folder: bool = True, upper_folder=True, raise_error_if_not_found: bool = False):
    start_dir = os.getcwd() if start_dir is None else start_dir
    start_dir = str(start_dir) if _is_appdata_object(start_dir) is True else start_dir
    dotfile = None
    if lower_folder:
        for dirname, _, filelist in os.walk(start_dir):
            for file in filelist:
                if file == filename:
                    print()
                    dotfile = os.path.join(dirname, file)
    if dotfile is None and upper_folder:
        _old_dir = os.getcwd()
        os.chdir(start_dir)
        dotfile = find_dotenv(filename, raise_error_if_not_found, usecwd=True)

        os.chdir(_old_dir)
    if dotfile is None:
        dotfile = ''
    return dotfile
