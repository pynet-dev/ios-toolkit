from netmiko import ConnectHandler
from getpass import getpass

# Prompts user for zone number, builds path to zone file
def get_device_list():
    zone_path=('C:/python scripts/library/device/') + input \
    ('Enter zone number to load file for host addresses: ').strip() + ('.txt')

    # Loads and sanitizes lines from file (typically IP addresses)
    with open(zone_path) as file:
        return [line.strip() for line in file.readlines()]
    
# Prompts user for credentials and returns them as a dictonary 
def get_credentials():
    username = input("Enter username: ")
    return {
        "username": username,
        "password": getpass("Enter password: ")
    }

# Constructs a device dictionary to be used by Netmiko from an IP and credential set    
def create_device(ip, credentials):
    return {
        "device_type": "cisco_ios",
        "host": ip,
        "username": credentials["username"],
        "password": credentials["password"]
    }
    
# Executes a CLI command on the target device using Netmiko
# 'device' and 'command' are passed in from the calling script
# Returns the output, or an error message if the connection fails
def connect_and_run(device, command):
    try:
        with ConnectHandler(**device) as conn:
            return conn.send_command(command)
    except Exception as err:
        return f"[ERROR: {device['host']}] {err}"