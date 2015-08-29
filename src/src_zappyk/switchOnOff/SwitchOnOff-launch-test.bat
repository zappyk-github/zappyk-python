@echo off

set PROGRAM=.\SwitchOnOff-launch.bat

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
rem call %PROGRAM% update -fn IB_PWHRETL -ff 0
rem call %PROGRAM% update -fn IB_PJHRETL -ff 0
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
call %PROGRAM% list
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
call %PROGRAM% select -fn IB_PWHRETL -on
if errorlevel 1 (
    echo Elaborazione ETL per Paghe Web STOPPPATA!
) else (
	echo Elaborazione ETL per Paghe Web attivo...
)
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
call %PROGRAM% select -fn IB_PJHRETL -on
if errorlevel 1 (
    echo Elaborazione ETL per Paghe Project STOPPPATA!
) else (
	echo Elaborazione ETL per Paghe Project attivo...
)
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
timeout /t 10 /nobreak