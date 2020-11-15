@echo off
SETLOCAL EnableDelayedExpansion

set OLDHOME_FOLDER=%~dp0
set LOG_FOLDER=%OLDHOME_FOLDER%create_venv_logs

pushd %OLDHOME_FOLDER%
mkdir %LOG_FOLDER%
del /S /Q "%LOG_FOLDER%"

call create_venv.cmd 2> "%LOG_FOLDER%\create_venv.errors" | TEE "%LOG_FOLDER%\create_venv.log"
