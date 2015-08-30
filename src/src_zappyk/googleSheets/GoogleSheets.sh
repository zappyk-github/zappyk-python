#!/bin/env bash

PRG_NAME='GoogleSheets'
PRG_VERS='0.0.1b1'
HOSTARCH='64bit_ELF'

DIR_BASE="GoogleSheets-$PRG_VERS"
DIR_ARCH="exe.linux-$HOSTARCH-python-3.4.2"

PRG_BASE="$DIR_BASE"
PRG_EXEC="$DIR_ARCH/$PRG_NAME"
PROGRAMM="$PRG_BASE/$PRG_EXEC"

[ ! -e "$PROGRAMM" ] && echo "Programma '$PRG_NAME' non installato..." && exit 1
[ ! -x "$PROGRAMM" ] && echo "Programma '$PRG_NAME' non eseguibile..." && exit 1

cd "$PRG_BASE" && $PRG_EXEC "$@"

exit
