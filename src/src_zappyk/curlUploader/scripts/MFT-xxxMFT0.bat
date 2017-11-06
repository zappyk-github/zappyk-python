@echo off

set file_send=resources\send-file.txt

call %~dp0\CurlUploader.bat xxxMFT0 "%file_send%" xxxmft0 password

exit /b %errorlevel%
