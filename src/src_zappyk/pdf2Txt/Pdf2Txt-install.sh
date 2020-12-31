#!/bin/env bash

PATH_BASE="${1:-$HOME}"

[ ! -d "$PATH_BASE" ] && echo "Attenzione, directory di installazione '$PATH_BASE' inesistente..." && exit 1

PROG_NAME='Pdf2Txt'
PROG_VERS='0.0.1b1'
PROG_PATH="$PROG_NAME-$PROG_VERS"


cp -vr "build/$PROG_PATH"  "$PATH_BASE"
cp -v   Pdf2Txt.sh         "$PATH_BASE"

cp -v   Pdf2Txt-config.ini "$PATH_BASE/$PROG_PATH/"
cp -v   Pdf2Txt-launch.bat "$PATH_BASE/$PROG_PATH/"
cp -v   Pdf2Txt-logger.ini "$PATH_BASE/$PROG_PATH/"