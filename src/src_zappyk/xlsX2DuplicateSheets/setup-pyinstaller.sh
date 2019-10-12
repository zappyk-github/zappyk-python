#!/bin/env bash

source "set-env-linux.load-source"

name_prog=XLSx2DuplicateSheets
name_prog=xls2duplicate-sheets.py
prog_main=XLSx2DuplicateSheets/xlsX2duplicate_sheets.py
file_gear=images/gear.ico

pyinstaller_prog=/home/pes0zap/Programmi/zappyk-python/bin/pyinstaller/pyinstaller.py
pyinstaller_eval="$pyinstaller_prog --clean --onefile --windowed --log-level=DEBUG"
pyinstaller_eval="$pyinstaller_prog --clean --onefile            --log-level=DEBUG"
pyinstaller_eval="$pyinstaller_prog --clean --onefile            --log-level=DEBUG"

$pyinstaller_eval --icon "$file_gear" --name "$name_prog" "$prog_main" "$@"

exit
