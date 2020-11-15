@rem taskarg: ${file}
@Echo off
set OLDHOME_FOLDER=%~dp0
cd %OLDHOME_FOLDER%
call ..\.venv\Scripts\activate.bat

call memory_profiling_time.cmd %MAIN_SCRIPT_FILE%
rem call memory_profiling_time.cmd D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\PyQt_Socius\pyqtsocius\main_window.py
