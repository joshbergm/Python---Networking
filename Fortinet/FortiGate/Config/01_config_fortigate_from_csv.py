import csv  # CSV file handling
import requests  # API handling
import os  # OS file handling
import getpass  # OS username handling
import urllib3  # Suppress SSL warning

# Device variables
fortigate_api_token = '' ## Specify API token generated in FortiGate Administrators
fortigate_ip = '' ## Specify FortiGate IP with HTTPS access
fortigate_port = '' ## Specify FortiGate HTTPS port

# Script variables
csv_delimiter = ';' ## Specify CSV delimiter for file handling
windowsusername = getpass.getuser() ## Get logged in user for file handling
apisession = requests.session()

# Disable SSL verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) ## Disable invallid SSL warning
apisession.verify = False

# API header
api_header = {
    'Accept': 'application/json', ## Specify API format
    'Authorization': f'Bearer {fortigate_api_token}' ## Specify Bearer token
}

# Default API prefix
defaultapiurl = f'https://{fortigate_ip}:{fortigate_port}/api/v2'

## Specific API prefixes
### Interface API
interfaceapi = f'{defaultapiurl}/cmdb/system/interface'
### Zone API
zoneapi = f'{defaultapiurl}/cmdb/system/zone'
### Address API
addressapi = f'{defaultapiurl}/cmdb/firewall/address'
### Policy API
policyapi = f'{defaultapiurl}/cmdb/firewall/policy'

## Functions
### Interface function
def create_interface(api_url, api_body, headers):
    response = apisession.post(api_url, json=api_body, headers=headers)
    return response

### Zone function
def create_zone(api_url, api_body, headers):
    response = apisession.post(api_url, json=api_body, headers=headers)
    return response

### Address function
def create_address(api_url, api_body, headers):
    response = apisession.post(api_url, json=api_body, headers=headers)
    return response

### Policy function
def create_policy(api_url, api_body, headers):
    response = apisession.post(api_url, json=api_body, headers=headers)
    return response

## File locations
config_file_path = os.path.join(f'c:/Users/{windowsusername}/Documents/Python-Networking/FortiGate/Configtool')

### Interface CSV file
csv_interfaces = os.path.join(f'{config_file_path}/interfaces.csv')

### Zone CSV file
csv_zones = os.path.join(f'{config_file_path}/zones.csv')

### Address CSV file
csv_addresses = os.path.join(f'{config_file_path}/addresses.csv')

### Policy CSV file
csv_policies = os.path.join(f'{config_file_path}/policies.csv')

## Modules
### Interface module
if input("Do you want to create interfaces? (y/n): ").lower() == 'y':
    with open(csv_interfaces, 'r') as interfaces:
        csv_reader = csv.reader(interfaces, delimiter=csv_delimiter)
        next(csv_reader, None)

        for row in csv_reader:
            interface_name = row[0] ## Interface name
            interface_vdom = row[1] if row[1] else 'root' ## If value is blank, use root as default
            interface_member = row[2] ## Interface member e.g. LACP bundle
            interface_vlanid = int(row[3]) ##Interface VLAN id
            interface_lacp_mode = row[4] ## active / passive
            interface_lacp_speed = row[5] ## fast / slow
            interface_mode = row[6] ## static / DHCP / PPPoE
            interface_ip = row[7] ## e.g. 1.1.1.1/32
            interface_access = row[8] ## PING HTTP HTTPS SSH
            interface_status = row[9] ## up / down
            interface_role = row[10] ## lan / wan / dmz / undefined
            interface_pppoe_username = row[11] ## e.g. internet
            interface_pppoe_password = row[12] ## e.g. internet

            interfaceapi_body = {
                "name": interface_name,
                "vdom": interface_vdom,
                "mode": interface_mode,
                "ip": interface_ip,
                "allowaccess": interface_access,
                "username": interface_pppoe_username,
                "password": interface_pppoe_password,
                "status": interface_status,
                "vlanid": interface_vlanid,
                "interface": interface_member,
                "lacp-mode": interface_lacp_mode,
                "lacp-speed": interface_lacp_speed,
                "role": interface_role
                }
            
            #### Send request and print status, throw error if status code is not 200
            interfaceapi_request = create_interface(interfaceapi, interfaceapi_body, api_header) ## Call function named 'create_interface' and define values
            if interfaceapi_request.status_code == 200:
                print(f'Interface creation for {interface_name} successfull')
            else:
                print(f'Interface creation for {interface_name} failed, code: {interfaceapi_request.status_code}') ## Print HTTP error status code

