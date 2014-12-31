#!/bin/env bash

PYTHON='python3'

PATH_BASE=$(dirname "$0")
PATH_HOME="$PATH_BASE/../"
PATH_HOME=$(cd -L "$PATH_HOME" && pwd)

IFS=$'\n'
for file in $(find "$PATH_HOME/" -iname "*.py" -print0 | xargs -0 -i echo "{}"); do
    echo "$PYTHON -m py_compile \"$file\""
done

exit
