@echo off
call winenv.bat
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

call MergeTwoCsv2One\main.py %*

exit /b %errorlevel%
