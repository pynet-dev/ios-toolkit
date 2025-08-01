# verification.py
from utils import get_device_list, get_credentials, create_device, connect_and_run
import time
import re

# Parse the specific line containing the version and extract the version string
def extract_ios_version(output):
    match = re.search(r"Version (\S+),", output)
    if match: 
        return match.group(1)
    return "could not be determined. Verify network connection and credentials"

def run_verification():
    # Module header: displays which operation is running when selected from driver script
    print("""
    ------------------------
    IOS Verification v1.1.0
    ------------------------
    """)

    # Define variables: device list, user credentials, CLI command, and expected IOS version
    devices = get_device_list()
    creds = get_credentials()
    command = "show version"
    expected_version = "15.2(7)E12"

    # Record start time for measuring runtime
    start = time.perf_counter()

    # Loop through each device, connection and check firmware version
    # If the firmware matches, print that the device is up to date
    # If not, indicate the device is running an outdated version and show what version is currently running
    for ip in devices:
        device = create_device(ip, creds)
        print(f"\nChecking firmware for {ip}")
        output = connect_and_run(device, command)
        current_version = extract_ios_version(output)
        if expected_version in output:
            print(f"{ip} is running the latest firmware.")
        else:
            print(f"{ip} is NOT running the latest firmware. Currently running Version {current_version}.")

    # Print total execution time
    print(f"\nScript finished in: {round(time.perf_counter() - start, 2)} seconds.")

# Only runs if you execute this script directly
if __name__ == "__main__":
    run_verification()

