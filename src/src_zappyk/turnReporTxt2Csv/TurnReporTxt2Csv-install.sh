#!/bin/env bash

PATH_BASE="${1:-$HOME}"

[ ! -d "$PATH_BASE" ] && echo "Attenzione, directory di installazione '$PATH_BASE' inesistente..." && exit 1

PROG_NAME='TurnReporTxt2Csv'
PROG_VERS='0.0.1b1'
PROG_PATH="$PROG_NAME-$PROG_VERS"


cp -vr "build/$PROG_PATH"           "$PATH_BASE"
cp -v   TurnReporTxt2Csv.sh         "$PATH_BASE"

cp -v   TurnReporTxt2Csv-config.ini "$PATH_BASE/$PROG_PATH/"
cp -v   TurnReporTxt2Csv-launch.bat "$PATH_BASE/$PROG_PATH/"
cp -v   TurnReporTxt2Csv-logger.ini "$PATH_BASE/$PROG_PATH/"