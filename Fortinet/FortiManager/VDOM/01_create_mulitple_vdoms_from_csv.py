##############################################################
##                                                          ##
##      - Author: Joshua Bergman                            ##
##      - Version: 0.1 (Draft)                              ##
##      - Date: 21-06-2024                                  ##
##                                                          ##
##############################################################

## Import dependencies
import csv ##CSV file handling
import requests ##API handling
import os ##OS file handling
import getpass ##OS username handling
import urllib3 ##Suppress SSL warning

## FortiManager login variables
username = input("Username: ")
password = getpass.getpass(prompt="Password: ", stream=None)
host = input("IP address: ")

## Get current username for file handling
logged_in_user = getpass.getuser()

## CSV variables
csv_delimiter = ';'

## Define file paths
base_file_path = os.path.join("c:/Users/", logged_in_user, "Documents/Python-Networking/")
vdom_input_csv_file = os.path.join("vdomcreationlist.csv")
vdom_resource_input_csv_file = os.path.join("vdomresourcelist.csv")

## Ignore invalid SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## Specify global JSON header
json_api_header = {
    'Content-Type': 'application/json'
}

## Get session ID
json_api_session_id_body = {
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
login_request = requests.post(login_url, json=json_api_session_id_body, headers=json_api_header, verify=False)

## Print successfull logon
print("Logged in successfully!")

## Get Session ID
session_id_json_ouput = login_request.json()
session_id = session_id_json_ouput.get('session')

## Read CSV file for VDOM creation
with open(vdom_input_csv_file, 'r') as vdomlist:
    csv_reader = csv.reader(vdomlist, delimiter=csv_delimiter)
    next(csv_reader, None)

## Loop trough CSV rules
    for row in csv_reader:
        vdom_name = row[0] ## VDOM name
        opmode = row[1] ## nat or transparent
        comments = row[2] ## comments in string format
        device_name = row[3] ## device name in string format

        ## JSON RPC API Request
        payload_url = f'https://{host}/jsonrpc'
        
        ## JSON RPC API Data
        json_api_vdom_body = {
            "method": "add",
            "params": [
                {
                    "data": [
                        {
                            'name': vdom_name,
                            'opmode': opmode,
                            'status': ' ',
                            'vdom_type': 'traffic',
                            'comments': comments
                        }
                    ],
                    "url": f'/dvmdb/device/{device_name}/vdom'
                }
            ],
            "session": session_id,
            "id": 1
        }

        ## Send request to create VDOM
        vdom_create_request = requests.post(payload_url, json=json_api_vdom_body, headers=json_api_header, verify=False)
        if vdom_create_request.status_code == 200:
            print(f'Created VDOM: {vdom_name} at {device_name}')
        else:
            print(f'Request failed for VDOM: {vdom_name} at {device_name}, error code: {vdom_create_request.status_code}')

## Let user know VDOM creation is done
print("VDOM creation is done")

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
logout_request = requests.post(logout_url, json=logout_body, headers=json_api_header, verify=False)

## Print logout
print("Logged out successfully")