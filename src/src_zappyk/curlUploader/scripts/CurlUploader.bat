@echo off

set MFT_flow=BRUMFT0
set MFT_file=resources\send_filename.txt
set MFT_path=resources\send_pathsave

set MFT_endp=http://apps.payroll.it/bos-mft-server/mft
set MFT_user=brumft0
set MFT_pswd=5353265d550602

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

set PROGRAM=CurlUploader\curl_uploader.exe
set OPTIONS=-fn "%MFT_flow%" -pf "%MFT_file%" -ps "%MFT_path%" -ua "%MFT_endp%" -uu "%MFT_user%" -up "%MFT_pswd%" -sm -gm %*

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if not defined OPTIONS set OPTIONS=--help
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
cd %~dp0
echo %PROGRAM% %OPTIONS%
call %PROGRAM% %OPTIONS%
set EXIT_CODE=%errorlevel%
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if errorlevel 1 (
    echo Failure Reason Given is %errorlevel%
    exit /b %errorlevel%
)
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
rem timeout /t 10 /nobreak
exit /b %EXIT_CODE%