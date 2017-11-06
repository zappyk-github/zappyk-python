#!/bin/env bash

MFT_flow=$1 ; shift # $1
MFT_file=$1 ; shift # $2
MFT_path=resources/send_pathsave

MFT_user=$1 ; shift # $3
MFT_pswd=$1 ; shift # $4
MFT_endp=http://apps.payroll.it/bos-mft-server/mft

CURLprog=CurlUploader/curl_uploader.py

"$CURLprog" -fn "$MFT_flow" -pf "$MFT_file" -ps "$MFT_path" -ua "$MFT_endp" -uu "$MFT_user" -up "$MFT_pswd" -sm -gm "$@"

exit