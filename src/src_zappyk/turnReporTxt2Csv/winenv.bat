@echo off

set PROJECTDIR=C:\Users\zappyk\PycharmProjects\zappyk-python

if not defined PROJECTDIR set PROJECTDIR=%~dp0\..

set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=UTF-8
set PYTHONPATH=^
%PROJECTDIR%\lib;^
%PROJECTDIR%\lib\lib_external;^
%PROJECTDIR%\lib\lib_zappyk;^
%PROJECTDIR%\src\src_zappyk;^
.

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::