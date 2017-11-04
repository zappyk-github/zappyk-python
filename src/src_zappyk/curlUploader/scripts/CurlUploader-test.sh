#!/bin/env bash

MFT_flow=BRUMFT0
MFT_file=resources/send_filename.txt
MFT_path=resources/send_pathsave

MFT_endp=http://apps.payroll.it/bos-mft-server/mft
MFT_user=brumft0
MFT_pswd=5353265d550602

CURLprog=CurlUploader/curl_uploader
CURLprog=CurlUploader/curl_uploader.py

"$CURLprog" -fn "$MFT_flow" -pf "$MFT_file" -ps "$MFT_path" -ua "$MFT_endp" -uu "$MFT_user" -up "$MFT_pswd" -sm -gm "$@"

exit