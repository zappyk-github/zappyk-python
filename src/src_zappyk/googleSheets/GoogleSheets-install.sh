#!/bin/env bash

PATH_BASE="${1:-$HOME}"

[ ! -d "$PATH_BASE" ] && echo "Attenzione, directory di instllazione '$PATH_BASE' inesistente..." && exit 1

PROG_NAME='GoogleSheets'
PROG_VERS='0.0.1b1'
PROG_VERS='0.0.2b1'
PROG_PATH="$PROG_NAME-$PROG_VERS"


cp -vr "build/$PROG_PATH"           "$PATH_BASE"
cp -v   GoogleSheets.sh             "$PATH_BASE"

cp -v   GoogleSheets-config.ini     "$PATH_BASE/$PROG_PATH/"
cp -v   GoogleSheets-launch.bat     "$PATH_BASE/$PROG_PATH/"
cp -v   GoogleSheets-logger.ini     "$PATH_BASE/$PROG_PATH/"
cp -vr  GoogleSheets.pem            "$PATH_BASE/$PROG_PATH/"
