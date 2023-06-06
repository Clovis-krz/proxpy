import os
from dotenv import load_dotenv
import time
from proxmoxer import ProxmoxAPI
import sys

load_dotenv(override=True)

node_name = os.getenv("NODE")

def init_connection():
    try:
        proxmox = ProxmoxAPI(os.getenv("HOST"), user=os.getenv("USER"), password=os.getenv("PASSWORD"), verify_ssl=True)
        return proxmox
    except OSError as err:
        print("Error: The connection could not be made, please make sure that your computer is connected to internet")
        time.sleep(2)
        main()

def intro_display():
   print("\t\t ____  ")
   print("\t\t|  _ \ _ __ _____  ___ __  _   _ ")
   print("\t\t| |_) | '__/ _ \ \/ / '_ \| | | |")
   print("\t\t|  __/| | | (_) >  <| |_) | |_| |")
   print("\t\t|_|   |_|  \___/_/\_\ .__/ \__, |")
   print("\t\t                    |_|    |___/ ")
   print()

def display_nodes(proxmox):
    try:
        running_list = []
        stopped_list = []
        status_symbol = "🔴"
        for pve_node in proxmox.nodes.get():
            for container in proxmox.nodes(pve_node['node']).qemu.get():
                if (container['status'] == "running"):
                    running_list.append((container['vmid'], container['name']))
                    status_symbol = "🟢"
                elif (container['status'] == "stopped"):
                    stopped_list.append((container['vmid'], container['name']))
                    status_symbol = "🔴"
                print("\t------------------------------------------------")
                print("\t%-21s %-21s %-21s" % (container['name'], container['status'], status_symbol))
                print("\t------------------------------------------------")
            print()
        return (running_list, stopped_list)
    except OSError as err:
        print("Error: The connection could not be made, please make sure that your computer is connected to internet")
        time.sleep(2)
        main()


def update_nodes(proxmox):
    try:
        running_list = []
        stopped_list = []
        for pve_node in proxmox.nodes.get():
            for container in proxmox.nodes(pve_node['node']).qemu.get():
                if (container['status'] == "running"):
                    running_list.append((container['vmid'], container['name']))
                elif (container['status'] == "stopped"):
                    stopped_list.append((container['vmid'], container['name']))
        return (running_list, stopped_list)
    except OSError as err:
        print("Error: The connection could not be made, please make sure that your computer is connected to internet")
        time.sleep(2)
        main()

def ask_switch():
    res = -1
    while res == -1:
        res = input("\tThe current session will be closed and any working progress unsaved.\n\tSwitch ? (y/n): ")
        if res == "y" or res == "yes":
            return 1
        elif res == "n" or res == "no":
            return 0
        else:
            res = -1

def ask_shutdown():
    res = -1
    while res == -1:
        res = input("\tThe current session will be closed and any working progress unsaved.\n\tShutdown ? (y/n): ")
        if res == "y" or res == "yes":
            return 1
        elif res == "n" or res == "no":
            return 0
        else:
            res = -1

def ask_poweroff_client():
    res = -1
    while res == -1:
        res = input("\tThe computer will be Powered OFF.\n\tAre you sure ? (y/n): ")
        if res == "y" or res == "yes":
            return 1
        elif res == "n" or res == "no":
            return 0
        else:
            res = -1

def loading_animation(value):
    if(value % 2 == 0):
        print("/", end='', flush=True)
    else:
        print("\x5c", end='', flush=True)

def shutdown(proxmox, node, vmid):
    try:
        proxmox.nodes(node).qemu(vmid).status.shutdown.post()
        time_spent = 0
        state = "running"
        print()
        while time_spent < 120 and state != "stopped":
            state = proxmox.nodes(node).qemu(vmid).status.current.get()['status']
            loading_animation(time_spent)
            time.sleep(3)
            time_spent += 3
        if(state == "stopped"):
            return 1
        else:
            print(str(vmid)+": cannot be shutdown")
            sys.exit(1)
    except OSError as err:
        print("Error: The connection could not be made, please make sure that your computer is connected to internet")
        time.sleep(2)
        main()

