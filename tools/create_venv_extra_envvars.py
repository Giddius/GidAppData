# * Standard Library Imports -->
# * Standard Library Imports ---------------------------------------------------------------------------->
import os
import sys

os.chdir(sys.argv[1])
PROJECT_NAME = sys.argv[2].lower()
PROJECT_AUTHOR = sys.argv[3].lower()
REL_ACTIVATE_SCRIPT_PATH = './.venv/Scripts/activate.bat'
REPLACEMENT = r"""@echo off

set FILEFOLDER=%~dp0

pushd %FILEFOLDER%
rem ----------------------------------------------------------------
cd ..\..\tools
rem ##################### setting vars from %cd%\_project_devmeta.env
for /f %%i in (_project_devmeta.env) do set %%i
rem ----------------------------------------------------------------
popd
"""


def create_project_devmeta_env_file():
    _workspacedirbatch = os.getcwd()
    _toplevelmodule = os.path.join(_workspacedirbatch, PROJECT_NAME)
    _main_script_file = os.path.join(_toplevelmodule, '__main__.py')
    with open(r".\tools\_project_devmeta.env", 'w') as envfile:
        envfile.write(f'WORKSPACEDIR={_workspacedirbatch}\n')
        envfile.write(f'TOPLEVELMODULE={_toplevelmodule}\n')
        envfile.write(f'MAIN_SCRIPT_FILE={_main_script_file}\n')
        envfile.write(f'PROJECT_NAME={PROJECT_NAME}\n')
        envfile.write(f'PROJECT_AUTHOR={PROJECT_AUTHOR}\n')
        envfile.write('IS_DEV=true')


def create_project_meta_env_file():
    _workspacedirbatch = os.getcwd()
    _toplevelmodule = os.path.join(_workspacedirbatch, PROJECT_NAME)
    _main_script_file = os.path.join(_toplevelmodule, '__main__.py')
    with open(os.path.join(_toplevelmodule, "project_meta_data.env"), 'w') as envfile:
        envfile.write(f'PROJECT_NAME={PROJECT_NAME}\n')
        envfile.write(f'PROJECT_AUTHOR={PROJECT_AUTHOR}\n')


def modify_activate_bat():

    with open(REL_ACTIVATE_SCRIPT_PATH, 'r') as origbat:
        _content = origbat.read()
    if REPLACEMENT not in _content:
        _new_content = _content.replace(r'@echo off', REPLACEMENT)
        with open(REL_ACTIVATE_SCRIPT_PATH, 'w') as newbat:
            newbat.write(_new_content)


if __name__ == '__main__':
    create_project_devmeta_env_file()
    # create_project_meta_env_file()
    modify_activate_bat()
