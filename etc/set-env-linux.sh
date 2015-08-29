#!/bin/env bash

#CZ#PROJECTDIR=$1
PROJECTDIR=

[ -z "$PROJECTDIR" ] && PROJECTDIR=$(readlink -f $(dirname "$0")/..)

PYTHONUNBUFFERED=1
PYTHONIOENCODING='UTF-8'
PYTHONPATH="\
$PROJECTDIR/lib:\
$PROJECTDIR/lib/lib_external:\
$PROJECTDIR/lib/lib_zappyk:\
$PROJECTDIR/src/src_zappyk:\
.\
"

echo "PROJECTDIR=$PROJECTDIR"

echo "export PYTHONUNBUFFERED=$PYTHONUNBUFFERED"
export PYTHONUNBUFFERED

echo "export PYTHONIOENCODING=$PYTHONIOENCODING"
export PYTHONIOENCODING

echo "export PYTHONPATH=$PYTHONPATH"
export PYTHONPATH

echo "alias pyinstaller=$PROJECTDIR/bin/pyinstaller/pyinstaller.py"
alias pyinstaller=$PROJECTDIR/bin/pyinstaller/pyinstaller.py

echo "alias cx_freeze=$PROJECTDIR/bin/cx_freeze/cxfreeze"
echo "alias cx_freeze_quickstart=$PROJECTDIR/bin/cx_freeze/cxfreeze-quickstart"
alias cx_freeze=$PROJECTDIR/bin/cx_freeze/cxfreeze
alias cx_freeze_quickstart=$PROJECTDIR/bin/cx_freeze/cxfreeze-quickstart
