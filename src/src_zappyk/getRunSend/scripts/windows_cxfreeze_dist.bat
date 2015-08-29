@echo off

set CXFREEZE=C:\Python34\Scripts\cxfreeze

cd ..\..\
cd

echo Avvio di %CXFREEZE% in corso...

start /wait /b ^
%CXFREEZE%     "test\src\main.py" ^
--include-path "test\img;test\lib;test\src;test\cfg" ^
--icon         "test\img\gear.ico" ^
--target-dir   "test\dist\windows" ^
--compress ^
--silent