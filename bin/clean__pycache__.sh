#!/bin/env bash

#command='rm -Rfv'
#command='ls -dla'
#command='ls -d'
 command=${*:-ls -d}

find ./ -name "src_external" -prune -o -name "__pycache__" -exec $command {} \;
find ./ -name "src_external" -prune -o -name "*.pyc"       -exec $command {} \;

exit
