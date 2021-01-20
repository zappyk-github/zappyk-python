#!/bin/env bash

PATH_PROG='lib/lib_zappyk/_pdf2img2txt.py'

CMDPYTHON=$(which zappyk-pythonx.sh 2>/dev/null)
PATH_NAME=$(dirname "$0")
PATH_BASE="$PATH_NAME/.."
CMDSOURCE="$PATH_BASE/etc/set-env-linux.load-source"

if [ -z "$CMDPYTHON" ]; then
    source "$PATH_BASE/$CMDSOURCE"
    CMDPYTHON=$(which python)

    if [ -z "$CMDPYTHON" ]; then
        echo "Install python!" ; exit 1
    fi
fi

"$CMDPYTHON" "$PATH_BASE/$PATH_PROG" "$@"

exit
