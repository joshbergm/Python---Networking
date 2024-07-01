## Import dependencies
import csv ##CSV file handling
import requests ##API handling
import os ##OS file handling
import getpass ##OS username handling
import urllib3 ##Suppress SSL warning

## Device variables
fortigate_api_token = 'xxxxxxxxxxxxxxxxxxxxxxx'
fortigate_ip = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
fortigate_port = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'

## Script variables
csv_delimiter = ';'
windowsusername = getpass.getuser()
apisession = requests.session()
apiclient = requests.post()

## Disable SSL verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
apisession.verify = False

## API header
api_header = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {fortigate_api_token}'
}

## Default API prefix
defaultapiurl = f'https://{fortigate_ip}:{fortigate_port}/api/v2'

## Specific API prefixes
### Global system settings
...

### Interfaces
interfaceapi = f'{defaultapiurl}/cmdb/sytem/interface'

### VPN's
ipsecvpnapi = f'{defaultapiurl}/cmdb/vpn.ipsec'
phase1_ipsecvpnapi = f'{ipsecvpnapi}/phase1'
phase1interface_ipsecvpnapi = f'{ipsecvpnapi}/phase1-interface'
phase2_ipsecvpnapi = f'{ipsecvpnapi}/phase2'
phase2interface_ipsecvpnapi = f'{ipsecvpnapi}/phase2-interface'

### Addresses
addressapi = f'{defaultapiurl}/cmdb/firewall/address'

### Policies
policyapi = f'{defaultapiurl}/cmdb/firewall/policy'

## Functions
### Create interface
def create_interface(api_url, api_body, headers):
    response = apisession.post(api_url, json=api_body, headers=headers)
    return response

def create_vpn(api_url, api_body, headers):
    response = apisession.post(api_url, json=api_body, headers=headers)
    return response

def create_address(api_url, api_body, headers):
    response = apisession.post(api_url, json=api_body, headers=headers)
    return response

def create_policy(api_url, api_body, headers):
    response = apisession.post(api_url, json=api_body, headers=headers)
    return response

## File locations
### Base file path
config_file_path = os.path.join(f'c:/Users/{windowsusername}/Documents/Python-Networking/FortiGate/Configtool')
csv_config = os.path.join(f'{config_file_path}/settings.txt')
csv_interfaces = os.path.join(f'{config_file_path}/interfaces.csv')
csv_vpns = os.path.join(f'{config_file_path}/vpns.csv')
csv_addresses = os.path.join(f'{config_file_path}/addresses.csv')
csv_policies = os.path.join(f'{config_file_path}/policies.csv')

## Modules
### Global system settings
##################################################################

### Interfaces
with open(csv_interfaces, 'r') as interfaces:
    csv_reader = csv.reader(interfaces, delimiter=csv_delimiter)
    next(csv_reader, None)

    #### CSV values
    for row in csv_reader:
        interface_name = row[0] ## Name as string format
        interface_vdom = row[1] ## Default = root
        interface_member = row[2] ## Interface name from LACP
        interface_vlanid = int(row[3]) ## VLAN ID as integer format
        interface_lacp_mode = row[4] ## statis / passive / active
        interface_lacp_speed = row[5] ## fast / slow
        interface_mode = row[6] ## static / DHCP / PPPoE
        interface_ip = row[7] ## x.x.x.x/y (1.1.1.1/32)
        interface_access = row[8] ## HTTPS PING, space between protcols
        interface_status = row[9] ## op / down
        interface_role = row[10] ## lan / wan / dmz / unspecified
        interface_pppoe_username = row[11] ## Only necesarry if mode = PPPoE
        interface_pppoe_password = row[12] ## Only necesarry if mode = PPPoE

        ##### API Body
        interfaceapi_body = {
            "data": {
                "name": interface_name,
                "vdom": interface_vdom,
                "mode": interface_mode,
                "ip": interface_ip,
                "allowaccess": interface_access,
                "username": interface_pppoe_username,
                "password": interface_pppoe_password,
                "status": interface_status,
                "vlanid": interface_vlanid,
                "member": [
                    {
                        "interface-name": interface_member
                    }
                ],
                "lacp-mode": interface_lacp_mode,
                "lacp-speed": interface_lacp_speed,
                "role": interface_role
                }
            }

        interfaceapi_request = create_interface(interfaceapi, interfaceapi_body, api_header)
        if interfaceapi_request.status_code == 200:
            print(f'Interface creation for {interface_name} succesfull')
        else:
            print(f'Interface creation for {interface_name} failed')

