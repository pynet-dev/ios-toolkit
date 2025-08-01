# ios_scp.py
from utils import get_device_list, get_credentials, create_device
from netmiko import ConnectHandler, file_transfer
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time
import os

# Define file transfer perameters: source and destination file names, direction, and target filesystem
source_file = "c:/python-scripts/ios-automation/bin/c2960c405-universalk9-mz.152-7.E12.bin"
destination_file = "c2960c405-universalk9-mz.152-7.E12.bin"
direction = "put"
file_system = "flash:"

# Upload ios to a single device using predefined file transfer perameters
def upload_ios(ip, creds):
    device = create_device(ip,creds)
    try:
        connection = ConnectHandler(**device)
        transfer_dict = file_transfer(
            connection,
            source_file=source_file,
            dest_file=destination_file,
            file_system=file_system,
            direction=direction,
            overwrite_file=True,
            verify_file=True,
        )
        connection.disconnect()
        # Print transfer status details based on file_transferred status, includes exception statement for error handling 
        if transfer_dict.get("file_transferred"):
            if transfer_dict.get("file_verified"):
                return f"{ip}: Transfer successful and verified."
            else:
                return f"{ip}: Transfer successful but verification failed!"
        elif transfer_dict.get("file_exists"):
            return f"{ip}: Skipped - file already exists"
        else:
            return f"{ip}: Skipped - unknown reason (check flash space or permissions)."
    except Exception as e:
        return f"{ip}: ERROR: {e}"
  
#  Main function to coordinate firmware uploads across all devices
def run_ios_scp():
    # Module header: displays which operation is running when selected from driver script
    print("""
    -------------------
    SCP Uploader v1.0.1
    -------------------
    """)
    # Check that the source files exists
    if not os.path.isfile(source_file):
        print(f"[ERROR] Source file '{source_file}' not found.")
        return
        
    # Define and device list and user credentials
    devices = get_device_list()
    creds = get_credentials()
    
    # Record start time for measuring runtime
    start = time.perf_counter()
    
    # Print start message and total device count
    print(f"\nStarting SCP transfers to {len(devices)} devices...\n")
    
    # Limit number of concurrent threads to avoid overloading system or network 
    max_workers = min(5, len(devices))
        
    # Create shared progress bar and collect results from each transfer
    with tqdm (total=len(devices), desc="SCP Upload", unit="device") as pbar:
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(upload_ios, ip, creds) for ip in devices}
            for future in as_completed(futures):
                result = future.result()
                results.append(result) # Used to save results to a log file (Will implement later)
                pbar.update(1)
                
    # Print each result on its own line AFTER the progress bar completes
    print()  # Adds spacing between the bar and results
    for result in results:
        print(result)            
    
    # Print summary and total time 
    print(f"\nAll uploads complete in {round(time.perf_counter() - start, 2)} seconds.")
    
# Only runs if you execute this script directly
if __name__ == "__main__":
    run_ios_scp()
