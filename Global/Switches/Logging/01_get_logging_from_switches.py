##############################################################
##      - Python script for checking config compliancy      ##
##      - Author: Joshua Bergman                            ##
##      - Version: 0.1 (Draft)                              ##
##      - Date: 22-05-2024                                  ##
##############################################################

## Import libs
import os
import getpass
from datetime import datetime, timedelta ## Get current time
from netmiko import ConnectHandler
import csv

## Define variables
port = '22'
delimiter = ';'

## Get username for file handling
pc_username = getpass.getuser()

## Get current time for file handling
date = datetime.now().strftime('%d-%m-%Y')

## Base file path
base_file_path = os.path.join("T:/ICT/Netwerk/Switchlogging")

## Device CSV
devicelist = os.path.join(f'{base_file_path}/devices.csv')

## Ouput file path
output_folder = os.path.join(f'{base_file_path}/output')

## Read CSV file and create loop
with open(devicelist, 'r') as devicelistcsv:
    csvreader = csv.reader(devicelistcsv, delimiter=delimiter)
    next(csvreader, None)
    
    ## Read rows and define variables
    for row in csvreader:
        netmiko_device = row[0]
        device_type = row[1]
        hostname = row[2]
        ip_address = row[3]
        username = row[4]
        password = row[5]
        show_command = row[6]
        
        ## SSH connection details
        netmiko_device = {
            'device_type': device_type,
            'host': ip_address,
            'username': username,
            'password': password,
            'port': port,
        }
        
        ## Try connection or throw error
        try:
            ssh = ConnectHandler(**netmiko_device)
            print(f'Connected to: {hostname}')
        
        except Exception as e:
            print(f'Error for: {hostname} with IP: {ip_address}, {e}')
        
        ## Get logging from switch
        output = ssh.send_command(f'{show_command}')
        
        ## Write logging to file
        with open(f'{output_folder}/{hostname}_{ip_address}_{date}.txt', 'w') as f:
            f.write(output)
            print(f'Logs exported for: {hostname}_{ip_address}')
        
    print('Done')