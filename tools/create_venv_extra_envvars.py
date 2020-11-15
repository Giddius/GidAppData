import os
import sys

os.chdir(sys.argv[1])
PROJECT_NAME = sys.argv[2]
REL_ACTIVATE_SCRIPT_PATH = '../.venv/Scripts/activate.bat'
REPLACEMENT = r"""@echo off

set FILEFOLDER=%~dp0

pushd %FILEFOLDER%
rem ----------------------------------------------------------------
cd ..\..\tools
echo ##################### setting vars from %cd%\_project_meta.env
for /f %%i in (_project_meta.env) do set %%i && echo %%i
rem ----------------------------------------------------------------
popd
"""


def create_project_meta_env_file():
    _workspacedirbatch = os.getcwd()
    _toplevelmodule = os.path.join(_workspacedirbatch, PROJECT_NAME)
    _main_script_file = os.path.join(_toplevelmodule, '__main__.py')
    with open("_project_meta.env", 'w') as envfile:
        envfile.write(f'WORKSPACEDIR={_workspacedirbatch}\n')
        envfile.write(f'TOPLEVELMODULE={_toplevelmodule}\n')
        envfile.write(f'MAIN_SCRIPT_FILE={_main_script_file}\n')


def modify_activate_bat():

    with open(REL_ACTIVATE_SCRIPT_PATH, 'r') as origbat:
        _content = origbat.read()
    if REPLACEMENT not in _content:
        _new_content = _content.replace(r'@echo off', REPLACEMENT)
        with open(REL_ACTIVATE_SCRIPT_PATH, 'w') as newbat:
            newbat.write(_new_content)


if __name__ == '__main__':
    create_project_meta_env_file()
    modify_activate_bat()
