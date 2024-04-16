##############################################################
##      - Python script for checking config compliancy      ##
##      - Author: Joshua Bergman                            ##
##      - Version: 0.1 (Draft)                              ##
##      - Date: 15-03-2024                                  ##
##############################################################

import netmiko
import os
import getpass
import sys
from time import sleep
from netmiko import ConnectHandler

## Define variables
username = input("Username: ")
password = getpass.getpass(prompt="Password: ", stream=None)
ip_address = "..."
device_type = 'juniper_junos'
port = '22'

## Get username for file handling
pc_username = getpass.getuser()

## Create file path
config_file_path = os.path.join("c:/Users/", pc_username, "Documents/PythonJuniper/")

## Define file names
configuration_file_input = os.path.join(config_file_path, "compliancyconfig.txt")

## Check if file is not empty
if os.stat(configuration_file_input).st_size == 0:
    print("Nothing in file to check")
    sleep(2)
    sys.exit()

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
def is_alive(net_connect):
    null = chr(0)

    try:
        net_connect.write_channel(null)
        print("SSH session connected")
    except (EOFError):
        print("SSH session denied")
        sleep(2)
        sys.exit()

## Function to retrieve switch configuration
def get_switch_config(net_connect):
    output = net_connect.send_command("show")
    return output

## Main function to compare configurations
def compare_configurations(switch_config, file_config):
    missing_configs = []
    for line in file_config.split('\n'):
        if line.strip() not in switch_config:
            missing_configs.append(line.strip())
    return missing_configs

## Main code
is_alive(net_connect)
switch_config = get_switch_config(net_connect)
with open(configuration_file_input, 'r') as file:
    file_config = file.read()
missing_configs = compare_configurations(switch_config, file_config)
if missing_configs:
    print("The following configurations from the file are missing in the switch:")
    for config in missing_configs:
        print(config)
else:
    print("All configurations from the file are present in the switch.")