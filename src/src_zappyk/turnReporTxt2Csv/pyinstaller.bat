@echo off
call winenv.bat
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

pyinstaller.exe ^
 --onefile --windowed --icon=images\gear.ico --version-file=pyinstaller-version.txt ^
 TurnReporTxt2Csv\main.py -rg