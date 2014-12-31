#!/bin/env bash

#command='rm -Rfv'
#command='ls -dla'
#command='ls -d'
 command=${*:-ls -d}

find ./ -name "__pycache__" | xargs $command

exit
