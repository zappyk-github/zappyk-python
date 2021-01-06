#!/bin/env bash

path_python=$(dirname "$(readlink "$0")")
file_source="$path_python/../etc/set-env-linux.load-source"

source "$file_source" && python "$@"

exit
