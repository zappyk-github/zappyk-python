@echo off
call winenv.bat
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

call TurnReporTxt2Csv\main.py %*

exit /b %errorlevel%