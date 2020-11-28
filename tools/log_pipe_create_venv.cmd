@echo off
SETLOCAL EnableDelayedExpansion

set OLDHOME_FOLDER=%~dp0
set LOG_FOLDER=%OLDHOME_FOLDER%create_venv_logs

RD /S /Q "%LOG_FOLDER%"

mkdir %LOG_FOLDER%

pushd %OLDHOME_FOLDER%

call create_venv.cmd 2> "%LOG_FOLDER%\create_venv.errors" | TEE "%LOG_FOLDER%\create_venv.log"
call create_venv.cmd > "%LOG_FOLDER%\create_venv_overall.log" 2>&1