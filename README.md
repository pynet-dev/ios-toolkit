# Cisco IOS Automation

This repository contains a suite of Python scripts designed to automate IOS updates, post cleanup, verification, and reloading of Cisco IOS devices using SSH and SCP via the Netmiko library.

## Features

- Uploads IOS images to switches using SCP with a live progress bar
- Verifies installed IOS version
- Cleans old IOS from flash
- Updates boot path and reloads devices
- Modular structure with reusable utilities
- Threaded execution for faster uploads

## Scripts

| Script                                   | Description                                        |
|------------------------------------------|----------------------------------------------------|
| [`ios_scp.py`](ios-toolkit/ios_scp.py)               | Uploads IOS image to multiple devices via SCP      |
| [`verification.py`](ios-toolkit/verification.py)     | Checks current IOS version on all devices          |
| [`cleanup.py`](ios-toolkit/cleanup.py)               | Deletes old IOS images from device flash           |
| [`boot_reload.py`](ios-toolkit/boot_reload.py)       | Sets new boot path and reloads devices             |
| [`ios_toolkit.py`](ios-toolkit/ios_toolkit.py)       | Main driver script to launch update actions        |
| [`utils.py`](ios-toolkit/utils.py)                   | Shared functions for credential and device setup   |

## Usage

Each script is standalone but can also be triggered from `ios_toolkit.py` for guided execution.

For example, run SCP upload:
`python ios_scp.py`

To verify installed IOS versions:
`python verification.py`

## Notes

- IP address lists are stored as .txt files under the device/ directory (ignored by .gitignore).
- User credentials are collected at runtime for security.
- Transfers are multi-threaded for improved performance and include verification after upload.

## Disclaimer

This project is intended for educational and internal lab use only.  
It is not recommended for use in production environments without thorough testing and modification to suit your specific requirements.

The author is not responsible for any damage, outages, or unintended behavior resulting from the use of this software.
Use at your own risk.

## Requirements

- Python 3.9 or newer (recommended: 3.11+)
- [Netmiko](https://github.com/ktbyers/netmiko)
- [tqdm](https://pypi.org/project/tqdm/) (for progress bars)

##  Getting Started

1. **Clone the Repository**

   ```bash
   git clone https://github.com/pynet-dev/pynet-ios-toolkit.git
   cd pynet-ios-toolkit