def start(proxmox, node, vmid):
    try:
        proxmox.nodes(node).qemu(vmid).status.start.post()
        time_spent = 0
        state = "stopped"
        print()
        while time_spent < 120 and state != "running":
            state = proxmox.nodes(node).qemu(vmid).status.current.get()['status']
            loading_animation(time_spent)
            time.sleep(3)
            time_spent += 3
        if(state == "running"):
            return 1
        else:
            print(str(vmid)+": cannot be started")
            sys.exit(1)
    except OSError as err:
        print("Error: The connection could not be made, please make sure that your computer is connected to internet")
        time.sleep(2)
        main()
    
def open_stream(computer_name):
    try:
        exit_code = 1
        tries_counter = 0
        while(exit_code != 0 and tries_counter < 60):
            exit_code = os.system("nc -vz "+computer_name+" 47984 -w 1")
            if(exit_code != 0):
                time.sleep(2)
                tries_counter += 1
        if(exit_code == 0):
            os.system(os.getenv("MOONLIGHTRUN")+" stream "+computer_name+" Desktop --quit-after")
            return 1
        else:
            print("\tCould not connect to "+computer_name+", PC offline")
            sys.exit(1)
    except OSError as err:
        print("Error: The connection could not be made, please make sure that your computer is connected to internet")
        time.sleep(2)
        main()


def main():
    proxmox = init_connection()
    (running_list, stopped_list) = update_nodes(proxmox)
    action = -1
    if(len(running_list) > 0 and action == -1):
        os.system("clear")
        intro_display()
        (running_list, stopped_list) = display_nodes(proxmox)
        print("\tWhat do you want to do ?")
        print("\t1: Open Streamer")
        print("\t2: Switch OS")
        print("\t3: Power OFF VM")
        print("\t4: Power ALL OFF")
        print("\t5: Nothing and exit")
        print()
        while(action != "1" and action != "2" and action != "3" and action != "4" and action != "5"):
            action = input("\t=> ")
        if(action == "1"):
            print("Opening Streamer...")
            open_stream(running_list[0][1])
        elif(action == "2"):
            do_switch = ask_switch()
            if(do_switch == 1):
                is_shut = shutdown(proxmox, node_name, running_list[0][0])
                if(is_shut == 1):
                    print(running_list[0][1]+" : Powered OFF")
                    is_on = start(proxmox, node_name, stopped_list[0][0])
                    if(is_on == 1):
                        print(stopped_list[0][1]+": Powered ON")
                        print()
                        display_nodes(proxmox)
                        open_stream(stopped_list[0][1])
        elif(action == "3"):
            do_shutdown = ask_shutdown()
            if(do_shutdown == 1):
                is_shut = shutdown(proxmox, node_name, running_list[0][0])
                if(is_shut == 1):
                    print(running_list[0][1]+" : Powered OFF")
                    print()
                    display_nodes(proxmox)
        elif(action == "4"):
            do_shutdown = ask_shutdown()
            if(do_shutdown == 1):
                is_shut = shutdown(proxmox, node_name, running_list[0][0])
                if(is_shut == 1):
                    print(running_list[0][1]+" : Powered OFF")
                    print()
                    display_nodes(proxmox)
                    os.system("poweroff")
        elif(action == "5"):
            print("Exiting...")
            sys.exit(0)
        main()
    else:
        os.system("clear")
        intro_display()
        (running_list, stopped_list) = display_nodes(proxmox)
        print("\tWhat do you want to do ?")
        for i in range(len(stopped_list)):
            print("\t"+str(i) + ": Power ON "+stopped_list[i][1])
        print("\t"+str(len(stopped_list))+": Power ALL OFF")
        print("\t"+str(len(stopped_list)+1)+": Nothing and exit")
        print()
        while(int(action) < 0 or int(action) > len(stopped_list)+1):
            action = input("\t=> ")
            if not action.isnumeric():
                action = -1
        action = int(action)
        if(action == len(stopped_list)):
            if(ask_poweroff_client() == 1):
                print("Exiting...")
                os.system("poweroff")
            else:
                main()
        if(action == len(stopped_list)+1):
            print("Exiting...")
            sys.exit(0)
        else:
            is_on = start(proxmox, node_name, stopped_list[action][0])
            if(is_on == 1):
                print()
                print(stopped_list[action][1]+": Powered ON")
                open_stream(stopped_list[action][1])
            main()

main()