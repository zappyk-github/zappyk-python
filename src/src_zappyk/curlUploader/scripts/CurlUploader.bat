@echo off

set MFT_flow=%1
set MFT_file=%2
set MFT_path=resources\send_pathsave

set MFT_user=%3
set MFT_pswd=%4
set MFT_endp=http://apps.payroll.it/bos-mft-server/mft

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

set PROGRAM=CurlUploader\curl_uploader.py
rem OPTIONS=-fn "%MFT_flow%" -pf "%MFT_file%" -ps "%MFT_path%" -ua "%MFT_endp%" -uu "%MFT_user%" -up "%MFT_pswd%" -sm -gm %*
set OPTIONS=-fn "%MFT_flow%" -pf "%MFT_file%" -ps "%MFT_path%" -ua "%MFT_endp%" -uu "%MFT_user%" -up "%MFT_pswd%" -sm -gm
set FILELOG="%MFT_path%\%MFT_flow%-log.txt"

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if not defined OPTIONS set OPTIONS=--help
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
cd %~dp0
echo %PROGRAM% %OPTIONS%
call %PROGRAM% %OPTIONS% 1>> %FILELOG% 2>&1
set EXIT_CODE=%errorlevel%
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if errorlevel 1 (
    echo Failure Reason Given is %errorlevel%
    exit /b %errorlevel%
)
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
rem timeout /t 10 /nobreak
exit /b %EXIT_CODE%