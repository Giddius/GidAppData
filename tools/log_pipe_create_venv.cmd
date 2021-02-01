@echo off
SETLOCAL EnableDelayedExpansion

set OLDHOME_FOLDER=%~dp0
set LOG_FOLDER=%OLDHOME_FOLDER%create_venv_logs

RD /S /Q "%LOG_FOLDER%"

mkdir %LOG_FOLDER%

pushd %OLDHOME_FOLDER%


rem ++++++++++++++++++++++++++++++++++++++++++++++++
rem &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

SET PROJECT_NAME=GIDAPPDATA

rem -------------------------------------------------

SET PROJECT_AUTHOR=GIDDIUS

rem &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
rem ++++++++++++++++++++++++++++++++++++++++++++++++

call create_venv.cmd %PROJECT_NAME% %PROJECT_AUTHOR% 2> "%LOG_FOLDER%\create_venv.errors" | TEE "%LOG_FOLDER%\create_venv.log"
if %ERRORLEVEL% == 0 (
    @echo off
    echo ErrorLevel is zero
    echo.
    echo No need to run again with combined log!!
) else (
   @echo off
   echo ErrorLevel is > 1
   echo.
   echo Running again with combined log to get error location
   echo.
   echo.
   call create_venv.cmd %PROJECT_NAME% %PROJECT_AUTHOR% > "%LOG_FOLDER%\create_venv_overall.log" 2>&1
)


