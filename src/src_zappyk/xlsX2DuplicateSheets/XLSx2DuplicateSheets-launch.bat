@echo off

rem VERSION=0.1

set PROGRAM=.\XLSx2DuplicateSheets-%VERSION%\XLSx2DuplicateSheets.exe
set PPARAMS=
set OPTIONS=%*

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
rem if not defined OPTIONS set OPTIONS=
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
set dir=%cd%
cd %~dp0
echo %PROGRAM% %PPARAMS% %OPTIONS%
call %PROGRAM% %PPARAMS% %OPTIONS%
set EXIT_CODE=%errorlevel%
cd %dir%
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
timeout /t 10 /nobreak
exit /b %EXIT_CODE%
