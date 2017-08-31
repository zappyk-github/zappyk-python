@echo off
call set-env-windows.bat
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

call MergeTwoCsv2One\main.py %*
rem call C:\Python34\python.exe MergeTwoCsv2One\main.py %*

exit /b %errorlevel%