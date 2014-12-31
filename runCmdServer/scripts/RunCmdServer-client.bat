@echo off
cd ..\
call ..\etc\set-env-windows.bat

set PROGRAM=.\RunCmdServer\main.py
set OPTIONS=client %*

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
rem if not defined OPTIONS set OPTIONS=--help
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
rem cd %~dp0
echo %PROGRAM% %OPTIONS%
call %PROGRAM% %OPTIONS%
set EXIT_CODE=%errorlevel%
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
rem if errorlevel 1 (
rem     echo Failure Reason Given is %errorlevel%
rem     exit /b %errorlevel%
rem )
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
rem timeout /t 10 /nobreak
exit /b %EXIT_CODE%