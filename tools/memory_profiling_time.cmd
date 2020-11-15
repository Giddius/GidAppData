@rem taskarg: ${file}
@Echo off
call pssuspend64 Dropbox
set OLDHOME_FOLDER=%~dp0

pushd %OLDHOME_FOLDER%

call ..\.venv\Scripts\activate.bat

rem ---------------------------------------------------
set _date=%DATE:/=-%
set _time=%TIME::=%
set _time=%_time: =0%
rem ---------------------------------------------------
rem ---------------------------------------------------
set _decades=%_date:~-2%
set _years=%_date:~-4%
set _months=%_date:~3,2%
set _days=%_date:~0,2%
rem ---------------------------------------------------
set _hours=%_time:~0,2%
set _minutes=%_time:~2,2%
set _seconds=%_time:~4,2%
rem ---------------------------------------------------



set INPATH=%~dp1

set INFILE=%~nx1

set INFILEBASE=%~n1

pushd %INPATH%

mkdir %WORKSPACEDIR%\misc\memory_profiling
echo %WORKSPACEDIR%\misc\memory_profiling
rem call pip install -q memory-profiler
rem call pip install -q matplotlib

mprof clean
mprof run --include-children %~1
mprof plot --flame
mprof plot -o %WORKSPACEDIR%\misc\memory_profiling\[%_years%-%_months%-%_days%_%_hours%-%_minutes%-%_seconds%]_mem_%INFILEBASE%.svg
mprof clean

rem call pip uninstall -q -y memory-profiler
rem call pip uninstall -q -y psutil
rem call pip uninstall -q -y matplotlib
rem call pip uninstall -q -y certifi
rem call pip uninstall -q -y cycler
rem call pip uninstall -q -y kiwisolver
rem call pip uninstall -q -y numpy
rem call pip uninstall -q -y pillow
rem call pip uninstall -q -y pyparsing
rem call pip uninstall -q -y python-dateutil
rem call pip uninstall -q -y six