### Zone module
if input("Do you want to create zones? (y/n): ").lower() == 'y':
    with open(csv_zones, 'r') as zones:
        csv_reader = csv.reader(zones, delimiter=csv_delimiter)
        next(csv_reader, None)

        for row in csv_reader:
            zone_name = row[0] ## Zone name
            zone_description = row[1] ## Zone descriptions
            zone_intrazone = row[2] ## Zone intrazone traffic allow / deny
            zone_interface = row[3] ## Zone assigned interfaces
            zone_vdom = row[4] if row[4] else 'root' ## If value is blank use root as default

            zoneapi_body = {
                "params": {
                    "vdom": zone_vdom
                },
                "data": {
                    "name": zone_name,
                    "description": zone_description,
                    "intrazone": zone_intrazone,
                    "interface": [
                        {
                            "interface-name": zone_interface
                        }
                    ]
                }
            }

            #### Send request and print status, throw error if status code is not 200
            zoneapi_request = create_zone(zoneapi, zoneapi_body, api_header) ## Call function named 'create_zone' and define values
            if zoneapi_request.status_code == 200:
                print(f'Zone creation for {zone_name} successfull')
            else:
                print(f'Zone creation for {zone_name} failed, code: {zoneapi_request.status_code}') ## Print HTTP error status code

### Address module
if input("Do you want to create addresses? (y/n): ").lower() == 'y':
    with open(csv_addresses, 'r') as addresses:
        csv_reader = csv.reader(addresses, delimiter=csv_delimiter)
        next(csv_reader, None)

        for row in csv_reader:
            address_name = row[0] ## Address name
            address_subnet = row[1] ## Address subnet e.g. 1.1.1.1/32
            address_type = row[2] ## Address type e.g. ipmask, iprange, fqdn, wildcard-fqdn, geography
            address_start_ip = row[3] ## Specify start IP if type is iprange
            address_end_ip = row[4] ## Specify end IP if type is iprange
            address_fqdn = row[5] ## Speciffy FQDN if type is fqdn
            address_wildcard_fqdn = row[6] ## Specify wildcard fqdn if type is fqdn
            address_geography = row[7] ## Specify country code e.g. NL
            address_cache_ttl = int(row[8]) ## Specify cache TTL in seconds between 0 - 86400
            address_interface = row[9] ## Specify address interface or zone
            address_comment = row[10] ## Specify comment
            address_vdom = row[11] if row[11] else 'root' ## If value is empty use vdom root as default

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
                    "associated-interface": address_interface
                }
            }

            #### Send request and print status, throw error if status code is not 200
            addressapi_request = create_address(addressapi, addressapi_body, api_header) ## Call function named 'create_address' and define values
            if addressapi_request.status_code == 200:
                print(f'Address creation for {address_name} successfull')
            else:
                print(f'Address creation for {address_name} failed, code: {addressapi_request.status_code}') ## Print HTTP error status code

### Policy module
if input("Do you want to create policies? (y/n): ").lower() == 'y':
    with open(csv_policies, 'r') as policies:
        csv_reader = csv.reader(policies, delimiter=csv_delimiter)
        next(csv_reader, None)

        for row in csv_reader:
            policy_name = row[0] ## Policy name
            policy_source_interface = row[1] ## Policy source interface
            policy_destination_interface = row[2] ## Policy destination interface
            policy_source_address = row[3] ## Policy source address
            policy_destination_address = row[4] ## Policy destination address
            policy_schedule = row[5] if row[5] else 'always' ## If value is blank use always as default
            policy_service = row[6] ## Policy service e.g. SSH
            policy_action = row[7] ## accept / deny
            policy_nat = row[8] ## enable / disable
            policy_logging = row[9] ## .....
            policy_status = row[11] ## enable / disable
            policy_vdom = row[12] if row[12] else 'root' ## If value is blank use vdom root as default

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
                    "schedule": policy_schedule,
                    "service": [
                        {
                            "name": policy_service
                        }
                    ],
                    "logtraffic": policy_logging,
                    "nat": policy_nat
                }
            }

            #### Send request and print status, throw error if status code is not 200
            policyapi_request = create_policy(policyapi, policyapi_body, api_header) ## Call function named 'create_policy' and define values
            if policyapi_request.status_code == 200:
                print(f'Policy creation for {policy_name} successfull')
            else:
                print(f'Policy creation for {policy_name} failed, code: {policyapi_request.status_code}') ## Print HTTP error status code