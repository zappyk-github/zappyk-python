@echo off

set PATH_BUILD=build
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
set VERS_PROGRAM=0.1
set NAME_EXE_BAT=XLSx2RewriteOut-launch.bat
set PATH_PROGRAM=XLSx2RewriteOut-%VERS_PROGRAM%
set NAME_PAK_ZIP=%PATH_PROGRAM%-win32
set PATH_COMPILE=exe.win32-32bit_WindowsPE-python-3.3.5
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
set ZIP="C:\Program Files (x86)\WinZip\WINZIP32.EXE"

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

cd "%PATH_BUILD%\%PATH_PROGRAM%"
md "%NAME_PAK_ZIP%"

xcopy /i "%PATH_COMPILE%"                "%NAME_PAK_ZIP%\%PATH_PROGRAM%"
xcopy    "%PATH_COMPILE%\%NAME_EXE_BAT%" "%NAME_PAK_ZIP%\"

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

rem %ZIP% "%NAME_PAK_ZIP%.zip" "%NAME_PAK_ZIP%\"
rem set EXIT_CODE=%errorlevel%
start .\

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

timeout /t 10 /nobreak
exit /b %EXIT_CODE%
