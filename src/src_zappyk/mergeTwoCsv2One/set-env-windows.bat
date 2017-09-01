@echo off
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
set PROMPT=$P$G$_$D$S$T$_#
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

set PROJECTDIR=C:\Users\zappyk\PycharmProjects\zappyk-python
if "%COMPUTERNAME%" == "VM-IT-002" (
    set PROJECTDIR=U:\IT\Devel\Python\PyCharmProject\zappyk-python
)
echo Set Project Directory on %PROJECTDIR% ...

if not defined PROJECTDIR set PROJECTDIR=%~dp0\..\..

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=UTF-8
set PYTHONPATH=^
%PROJECTDIR%\lib;^
%PROJECTDIR%\lib\lib_external;^
%PROJECTDIR%\lib\lib_zappyk;^
%PROJECTDIR%\src\src_zappyk;^
.

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::