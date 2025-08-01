# cleanup.py
from utils import get_device_list, get_credentials, create_device, connect_and_run
from netmiko import ConnectHandler
import time 

def run_cleanup():
    # Module header: displays which operation is running when selected from driver script
    print("""
    ----------------------
    Filesystem Cleanup v1.0.1
    ----------------------
    """)
    print(f"\nWarning: Delete command is irreversible and will remove files from device filesystem.\n")

    # Define variables: device list, credentials, and cleanup command
    # Warning: Delete command is irreversible and will remove files from device filesystem.
    devices = get_device_list()
    creds = get_credentials()
    cleanup_cmd = "del /for /recur c2960c405-universalk9-mz.152-7.E12.bin"

    # Record start time for measuring runtime
    start = time.perf_counter()
    
    # --- Confirmation Before Deletion ---
    confirm = input(f'\nCommand to be sent is "{cleanup_cmd}". Proceed with deletion? (yes/no): ').strip().lower()
    if confirm != 'yes':
        print("Deletion aborted. Script terminated.")
        return
    
    # Loop through each device, establish connection and execute cleanup command
    # Print status message for each device, showing device IP and the command output
    for ip in devices:
        device = create_device(ip, creds)
        print(f"\nCleaning up device {ip}")
        try:
            with ConnectHandler(**device) as conn:
                output = conn.send_command_timing(cleanup_cmd)
                print(output)
                print(" Files removed successfully.")
        except Exception as err:
            print(f"[ERROR: {ip}] {err}")

    # Print total execution time
    print(f"\nScript finished in: {round(time.perf_counter() - start, 2)} seconds.")
    
# Only runs if you execute this script directly
if __name__ == "__main__":
    run_cleanup()