### VPN's
with open(csv_vpns, 'r') as vpns:
    csv_reader = csv.reader(vpns, delimiter=csv_delimiter)
    next(csv_reader, None)
    ######################################################################

### Addresses
with open(csv_addresses, 'r') as addresses:
    csv_reader = csv.reader(vpns, delimiter=csv_delimiter)
    next(csv_reader, None)

    for row in csv_reader:
        address_name = row[0]
        address_subnet = row[1] ## if type is ipmask
        address_type = row[2] ##ipmask, iprange, fqdn, geography
        address_start_ip = row[3] ## if type is iprange
        address_end_ip = row[4] ##if type is iprange
        address_fqdn = row[5] ## if type is fqdn
        address_wildcard_fqdn = row[6] ##if type is fqdn
        address_geography = row[7] ## if type is geography, country code e.g. NL
        address_cache_ttl = int(row[8]) ## set time in seconds for cache, 0 - 86400 
        address_interface = row[9]
        address_comment = row[10]
        address_vdom = row[11] ## default is root

        addressapi_body = {
                "params": {
                    "vdom": address_vdom
                },
                "data": {
                    "name": address_name,
                    "subnet": address_subnet,
                    "type": address_type,
                    "start-ip": address_start_ip,
                    "end-ip": address_end_ip,
                    "fqdn": address_fqdn,
                    "country": address_geography,
                    "wildcard-fqdn": address_wildcard_fqdn,
                    "cache-ttl": address_cache_ttl,
                    "comment": address_comment,
                    "associated-interface": {
                        "q_origin_key": address_interface
                    },
                }
            }
    
        addressapi_request = create_address(addressapi, addressapi_body, api_header)
        if addressapi_request.status_code == 200:
            print(f'Address creation for {address_name} succesfull')
        else:
            print(f'Address creation for {address_name} failed')

### Policies
with open(csv_policies, 'r') as policies:
    csv_reader = csv.reader(policies, delimiter=csv_delimiter)
    next(csv_reader, None)

    #### CSV values
    for row in csv_reader:
        policy_name = row[0]
        policy_source_interface = row[1]
        policy_destination_interface = row[2]
        policy_source_address = row[3]
        policy_destination_address = row[4] 
        policy_schedule = row[5] ## always / other...
        policy_service = row[6] ## ALL / other...
        policy_action = row[7] ## accept / deny
        policy_nat = row[8] ## enable / disable
        policy_logging = row[9] ## all / ''
        policy_status = row[11] ## enable / disable
        policy_vdom = row[12] ## default = root

        ##### API Body
        policyapi_body = {
            "params": {
                "vdom": policy_vdom
            },
            "data": {
                "status": policy_status,
                "name": policy_name,
                "srcintf": [
                    {
                        "name": policy_source_interface
                    }
                ],
                "dstintf": [
                    {
                        "name": policy_destination_interface
                    }
                ],
                "action": policy_action,
                "srcaddr": [
                    {
                        "name": policy_source_address
                    }
                ],
                "dstaddr": [
                    {
                        "name": policy_destination_address
                    }
                ],
                "schedule": {
                    "q_origin_key": policy_schedule
                },
                "service": [
                    {
                        "name": policy_service
                    }
                ],
                "logtraffic": policy_logging,
                "nat": policy_nat
            }
        }