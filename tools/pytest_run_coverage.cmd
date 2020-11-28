@echo off
setlocal enableextensions
set OLDHOME_FOLDER=%~dp0
set INPATH=%~dp1
set INFILE=%~nx1
set INFILEBASE=%~n1

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
set TIMEBLOCK=%_years%-%_months%-%_days%_%_hours%-%_minutes%-%_seconds%
Echo ################# Current time is %TIMEBLOCK%
call ..\.venv\Scripts\activate.bat

set COVERAGE_REPORT_FOLDER="%WORKSPACEDIR%\pytest_coverage"
CD %WORKSPACEDIR%
echo %COVERAGE_REPORT_FOLDER%
RD /S /Q %COVERAGE_REPORT_FOLDER%
mkdir %COVERAGE_REPORT_FOLDER%



rem ECHO standard

rem call pytest --cov=%PROJECT_NAME% .\tests -v



ECHO html report

call pytest .\tests -v --cov=%PROJECT_NAME% --cov-report html:"%COVERAGE_REPORT_FOLDER%\%PROJECT_NAME%_coverage_html"



rem ECHO xml report

rem call pytest tests\ -v --cov=%PROJECT_NAME% --cov-report xml:"%COVERAGE_REPORT_FOLDER%\%PROJECT_NAME%_coverage.xml"



rem ECHO annotated source code report

rem call pytest .\tests -v --cov=%PROJECT_NAME% --cov-report annotate:"%COVERAGE_REPORT_FOLDER%\%PROJECT_NAME%_coverage"