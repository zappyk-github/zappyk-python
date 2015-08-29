@echo off

set VERSION=0.1
set VERSION=0.2
set VERSION=0.2-1

set PROGRAM=.\CheckDiskSpace-%VERSION%\CheckDiskSpace.exe
set PPARAMS=
set OPTIONS=%*

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
rem if not defined OPTIONS set OPTIONS=
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
cd %~dp0
echo %PROGRAM% %PPARAMS% %OPTIONS%
call %PROGRAM% %PPARAMS% %OPTIONS%
set EXIT_CODE=%errorlevel%
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
timeout /t 10 /nobreak
exit /b %EXIT_CODE%
