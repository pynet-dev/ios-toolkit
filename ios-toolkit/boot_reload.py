# boot_reload.py
from utils import get_device_list, get_credentials, create_device
from netmiko import ConnectHandler
import time

# Run boot system command and reload across multiple devices
def run_boot_and_reload():
    # Module header: displays which operation is running when selected from driver script
    print("""
    ---------------------------------
    Boot Path Update + Reload v1.0.1
    ---------------------------------
    """)
    # Define  device list, user credentials, and new boot path
    devices = get_device_list()
    creds = get_credentials()
    image_path = "boot system flash:/c2960c405-universalk9-mz.152-7.E12.bin"

    # Record start time for measuring runtime
    start = time.perf_counter()

    # --- First Pass: Set Boot Path ---
    # Loop through each device, apply boot path, and handle any errors
    for ip in devices:
        device = create_device(ip.strip(), creds)
        print(f"\nUpdating boot path for {ip.strip()}")

        try:
            with ConnectHandler(**device) as conn:
                output = conn.send_config_set([image_path])
                output += conn.save_config()
                print(output)
        except Exception as err:
            print(f"[ERROR: {ip.strip()}] {err}")

    # --- Confirmation Before Reload ---
    confirm = input("\n Proceed with reloading all devices? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Reload aborted.")
        return

    # --- Second Pass: Reload Devices ---
    # Loop through each device, issue reload command and handle any erros
    for ip in devices:
        device = create_device(ip.strip(), creds)
        print(f"\nReloading {ip.strip()}")

        try:
            with ConnectHandler(**device) as conn:
                output = conn.send_command("reload", expect_string=r'Proceed with reload?')
                print(output)

                output = conn.send_command('\n')  # Confirm reload
                print(output)
        except Exception as err:
            print(f"[ERROR: {ip.strip()}] {err}")
    
    # Print total execution time in seconds  
    print(f"\nTotal time: {round(time.perf_counter() - start, 2)} seconds.")
    
# Only runs if you execute this script directly
if __name__ == "__main__":
    run_boot_and_reload()