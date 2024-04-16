##############################################################
##      - Python script for rekeying IPSec VPN's            ##
##      - Author: Joshua Bergman                            ##
##      - Version: 0.1 (Draft)                              ##
##      - Date: 16-03-2024                                  ##
##############################################################

from netmiko import ConnectHandler
import random
import string
import time

## Define variables
username = "..."
password = "..."
local_ip_address = "..."
remote_ip_address = "..."
device_type = 'fortinet'
port = '22'
key_length = 32

## Specify connection details
remote_fortigate = {
    'device_type': device_type,
    'host': remote_ip_address,
    'username': username,
    'password': password,
    'port': port,
}

local_fortigate = {
    'device_type': device_type,
    'host': local_ip_address,
    'username': username,
    'password': password,
    'port': port,
}

## Generate PSK
def generate_key(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in
    range(length))

VPN_PSK = generate_key(key_length)

## Generate command set
REMOTE_COMMANDS = ['config vpn ipsec phase1-interface',
                      'edit "<VPN NAME>"',
                      'set psk ' + VPN_PSK]

LOCAL_COMMANDS = ['config vpn ipsec phase1-interface',
                     'edit "<VPN NAME>"',
                     'set psk ' + VPN_PSK]

## Start SSH connection (remote, local)
SSH_REMOTE_FORTIGATE = ConnectHandler(**remote_fortigate)
SSH_LOCAL_FORTIGATE = ConnectHandler(**local_fortigate)

## Send SSH commands (remote, local)
SSH_REMOTE_FORTIGATE.send_config_set(REMOTE_COMMANDS)
time.sleep(5)
SSH_LOCAL_FORTIGATE.send_config_set(LOCAL_COMMANDS)

## Stop SSH connection (remote, local)
SSH_REMOTE_FORTIGATE.disconnect()
SSH_LOCAL_FORTIGATE.disconnect()