# Mikrotik

## Introduction
Documentation page for Mikrotik scripts.

### Index

- [01 - Create L2TP users from batch](#01---create-l2tp-users-from-batch)
- [02 - Create L2TP users from batch with PMP](#02---create-l2tp-users-from-batch-pmp)

---

#### 01 - Create L2TP users from batch

#### Important !
> create a file named l2tpclients.csv (with CSV format and ; as delimiter), in the directory: c:/Users/%username%Documents/Python-Networking/Mikrotik/

Get user input such as username, password and IP to connect to Mikrotik device later in script.

---
<br>

```python
## Device system variables
mt_username = input("Username: ")
mt_password = getpass.getpass(prompt="Password: ", stream=None)
mt_host = input("IP address: ")
```
<br>

Set device type to Mikrotik so Netmiko knows how to process commands to device.

```python
## Define Mikrotik variables
device_type = 'mikrotik_routeros'
port = '22'
```
<br>

Get username from currently logged in user for file handling later on in script.

```python
## Get current username
pc_username = getpass.getuser()
```
<br>

Define file location for file handling later on in script.

```python
## Define file variables
base_file_path = os.path.join("c:/Users/", pc_username, "Documents/Python-Networking/Mikrotik/")
input_csv_file = os.path.join(base_file_path, "l2tpclients.csv")
```
<br>

Get CSV file from file location and define delimiter.

```python
## Loop trough l2tp clients
with open(input_csv_file, 'r') as configlist:
    csv_reader = csv.reader(configlist, delimiter=';') ##Define path and delimiter
    next(csv_reader, None) ##Skip first line where names are defined
```
<br>

Try logging in to Mikrotik device with specified device type, username, password, ip and port from earlier.

```python
try: ##Connect to Mikrotik
    net_connect = ConnectHandler(**mikrotik)
    print('Successfully logged in')

except Exception as e: ##Return error when error occurs.
    print("An error occurred for: ", mt_host, e)
    exit ##Stop script if connection fails
```
<br>

Read CSV file line by line and use values later on in script.

```python
## Create loop
for row in csv_reader:
    ## Define rows
    name = row[0]
    password = row[1]
    dst_address = row[2]
```
<br>

Static values for creating L2TP PPP Secret

```python
## L2TP Client
service = 'any'
profile = 'vpn-profile'
```
<br>

Combine name with 'L2TP-' for naming convention

```python
## L2TP Server binding
l2tp_name = 'l2tp-' + name
user = name
```
<br>

Add static route to dial up PPP client.

```python
## IP Route
gateway = l2tp_name
```
<br>

Create command set with values from CSV file and combined values from earlier in the script.

```python
## Define commands
commands = [
    'ppp secret add' + ' name=' + name + ' password=' + password + ' service=' + service + ' profile=' profile,
    'interface l2tp-server add' + ' name=' + l2tp_name + ' user=' + user,
    'ip route add' + ' dst-address=' + dst_address + ' gateway=' + gateway
]
```
<br>

Send created commands for every line and return which client has been configured

```python
## Send commands and let user know which L2TP client is pushed
net_connect.send_config_set(commands)
print('Created: ' + l2tp_name)
```
<br>

Disconnect session after completion.

```python
## Disconnect
net_connect.disconnect()
print('Done, logged out successfully')
```

<br>

---

#### 02 - Create L2TP users from batch with PMP

File is almost completely the same as '01 - Create L2TP users from batch' but instead of specifying a password, password gets loaded dynamically from PMP (Password Manager Pro from Manage Engine)

File differences:

```python
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
```