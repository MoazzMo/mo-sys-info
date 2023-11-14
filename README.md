# MO-SYS-INFO

## Overview

`MO-SYS-INFO` is a Python script that displays system information and allows clearing logs for specific paths.

## Features

- **Clear Logs:**
  - Provides buttons to clear VNA and MiBroker logs separately.
  - Displays a message on success or an error message on failure.

- **Disk Information:**
  - Shows information about disk partitions, including total, used, and free space.

- **RAM Information:**
  - Constantly updates and displays RAM usage information.

## Prerequisites

- Python 3
- Required Python packages can be installed using `pip install psutil`

## Usage

1. Run the script using Python:
   ```bash
   python mo_sys_info.py

## Notes

The script uses the psutil library to gather system information.


## Contributing

Contributions are welcome! If you find a bug or have suggestions, please create an issue or a pull request.