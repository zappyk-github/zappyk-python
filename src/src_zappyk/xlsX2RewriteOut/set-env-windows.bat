@echo off
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
set PROMPT=$P$G$_$D$S$T$_#
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

rem PROJECTDIR=C:\Users\zappyk\PycharmProjects\zappyk-python
set PROJECTDIR=C:\Users\CarloZappacosta\Programmi\Python\PycharmProjects\zappyk-python-projects\zappyk-python

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