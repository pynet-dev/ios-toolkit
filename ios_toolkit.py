# ios_toolkit.py
from cleanup import run_cleanup
from verification import run_verification
from ios_scp import run_ios_scp
from boot_reload import run_boot_and_reload

# Main driver script providing a menu for running IOS automation tasks
# - Upload IOS via SCP
# - Set boot path and reload devices
# - Verify currently running IOS version
# - Clean up old IOS files from device flash
def main():

    print("""
    Cisco IOS Automation Toolkit
    ----------------------------
    1. Upload IOS via SCP
    2. Set boot path and reload devices
    3. Verify firmware version
    4. Remove IOS files
    """)

    choice = input("Choose an option (1-4): ").strip()

    if choice == '1':
        run_ios_scp()
    elif choice == '2':
        run_boot_and_reload()
    elif choice == '3':
        run_verification()
    elif choice == '4':
        run_cleanup()
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
