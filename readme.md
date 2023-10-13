## Project Information

This project is designed to retrieve and save measurement data from Socomec electricity meters in a database. The Socomec electricity meters store their daily measurement data in CSV format on an FTP server.

This Python project connects to this network through a VPN connection, downloads the measurement data, and saves the information in a database. The collected measurements are then sent via email.

## Libraries/Frameworks/Modules

This project utilizes the following libraries and modules:
- pandas
- py7zr

## Prerequisites

To use this project, you will need the following prerequisites:
- Python
- Virtual environment named 'env'
- Install required dependencies using `pip install -r requirements.txt`
- a configured VPN connection (PPTP in this case)

## Network settings (Linux)

- Create a VPN connection (PPTP)
  - Edit the PPTP configuration file:
    ```shell
    sudo nano /etc/ppp/peers/MY_VPN
    ```
    Add the following configuration:
    ```shell
    pty "pptp 123.45.67.89 --nolaunchpppd"
    name user_name
    password Secret_password
    remotename PPTP
    require-mppe-128
    file /etc/ppp/options.pptp
    ipparam MY_VPN
    ```

  - In Linux, add `/usr/bin/pon` and `/usr/bin/poff` to the sudoers file with 'visudo'.

  - Add a route to the VPN when starting it and remove it when closing it. Use the following scripts:
    - Create `/etc/ppp/ip-up.d/add_vpn_route`:
      ```shell
      #!/bin/bash
      /sbin/route add -net 172.16.0.0 netmask 255.255.240.0 dev ppp0
      ```

    - Create `/etc/ppp/ip-down.d/del_vpn_route`:
      ```shell
      #!/bin/bash
      /sbin/route del -net 172.16.0.0 netmask 255.255.240.0 dev ppp0
      ```

  - Make scripts executable: `sudo chmod +x /etc/ppp/ip-up/down.d/..._vpn_route`

  - Check the route with: `traceroute <ip-ftp-server>`

## Installation

To set up the project, follow these steps:
1. Create the 'socomec.ini' from the 'example.ini' file and enter the necessary information for 'vpn', 'ftp', 'mail', and 'smtp'.
2. In the 'folders' section, specify a 'base_directory'. This directory will serve as the location for your database, downloaded & backup folders, and log file.
3. Copy files from the '_init' directory. This step will create the 'download' and 'backup' folders and copy an empty database. Be careful not to overwrite any existing data.
4. Create a VPN connection with the same name entered in the 'vpn' section of the 'socomec.ini' file.
5. Make sure the `startscraper.sh` is executable (chmod +x)

## Using the Scraper

To use the scraper, follow these steps:
1. Run the 'startscraper.sh' script.
2. The script downloads CSV files, processes them, saves the information to the database, and sends a mail with the latest results.
3. If there are files on the FTP server, the script takes about 30 seconds. The script logs errors, warnings, and information to the log file.
4. Optional, but recommended: add the script to a task scheduler or crontab for automated execution: `crontab -e`.

# some notes to myself
# virtual environments
    # make virtual environment
    python -m venv <env_name>

    # activate virtual environment
        # Windows: cmd.exe
        venv\Scripts\activate.bat
        # Windows: PowerShell
        venv\Scripts\Activate.ps1
        # Linux
        source myvenv/bin/activate

    # deactivate virtual environment
    deactivate

# git
    # enter user.name & user.email
    git config --global user.name "Your Name"
    git config --global user.email "youremail@yourdomain.com"
    # .gitignore
    files & folders in here are not synced via git

# requirements.txt
    used imports in scripts. quickly install with:
    pip install -r requirements.txt
    # example
    nose
    pandas
    ###### Requirements with Version Specifiers ######
    docopt == 0.6.1             # Version Matching. Must be version 0.6.1
    keyring >= 4.1.1            # Minimum version 4.1.1
    coverage != 3.5             # Version Exclusion. Anything except version 3.5

# websites
    # Python Package Index
    https://pypi.org/
    # Structuring Your Project
    https://docs.python-guide.org/writing/structure/

# start uvicorn
