@echo off

rem set PROJECTDIR=$1
set PROJECTDIR=

if not defined PROJECTDIR set PROJECTDIR=%~dp0\..

set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=UTF-8
set PYTHONPATH=^
%PROJECTDIR%\lib;^
%PROJECTDIR%\lib\lib_external;^
%PROJECTDIR%\lib\lib_zappyk;^
%PROJECTDIR%\getRunSend;^
%PROJECTDIR%\switchOnOff;^
%PROJECTDIR%\runCmdServer;^
%PROJECTDIR%\findNameSend;^
.


echo PYTHONUNBUFFERED=%PYTHONUNBUFFERED%

echo PYTHONIOENCODING=%PYTHONIOENCODING%

echo PYTHONPATH=
echo %PYTHONPATH%
