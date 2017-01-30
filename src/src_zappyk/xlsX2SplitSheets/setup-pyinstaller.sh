#!/bin/env bash

source "set-env-linux.load-source"

name_prog=XLSx2SplitSheets
name_prog=xls2splits-sheets.py
prog_main=XLSx2SplitSheets/xlsX2splits_sheets.py
file_gear=images/gear.ico

pyinstaller_prog=/home/pes0zap/Programmi/zappyk-python/bin/pyinstaller/pyinstaller.py
pyinstaller_eval="$pyinstaller_prog --clean --onefile --windowed --log-level=DEBUG"
pyinstaller_eval="$pyinstaller_prog --clean --onefile            --log-level=DEBUG"
pyinstaller_eval="$pyinstaller_prog --clean --onefile            --log-level=DEBUG"

$pyinstaller_eval --icon "$file_gear" --name "$name_prog" "$prog_main" "$@"

exit
