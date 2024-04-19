import csv ##CSV file handling
import os ##OS file handling
import getpass ##OS username handling
from netmiko import ConnectHandler ##SSH handling
import passwordmanpro_cli ##PMP Handling

## Device system variables
mt_username = input("Username: ")
mt_host = input("IP address: ")

## Retrieve password from PMP
pmp_resource = 'Mikrotik'
pmp_apikey = 'xxxxxxxxxxxxxxxx'
pmp_accound_id = 'admin'
pmp_url = '1.1.1.1'
pmp_port = '7272'

## Create request
pmp_password = passwordmanpro_cli.getSinglePassword(
    pmp_resource,
    pmp_apikey,
    skipSSLChecks=True
)

## Specify header with API key
pmp_header = {
    'AUTHTOKEN': pmp_apikey
}

## Create payload URL with specified values
pmp_payload_url = f'https://{pmp_url}:{pmp_port}/restapi/json/v1/resources/{pmp_resource}/accounts/{pmp_accound_id}/password'

## Define Mikrotik variables
device_type = 'mikrotik_routeros'
port = '22'

## Define device model
mikrotik = {
        'device_type': device_type,
        'host': mt_host,
        'username': mt_username,
        'password': pmp_password,
        'port': port,
    }

## Get current username
pc_username = getpass.getuser()

## Define file variables
base_file_path = os.path.join("c:/Users/", pc_username, "Documents/Python-Networking/Mikrotik/")
input_csv_file = os.path.join(base_file_path, "l2tpclients.csv")

## Loop trough l2tp clients
with open(input_csv_file, 'r') as configlist:
    csv_reader = csv.reader(configlist, delimiter=';') ##Define path and delimiter
    next(csv_reader, None) ##Skip first line where names are defined
    
    try: ##Connect to Mikrotik
        net_connect = ConnectHandler(**mikrotik)
        print('Successfully logged in')
    
    except Exception as e: ##Return error when error occurs.
        print("An error occurred for: ", mt_host, e)
        exit ##Stop script if connection fails

    ## Create loop
    for row in csv_reader:
        ## Define rows
        name = row[0]
        password = row[1]
        dst_address = row[2]
        
        ## L2TP Client
        service = 'any'
        profile = 'vpn-profile'

        ## L2TP Server binding
        l2tp_name = 'l2tp-' + name
        user = name

        ## IP Route
        gateway = l2tp_name
        
        ## Define commands
        commands = [
            'ppp secret add' + ' name=' + name + ' password=' + password + ' service=' + service + ' profile=' + profile,
            'interface l2tp-server add' + ' name=' + l2tp_name + ' user=' + user,
            'ip route add' + ' dst-address=' + dst_address + ' gateway=' + gateway
        ]
        
        net_connect.send_config_set(commands)
        print('Created: ' + l2tp_name)
        
    net_connect.disconnect()
    print('Done, logged out successfully')