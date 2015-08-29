#!/bin/env bash

CXFREEZE=cxfreeze

PATH_BASE=$(dirname "$0")
PATH_HOME=$PATH_BASE/../../

cd "$PATH_HOME"

echo "Avvio di $CXFREEZE in corso..."

$CXFREEZE      "test/src/main.py" \
--include-path "test/img;test/lib;test/src;test/cfg" \
--icon         "test/img/gear.ico" \
--target-dir   "test/dist/linux" \
--compress \
--silent