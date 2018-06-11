#!/bin/env bash

source "set-env-linux.load-source"

name_prog=XLSx2RewriteOut
name_prog=xls2rewrite_out.py
prog_main=XLSx2RewriteOut/xlsX2rewrite_out.py
file_gear=images/gear.ico

pyinstaller_prog=/home/pes0zap/Programmi/zappyk-python/bin/pyinstaller/pyinstaller.py
pyinstaller_eval="$pyinstaller_prog --clean --onefile --windowed --log-level=DEBUG"
pyinstaller_eval="$pyinstaller_prog --clean --onefile            --log-level=DEBUG"
pyinstaller_eval="$pyinstaller_prog --clean --onefile            --log-level=DEBUG"

$pyinstaller_eval --icon "$file_gear" --name "$name_prog" "$prog_main" "$@"

exit
