import csv ##CSV file handling
import os ##OS file handling
import getpass ##OS username handling
from netmiko import ConnectHandler ##SSH handling
from netmiko import SCPConn ##SCP handling

## Device system variables
mt_username = input("Username: ")
mt_password = getpass.getpass(prompt="Password: ", stream=None)
mt_ipaddress = input("IP address: ")

## Define CSV variables
csv_delimiter = ';'

## Define Mikrotik variables
device_type = 'mikrotik_routeros'
port = '22'

## Define device model
mikrotik = {
        'device_type': device_type,
        'host': mt_ipaddress,
        'username': mt_username,
        'password': mt_password,
        'port': port,
    }

## Get current username
pc_username = getpass.getuser()

## Define file variables
base_file_path = os.path.join("c:/Users/", pc_username, "Documents/Python-Networking/Mikrotik/")
input_csv_file = os.path.join(base_file_path, "mt_config.csv")
output_folder = os.path.join(base_file_path, 'Configbackup/')

## Loop trough l2tp clients
with open(input_csv_file, 'r') as configlist:
    csv_reader = csv.reader(configlist, delimiter=csv_delimiter) ##Define path and delimiter
    next(csv_reader, None) ##Skip first line where names are defined
    
    try: ##Connect to Mikrotik
        ssh_session = ConnectHandler(**mikrotik)
        print('Successfully logged in')
    
    except Exception as e: ##Return error when error occurs.
        print(f"An error occurred for: {mt_ipaddress}", e)
        exit ##Stop script if connection fails

    ## Create loop
    for row in csv_reader:
        ## Define rows
        ethernet3_address = row[0]
        ethernet3_network = row[1]
        firewall_subnet = row[2]
        ppp_username = row[3]
        ppp_password = row[4]
        filename = row[5]
        filepass = row[6]
        
        commands = [
            '',
            '',
            ''
        ]
        
        ## Send commands to device
        ssh_session.send_config_set(commands)
        print(f'Config done for: {ppp_username}')
        
        ## Define remote file
        remote_file = filename
        
        ## Export backup file to share
        ssh_session.send_command(f'/system backup save name={filename} password={filepass}')
        print(f'Backup created for: {filename}')
        scp_session = SCPConn(ssh_session)
        scp_session.scp_get_file(remote_file, output_folder)
        print(f'Backup exported to: {output_folder}/{filename}')
        
    ## Disable SCP
    ssh_session.send_command('/ip service disable scp')
    
    ## Disconnect
    ssh_session.disconnect()
    print('Done, logged out successfully')