##############################################################
##      - Config backup script via FortiGate API            ##
##      - Author: Joshua Bergman                            ##
##      - Version: 0.1 (Draft)                              ##
##      - Date: 24-12-2024                                  ##
##############################################################

from fortigate_api import FortiGateAPI
import getpass
from datetime import datetime
import os
import requests

## Define login variables
fortigate_ip = input("FortiGate IP: ")
token = getpass.getpass(prompt="Token: ", stream=None)
vdom = 'root'
port = '443'

## Define other
pc_username = getpass.getuser()
date = datetime.now().strftime('%d_%m_%Y')
backup_file_path = os.path.join("c:/Users/", pc_username, "Documents/Python-Networking/")

## Assemble API request
### Create a session
client = requests.session()

### Disable SSL verification
client.verify = False

## Get hostname for file name
hostname_api_request = (f'https://{fortigate_ip}:{port}/api/v2/cmdb/system/global?scope=global&access_token={token}')

## Define API request URL
backup_api_request =(f'https://{fortigate_ip}:{port}/api/v2/monitor/system/config/backup?scope=vdom&vdom={vdom}&access_token={token}')

### Send GET request
backup_file_response = client.get(backup_api_request)
hostname_response = client.get(hostname_api_request)

## Extract hostname from JSON query
if hostname_response.ok:
    hostname_data = hostname_response.json()
    hostname = hostname_data.get("results", {}).get("hostname")

## Write backup content to file
if backup_file_response.ok:
    with open(backup_file_path + f'{hostname}_backup_{date}.conf', 'wb') as f:
        f.write(backup_file_response.content)
    print("Config file saved succesfully as:" + backup_file_path + f"{hostname}_backup_{date}.conf")
else:
    print("Failed to retrieve config file, Status code:", backup_file_response.status_code)