@echo off
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
set PROMPT=$P$G$_$D$S$T$_#
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

rem set PROJECTDIR=$1
set PROJECTDIR=

if not defined PROJECTDIR set PROJECTDIR=%~dp0\..

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

echo PYTHONUNBUFFERED=%PYTHONUNBUFFERED%

echo PYTHONIOENCODING=%PYTHONIOENCODING%

echo PYTHONPATH=^
%PYTHONPATH%
