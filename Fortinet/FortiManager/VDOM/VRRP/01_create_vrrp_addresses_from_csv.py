##############################################################
##                                                          ##
##      - Author: Joshua Bergman                            ##
##      - Version: 0.1 (Draft)                              ##
##      - Date: 11-09-2024                                  ##
##                                                          ##
##############################################################

## Import dependencies
import csv ##CSV file handling
import requests ##API handling
import os ##OS file handling
import getpass ##OS username handling
import urllib3 ##Suppress SSL warning

## FortiManager login variables
fmg_username = input("Username: ")
fmg_password = getpass.getpass(prompt="Password: ", stream=None)
fmg_ip_address = input("IP address: ")

## FortiManager ADOM variable
adom = "root"

## Get current username for file handling
win_username = getpass.getuser()

## CSV variables
csv_delimiter = ';'

## Define file paths
base_file_path = os.path.join("c:/Users/", win_username, "Documents/Python-Networking/FortiManager/VDOM/VRRP/")
vdom_input_csv_file = os.path.join(base_file_path, "vrrpaddresses.csv")

## Ignore invalid SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## API
apisession = requests.session()

## Specify JSON header
json_api_header = {
    'Content-Type': 'application/json'
}

########################################## GET SESSION ID ##########################################

## Define JSON API Body for session ID request
json_api_session_id_body = {
    "id": 1,
    "method": "exec",
    "params": [{"data": {"user": fmg_username, "passwd": fmg_password}, "url": "/sys/login/user"}]
}

## Define login URL
json_rpc_api_url = f'https://{fmg_ip_address}/jsonrpc'

## Get session ID function
def get_session_id():
    response = apisession.post(json_rpc_api_url, json=json_api_session_id_body, headers=json_api_header, verify=False)
    if response.status_code == 200:
        print(f'Succesfully logged in to {fmg_ip_address}')
        session_id_json_ouput = response.json()
        session_id = session_id_json_ouput.get('session')
        return session_id
    else:
        print(f'Failed to connect to {fmg_ip_address}, error code: {response.status_code}, error: {response.text}')
        return None

## Call session ID function
session_id = get_session_id()

########################################## LOCK ADOM ##########################################

## Define JSON API Body for locking ADOM
json_api_lock_adom_body = {
    "method": "exec",
    "params": [{"url": f'/dvmdb/adom/{adom}/workspace/lock'}],
    "session": session_id,
    "id": 1
}

## ADOM lock function
def lock_adom():
    response = apisession.post(json_rpc_api_url, json=json_api_lock_adom_body, headers=json_api_header, verify=False)
    if response.status_code == 200:
        print(f'Succesfully locked ADOM: {adom}')
    else:
        print(f'Failed to lock ADOM: {adom}, error code: {response.status_code}, error: {response.text}')

## Call ADOM lock function
lock_adom()

########################################## CREATE VRRP ADDRESSES ##########################################

def create_vrrp_address(adom, device_name, interface_name, vrrp_vrid, vrrp_priority, vrrp_vrgrp, vrrp_vrip):
    response = apisession.post(json_rpc_api_url, json=json_api_vrrp_address_body, headers=json_api_header, verify=False)
    if response.status_code == 200:
        print(f'Succesfully created VRRP config for {interface_name} @ {device_name}')
    else:
        print(f'Failed to create VRRP config for {interface_name} @ {device_name}')

## Read CSV file for VDOM creation
with open(vdom_input_csv_file, 'r') as vdomlist:
    csv_reader = csv.reader(vdomlist, delimiter=csv_delimiter)
    next(csv_reader, None)

## Loop trough CSV rules
    for row in csv_reader:
        device_name = row[0]
        interface_name = row[1]
        vrrp_vrid = row[2] ## Default is 1
        vrrp_priority = row[3] ## Default is 100
        vrrp_vrgrp = row[4]
        vrrp_vrip = row[5]

        json_api_vrrp_address_body = {
            "method": "add",
            "params": [
                {
                    "data": [
                     {
                         "priority": int(vrrp_priority),
                         "vrgrp": int(vrrp_vrgrp),
                         "vrid": int(vrrp_vrid),
                         "vrip": str(vrrp_vrip)
                     }
                 ],
                    "url": f"/pm/config/device/{device_name}/global/system/interface/{interface_name}/vrrp"
                }
            ],
            "session": session_id,
            "id": 1
        }

        create_vrrp_address(adom, device_name, interface_name, vrrp_vrid, vrrp_priority, vrrp_vrgrp, vrrp_vrip)

########################################## UNLOCK ADOM ##########################################

## Define JSON API Body for unlocking ADOM
json_api_unlock_adom_body = {
    "method": "exec",
    "params": [{"url": f'/dvmdb/adom/{adom}/workspace/unlock'}],
    "session": session_id,
    "id": 1
}

## ADOM unlock function
def unlock_adom():
    response = apisession.post(json_rpc_api_url, json=json_api_unlock_adom_body, headers=json_api_header, verify=False)
    if response.status_code == 200:
        print(f'Succesfully unlocked ADOM: {adom}')
    else:
        print(f'Failed to unlock ADOM: {adom}, error code: {response.status_code}, error: {response.text}')

## Call ADOM unlock function
unlock_adom()

########################################## LOGOUT SESSION ##########################################

## Define JSON API Body for logging out
json_api_logout_body = {
    "id": 1,
    "method": "exec",
    "params": [{"url": "/sys/logout"}],
    "session": session_id
}

## Logout function
def logout():
    response = apisession.post(json_rpc_api_url, json=json_api_logout_body, headers=json_api_header, verify=False)
    if response.status_code == 200:
        print(f'Succesfully logged out from {fmg_ip_address}')
    else:
        print(f'Failed to logout from {fmg_ip_address}')

## Call logout function
logout()