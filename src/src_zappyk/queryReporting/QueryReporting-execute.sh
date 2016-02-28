#!/bin/env bash

_SET_ENV_='../../../set-env-linux.load-source'
PROG_NAME='QueryReporting'
PROG_MAIN='main.py'

source "$_SET_ENV_"

eval "$PROG_NAME/$PROG_MAIN" "$@"

exit
