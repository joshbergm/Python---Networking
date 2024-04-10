import csv ##CSV file handling
import requests
import os ##OS file handling
import getpass ##OS username handling
import urllib3

## Device system variables
username = input("Username: ")
password = getpass.getpass(prompt="Password: ", stream=None)
host = input("IP address: ")

## Get current username
pc_username = getpass.getuser()

## Define file variables
base_file_path = os.path.join("c:/Users/", pc_username, "Documents/Python-Networking/")
input_csv_file = os.path.join(base_file_path, "objectlist.csv")

## Suppress the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## Specify JSON header
header = {
    'Content-Type': 'application/json'
}

## Get session ID
login_body = {
    "id": 1,
    "method": "exec",
    "params": [
        {
            "data": {
                "user": username,
                "passwd": password
            },
            "url": "/sys/login/user"
        }
    ],
}

login_url = f'https://{host}/jsonrpc'
login_request = requests.post(login_url, json=login_body, headers=header, verify=False)

## Get Session ID
session_id_json_ouput = login_request.json()
session_id = session_id_json_ouput.get('session')

## Read CSV file
with open(input_csv_file, 'r') as objectlist:
    csv_reader = csv.reader(objectlist, delimiter=';')
    next(csv_reader, None)

## Loop trough CSV rules
    for row in csv_reader:
        name = row[0]
        subnet = row[1]
        adom = row[2]
        comments = row[3]
        
        ## JSON RPC API Request
        payload_url = f'https://{host}/jsonrpc'
        
        ## JSON RPC API Data
        firewallobject_body = {
            "method": "set",
            "params": [
                {
                    "data": [
                        {
                            "name": name,
                            'subnet': subnet,
                            'comment': comments,
                            'type': "ipmask"
                        }
                    ],
                    "url": f'/pm/config/adom/{adom}/obj/firewall/address'
                }
            ],
            "session": session_id,
            "id": 1
        }
        
        ## Send request
        requests.post(payload_url, json=firewallobject_body, headers=header, verify=False)
        
## Log out
logout_body = {
    "id": 1,
    "method": "exec",
    "params": [
        {
            "url": "/sys/logout"
        }
    ],
    'session': session_id
}

logout_url = f'https://{host}/jsonrpc'
logout_request = requests.post(logout_url, json=logout_body, headers=header, verify=False)