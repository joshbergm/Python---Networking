import csv ##CSV file handling
import os ##OS file handling
import getpass ##OS username handling
from netmiko import ConnectHandler ##SSH handling
import ftplib ## FTP handling

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
base_file_path = os.path.join("T:/ICT/Netwerk/Mikrotik/")
input_csv_file = os.path.join(base_file_path, "mt_config.csv")
output_folder = os.path.join(base_file_path, 'Configbackup/')

## Loop trough l2tp clients
with open(input_csv_file, 'r') as configlist:
    csv_reader = csv.reader(configlist, delimiter=csv_delimiter) ##Define path and delimiter
    next(csv_reader, None) ##Skip first line where names are defined
    
    ## Create SSH Session
    ssh_session = ConnectHandler(**mikrotik)

    ## Create loop
    for row in csv_reader:
        ## Define rows
        ethernet3_address = row[0]
        ethernet3_network = row[1]
        ethernet3_netmask = row [2]
        firewall_subnet = row[3]
        ppp_username = row[4]
        ppp_password = row[5]
        filename = row[6]
        filepass = row[7]
        
        commands = [
            f'/interface l2tp-client set 0 user={ppp_username} password={ppp_password}',
            f'/ip address set numbers=1 address={ethernet3_address} network={ethernet3_network} netmask={ethernet3_netmask}',
            f'/ip firewall filter set numbers=6 dst-address={firewall_subnet}',
            f'/ip firewall filter set numbers=11 dst-address={firewall_subnet}'
        ]
        
        ## Send commands to device
        ssh_session.send_config_set(commands)
        print(f'Config done for: {ppp_username}')
        
        ## Define remote file
        remote_file = f'config{filename}.backup'
        
        ## Export backup file to folder
        ssh_session.send_command(f'/system backup save name={filename} password={filepass}')
        print(f'Backup created for: {filename}')
        
        output_file = os.path.join(f'{output_folder}/{filename}.backup')
        
        with ftplib.FTP(mt_ipaddress, mt_username, mt_password) as ftp:
            with open (output_file, 'wb') as local_file:
                ftp.retrbinary('RETR ' + remote_file, local_file.write)
                print(f'Backup exported to: {output_folder}/{filename}.backup')
    
    ## Disconnect
    ssh_session.disconnect()
    print('Done, logged out successfully')