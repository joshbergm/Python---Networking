##############################################################
##      - Python script for applying Juniper config         ##
##      - Author: Joshua Bergman                            ##
##      - Version: 0.1 (Draft)                              ##
##      - Date: 15-03-2024                                  ##
##############################################################

## Import libraries
import netmiko
import getpass
import os
import sys
from time import sleep
from netmiko import ConnectHandler

## Define variables
username = input("Username: ")
password = getpass.getpass(prompt="Password: ", stream=None)
ip_address = input("IP address: ")
device_type = 'juniper_junos'
port = '22'

## SSH connection details
juniper = {
    'device_type': device_type,
    'host': ip_address,
    'username': username,
    'password': password,
    'port': port,
}

## Create session
net_connect = ConnectHandler(**juniper)

## SSH session succesfull?
def is_allive(net_connect):
    null = chr(0)

    try:
        net_connect.write_channel(null)
        print("SSH session connected")
    except (EOFError):
        print("SSH session denied")
        sleep(2)
        sys.exit()

## Import config from file
pc_username = getpass.getuser()
config_file_path = os.path.join("c:/Users/", pc_username, "Documents/PythonJuniper/config.txt")
configuration_file = open(config_file_path)

## Check if file is not empty
if os.stat(config_file_path).st_size == 0:
    print("Nothing in file to push")
    sleep(2)
    sys.exit()

## Push config
net_connect.config_mode()
net_connect.send_config_from_file(config_file_path)

## Ask to view changes after deployement
compare_question = None
while compare_question not in ("y", "n"):
    compare_question = input("View changes y/n? ")
    if compare_question == "y":
        net_connect.config_mode()
        compare_output = net_connect.send_command_timing("show | compare")
        print(compare_output, '\n')
    elif compare_question == "n":
        continue
    else:
        print("View changes y/n? ")

## Ask user to commit changes
commit_question = None
while commit_question not in ("y", "n"):
    commit_question = input("Commit changes y/n? ")
    if commit_question == "y":
        net_connect.commit()
    elif commit_question == "n":
        continue
    else:
        print("Commit changes y/n? ")

## Disconnect SSH session
net_connect.disconnect()

## Print successfull push
print('Config applied')