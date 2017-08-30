#!/bin/env bash

PATH_BASE="${1:-$HOME}"

[ ! -d "$PATH_BASE" ] && echo "Attenzione, directory di installazione '$PATH_BASE' inesistente..." && exit 1

PROG_NAME='MergeTwoCsv2One'
PROG_VERS='0.1.0.0'
PROG_PATH="$PROG_NAME-$PROG_VERS"


cp -vr "build/$PROG_PATH"          "$PATH_BASE"
cp -v   MergeTwoCsv2One.sh         "$PATH_BASE"

cp -v   MergeTwoCsv2One-config.ini "$PATH_BASE/$PROG_PATH/"
cp -v   MergeTwoCsv2One-launch.bat "$PATH_BASE/$PROG_PATH/"
cp -v   MergeTwoCsv2One-logger.ini "$PATH_BASE/$PROG_PATH/"
