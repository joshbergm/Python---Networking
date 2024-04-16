##############################################################
##      - Config backup script via FortiGate API            ##
##      - Author: Joshua Bergman                            ##
##      - Version: 0.1 (Draft)                              ##
##      - Date: 22-03-2024                                  ##
##############################################################

## Import libraries
from fortigate_api import FortiGateAPI ## FortiGate API
import getpass ## Ability to get token without displaying chars in the terminal
from datetime import datetime, timedelta ## Get current time
import os ## Needed for getting files
import requests ## Needed for sending API's
import csv ## Needed for CSV file handling

## Define variables
vdom = 'root'
delete_days = 90

## Get username for file handling
pc_username = getpass.getuser()

## Get current time for file handling
date = datetime.now().strftime('%d_%m_%Y')

## Set default path for file handling
file_path = os.path.join("/volume1/Back-up/FortiGate/")

## Define source file
ip_address_list_input = os.path.join(file_path, "config/iplist.csv")

## Function to delete files older than x days
def delete_backup_files_older_than_x_days():
    current_time = datetime.now()
    delta = timedelta(days=delete_days)

    ## Loop trough files and check if there are any older than x days
    for files in os.walk(file_path,"Backups/"+hostname):
        for backup in files:
            file_creation_date = datetime.fromtimestamp(os.path.getctime(config_backup_output))
            if current_time - file_creation_date > delta:
                os.remove(file_path,"Backups",hostname)

## Loop trough IP's
with open(ip_address_list_input, 'r') as ip_address_list:
    csv_reader = csv.reader(ip_address_list, delimiter=';')

    next(csv_reader, None)

    for row in csv_reader:
        ip = row[0]
        port = row[1]
        token = row[2]
        
        ## Assemble API request
        ### Create a session
        client = requests.session()

        ### Disable SSL verification
        client.verify = False

        ## Get hostname for file name
        hostname_api_request = (f'https://{ip}:{port}/api/v2/cmdb/system/global?scope=vdom&vdom={vdom}&access_token={token}')

        ## Define API request URL
        backup_api_request =(f'https://{ip}:{port}/api/v2/monitor/system/config/backup?scope=vdom&vdom={vdom}&access_token={token}')

        ### Send GET request
        backup_file_response = client.get(backup_api_request)
        hostname_response = client.get(hostname_api_request)
        
        ## Extract hostname from JSON query
        if hostname_response.ok:
            hostname_data = hostname_response.json()
            hostname = hostname_data.get("results", {}).get("hostname")

        ## Define backup path
        config_backup_output = os.path.join(file_path, "Backups/"+hostname+"/")

        ## Create folder with hostname if not exists
        if not os.path.exists(config_backup_output):
            os.makedirs(config_backup_output)

        ## Write backup content to file
        if backup_file_response.ok:
            with open(config_backup_output + f'{hostname}_backup_{date}.conf', 'wb') as f:
                f.write(backup_file_response.content)
            print("Config file saved succesfully as: " + config_backup_output + f"{hostname}_backup_{date}.conf")
        else:
            print("Failed to retrieve config file, Status code: ", backup_file_response.status_code)

        ## Delete files older than specified
        delete_backup_files_older_than_x_days()