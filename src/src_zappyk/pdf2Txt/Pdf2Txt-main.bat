@echo off
call winenv.bat
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

call Pdf2Txt\main.py %*

exit /b %errorlevel%