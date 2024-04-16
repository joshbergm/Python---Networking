##############################################################
##      - Python script for backing up FortiGate            ##
##      - Author: Joshua Bergman                            ##
##      - Version: 0.1 (Draft)                              ##
##      - Date: 16-03-2024                                  ##
##############################################################

from netmiko import ConnectHandler
import datetime

fw = {'host': '<hostname>',
      'device_type': 'fortinet',
      'ip': '<ip>',
      'username': '<username>',
      'password': '<password>'}

net_connect = ConnectHandler(**fw)
output = net_connect.send_command('show full-configuration')

current_time = datetime.datetime.today().strftime('%Y_%m_%d')

with open('/paste/path/here' + str(fw['host']) + '_' + str(current_time) + '.cfg', 'w') as f:
    for line in output:
        f.write(line)