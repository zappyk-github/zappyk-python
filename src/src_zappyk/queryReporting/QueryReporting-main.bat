@echo off
call winenv.bat
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

call QueryReporting\main.py %*

exit /b %errorlevel%