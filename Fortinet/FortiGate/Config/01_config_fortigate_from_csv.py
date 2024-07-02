import csv  # CSV file handling
import requests  # API handling
import os  # OS file handling
import getpass  # OS username handling
import urllib3  # Suppress SSL warning

# Device variables
fortigate_api_token = ''
fortigate_ip = ''
fortigate_port = ''

# Script variables
csv_delimiter = ';'
windowsusername = getpass.getuser()
apisession = requests.session()

# Disable SSL verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
apisession.verify = False

# API header
api_header = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {fortigate_api_token}'
}

# Default API prefix
defaultapiurl = f'https://{fortigate_ip}:{fortigate_port}/api/v2'

# Specific API prefixes
interfaceapi = f'{defaultapiurl}/cmdb/system/interface'
ipsecvpnapi = f'{defaultapiurl}/cmdb/vpn.ipsec'
phase1_ipsecvpnapi = f'{ipsecvpnapi}/phase1'
phase1interface_ipsecvpnapi = f'{ipsecvpnapi}/phase1-interface'
phase2_ipsecvpnapi = f'{ipsecvpnapi}/phase2'
phase2interface_ipsecvpnapi = f'{ipsecvpnapi}/phase2-interface'
zoneapi = f'{defaultapiurl}/cmdb/system/zone'
addressapi = f'{defaultapiurl}/cmdb/firewall/address'
policyapi = f'{defaultapiurl}/cmdb/firewall/policy'

# Functions
def create_interface(api_url, api_body, headers):
    response = apisession.post(api_url, json=api_body, headers=headers)
    return response

def create_vpn(api_url, api_body, headers):
    response = apisession.post(api_url, json=api_body, headers=headers)
    return response

def create_zone(api_url, api_body, headers):
    response = apisession.post(api_url, json=api_body, headers=headers)
    return response

def create_address(api_url, api_body, headers):
    response = apisession.post(api_url, json=api_body, headers=headers)
    return response

def create_policy(api_url, api_body, headers):
    response = apisession.post(api_url, json=api_body, headers=headers)
    return response

# File locations
config_file_path = os.path.join(f'c:/Users/{windowsusername}/Documents/Python-Networking/FortiGate/Configtool')

csv_config = os.path.join(f'{config_file_path}/settings.txt')
csv_interfaces = os.path.join(f'{config_file_path}/interfaces.csv')
csv_vpns = os.path.join(f'{config_file_path}/vpns.csv')
csv_zones = os.path.join(f'{config_file_path}/zones.csv')
csv_addresses = os.path.join(f'{config_file_path}/addresses.csv')
csv_policies = os.path.join(f'{config_file_path}/policies.csv')

# Modules
if input("Do you want to create interfaces? (y/n): ").lower() == 'y':
    with open(csv_interfaces, 'r') as interfaces:
        csv_reader = csv.reader(interfaces, delimiter=csv_delimiter)
        next(csv_reader, None)

        for row in csv_reader:
            interface_name = row[0]
            interface_vdom = row[1] if row[1] else 'root'
            interface_member = row[2]
            interface_vlanid = int(row[3])
            interface_lacp_mode = row[4]
            interface_lacp_speed = row[5]
            interface_mode = row[6]
            interface_ip = row[7]
            interface_access = row[8]
            interface_status = row[9]
            interface_role = row[10]
            interface_pppoe_username = row[11]
            interface_pppoe_password = row[12]

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

            interfaceapi_request = create_interface(interfaceapi, interfaceapi_body, api_header)
            if interfaceapi_request.status_code == 200:
                print(f'Interface creation for {interface_name} successfull')
            else:
                print(f'Interface creation for {interface_name} failed, code: {interfaceapi_request.status_code}')

if input("Do you want to create VPNs? (y/n): ").lower() == 'y':
    with open(csv_vpns, 'r') as vpns:
        csv_reader = csv.reader(vpns, delimiter=csv_delimiter)
        next(csv_reader, None)

        for row in csv_reader:
            # Implement VPN creation similarly
            pass

if input("Do you want to create zones? (y/n): ").lower() == 'y':
    with open(csv_zones, 'r') as zones:
        csv_reader = csv.reader(zones, delimiter=csv_delimiter)
        next(csv_reader, None)

        for row in csv_reader:
            zone_name = row[0]
            zone_description = row[1]
            zone_intrazone = row[2]
            zone_interface = row[3]
            zone_vdom = row[4] if row[4] else 'root'

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

            zoneapi_request = create_zone(zoneapi, zoneapi_body, api_header)
            if zoneapi_request.status_code == 200:
                print(f'Zone creation for {zone_name} successfull')
            else:
                print(f'Zone creation for {zone_name} failed, code: {zoneapi_request.status_code}')

if input("Do you want to create addresses? (y/n): ").lower() == 'y':
    with open(csv_addresses, 'r') as addresses:
        csv_reader = csv.reader(addresses, delimiter=csv_delimiter)
        next(csv_reader, None)

        for row in csv_reader:
            address_name = row[0]
            address_subnet = row[1]
            address_type = row[2]
            address_start_ip = row[3]
            address_end_ip = row[4]
            address_fqdn = row[5]
            address_wildcard_fqdn = row[6]
            address_geography = row[7]
            address_cache_ttl = int(row[8])
            address_interface = row[9]
            address_comment = row[10]
            address_vdom = row[11] if row[11] else 'root'

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

            addressapi_request = create_address(addressapi, addressapi_body, api_header)
            if addressapi_request.status_code == 200:
                print(f'Address creation for {address_name} successfull')
            else:
                print(f'Address creation for {address_name} failed, code: {addressapi_request.status_code}')

if input("Do you want to create policies? (y/n): ").lower() == 'y':
    with open(csv_policies, 'r') as policies:
        csv_reader = csv.reader(policies, delimiter=csv_delimiter)
        next(csv_reader, None)

        for row in csv_reader:
            policy_name = row[0]
            policy_source_interface = row[1]
            policy_destination_interface = row[2]
            policy_source_address = row[3]
            policy_destination_address = row[4]
            policy_schedule = row[5]
            policy_service = row[6]
            policy_action = row[7]
            policy_nat = row[8]
            policy_logging = row[9]
            policy_status = row[11]
            policy_vdom = row[12] if row[12] else 'root'

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

            policyapi_request = create_policy(policyapi, policyapi_body, api_header)
            if policyapi_request.status_code == 200:
                print(f'Policy creation for {policy_name} successfull')
            else:
                print(f'Policy creation for {policy_name} failed, code: {policyapi_request.status_code}')