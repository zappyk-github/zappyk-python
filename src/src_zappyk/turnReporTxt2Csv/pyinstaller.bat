@echo off
call winenv.bat
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

set pyinstaller=pyinstaller.exe --onefile --windowed --icon=images\gear.ico --version-file=pyinstaller-version.txt
set pyinstaller=pyinstaller.exe --onefile --windowed --icon=images\gear.ico
set pyinstaller=pyinstaller.exe --onefile --windowed --log-level=DEBUG --clean

rem pyinstaller --noconfirm --log-level=WARN ^
rem     --onefile --nowindow ^
rem     --hidden-import=secret1 ^
rem     --hidden-import=secret2 ^
rem     --icon-file=..\MLNMFLCN.ICO ^
rem     myscript.spec

rem %pyinstaller% TurnReporTxt2Csv\main.py -rg

TurnReporTxt2Csv\main.py -rg