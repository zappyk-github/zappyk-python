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
$PROJECTDIR/getRunSend:\
$PROJECTDIR/switchOnOff:\
$PROJECTDIR/runCmdServer:\
$PROJECTDIR/findNameSend:\
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
