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

## FortiManager ADOM variable
adom = "1PLATFORM"

## Get current username for file handling
logged_in_user = getpass.getuser()

## CSV variables
csv_delimiter = ';'

## Define file paths
base_file_path = os.path.join("c:/Users/", logged_in_user, "Documents/Python-Networking/")
vdom_input_csv_file = os.path.join(base_file_path, "vdomcreationlist.csv")

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

## Lock ADOM for VDOM creation
payload_url_lock_adom = f'https://{host}/jsonrpc'
json_api_adom_lock_body = {
        "method": "exec",
        "params": [
            {
                "url": f'/dvmdb/adom/{adom}/workspace/lock'
            }
        ],
        "session": session_id,
        "id": 1
    }

lock_adom_request = logout_request = requests.post(payload_url_lock_adom, json=json_api_adom_lock_body, headers=json_api_header, verify=False)
print(f'Locked ADOM: {adom}')

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
        sslvpn_status = row[4] ## enable or disable
        vdom_session = row[5] ## Integer
        vdom_firewall_policy = row[6] ## Integer
        vdom_firewall_address = row[7] ## Integer
        vdom_firewall_address_group = row[8] ## Integer


        ## JSON RPC API Request
        payload_url = f'https://{host}/jsonrpc'
        
        ## VDOM creation body
        json_api_vdom_body = {
			"method": "add",
			"params": [
				{
					"data": [
						{
							"comments": comments,
							"name": vdom_name,
							"opmode": opmode,
							"vdom_type": "traffic",
						}
					],
					"url": f"/dvmdb/adom/{adom}/device/{device_name}/vdom"
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

        ## SSLVPN settings for VDOM
        json_api_vdom_sslvpn_body = {
            "method": "set",
            "params": [
                {
                    "data": [
                        {
                            "status": sslvpn_status
                        }
                    ],
                    "url": f'/pm/config/device/{device_name}/vdom/{vdom_name}/vpn/ssl/settings'
                }
            ],
            "session": session_id,
			"id": 1
        }

        vdom_sslvpn_request = requests.post(payload_url, json=json_api_vdom_sslvpn_body, headers=json_api_header, verify=False)
        if vdom_sslvpn_request.status_code == 200:
            print(f'SSLVPN settings changed for VDOM: {vdom_name} at {device_name}')
        else:
            print(f'SSLVPN settings failed for VDOM: {vdom_name} at {device_name}')

        ## Set VDOM resources
        json_api_vdom_resources = {
            "method": "set",
            "params": [
                {
                    "data": [
                        {
                            "firewall-address": vdom_firewall_address,
                            "firewall-addrgrp": vdom_firewall_address_group,
                            "firewall-policy": vdom_firewall_policy,
                            "session": vdom_session
                        }
                    ],
                    "url": f'/pm/config/device/{device_name}/global/system/vdom-property/{vdom_name}'
                }
            ],
            "session": session_id,
			"id": 1
        }

        vdom_resources_request = requests.post(payload_url, json=json_api_vdom_resources, headers=json_api_header, verify=False)
        if vdom_resources_request.status_code == 200:
            print(f'Resource limits set for VDOM: {vdom_name} at {device_name}')
        else:
            print(f'Resource limits failed for VDOM: {vdom_name} at {device_name}')

## Let user know VDOM creation is done
print("VDOM creation is done")

## Unlock ADOM
payload_url_unlock_adom = f'https://{host}/jsonrpc'
json_api_adom_unlock_body = {
        "method": "exec",
        "params": [
            {
                "url": f'/dvmdb/adom/{adom}/workspace/unlock'
            }
        ],
        "session": session_id,
        "id": 1
    }

unlock_adom_request = logout_request = requests.post(payload_url_unlock_adom, json=json_api_adom_unlock_body, headers=json_api_header, verify=False)
print(f'Unlocked ADOM: {adom}')

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