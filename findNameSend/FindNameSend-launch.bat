@echo off

set PROGRAM=.\FindNameSend\FindNameSend.exe
set OPTIONS=%*

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
rem if not defined OPTIONS set OPTIONS=
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
cd %~dp0
echo %PROGRAM% -v %OPTIONS%
call %PROGRAM% -v %OPTIONS%
set EXIT_CODE=%errorlevel%
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
timeout /t 10 /nobreak
exit /b %EXIT_CODE%