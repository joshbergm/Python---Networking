##############################################################
##                                                          ##
##      - Author: Joshua Bergman                            ##
##      - Version: 0.1 (Draft)                              ##
##      - Date: 12-09-2024                                  ##
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
base_file_path = os.path.join("c:/Users/", win_username, "Documents/Python-Networking/FortiManager/VDOM/Interface/")
vrrp_address_csv_file = os.path.join(base_file_path, "normalizedinterfaces.csv")

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
        print(f'Successfully logged in to {fmg_ip_address}')
        session_id_json_output = response.json()
        session_id = session_id_json_output.get('session')
        return session_id
    else:
        print(f'Failed to connect to {fmg_ip_address}, error code: {response.status_code}, error: {response.text}')
        return None

## Call session ID function
session_id = get_session_id()

if session_id:
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
            print(f'Successfully locked ADOM: {adom}')
        else:
            print(f'Failed to lock ADOM: {adom}, error code: {response.status_code}, error: {response.text}')

    ## Call ADOM lock function
    lock_adom()
    
    ########################################## Create Normalized Interfaces ##########################################
    
    
    
    
    
    ########################################## Link Device Interfaces ##########################################
    
    
    
    
    ########################################## UNLOCK ADOM #########################################

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
            print(f'Successfully unlocked ADOM: {adom}')
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
            print(f'Successfully logged out from {fmg_ip_address}')
        else:
            print(f'Failed to log out from {fmg_ip_address}')

    ## Call logout function
    logout()
    
########################################## BREAK IF NO SESSION ID ##########################################
    
else:
    print("Login failed, cannot proceed.")