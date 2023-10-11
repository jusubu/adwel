# Project Information

This Python project involves Socomec electricity readers that send their latest readings to a FTP server located in a separate network. The project connects to the separate network via VPN, downloads reading information from the FTP server, saves the data to an SQLite database, and sends a CSV file attached to an email with the latest results.

## Libraries/Frameworks/Modules

This project utilizes the following libraries and modules:
- pandas
- py7zr

## Prerequisites

To use this project, you will need the following prerequisites:
- Python
- Virtual environment named 'env'
- Install required dependencies using `pip install -r requirements.txt`
- a configured vpn connection (pptp in this case)

## Network settings Linux
- create VPN connection
- in linux add /usr/bin/pon and /usr/bin/poff to sudoers with 'visudo'
- add a route to the vpn when starting it and remove when closing it:
- sudo nano /etc/ppp/ip-up.d/add_vpn_route
'
#!/bin/bash
/sbin/route add -net 172.16.0.0 netmask 255.255.240.0 dev ppp0
'
- sudo nano /etc/ppp/ip-down.d/del_vpn_route
'
#!/bin/bash
/sbin/route del -net 172.16.0.0 netmask 255.255.240.0 dev ppp0
'
- make script executable: 'sudo chmod +x /etc/ppp/ip-up/down.d/..._vpn_route'
- check the route with traceroute <ip-ftp-server>

## Installation

To set up the project, follow these steps:
1. Edit the 'socomec.ini' file and enter the necessary information for 'vpn', 'ftp', 'mail', and 'smtp'.
2. In the 'folders' section, specify a 'base_directory'. This directory will serve as the location for your database, downloaded files, and log file.
3. Copy files from the '_init' directory. This step will create the 'download' and 'backup' folders and copy an empty database. Be careful not to overwrite any existing data.
4. Create a VPN connection with the same name entered in the 'vpn' section of the 'socomec.ini' file.

## Using the Scraper

To use the scraper, follow these steps:
1. Run the 'startscraper.sh' script.
2. The script downloads csv-files, processes them, saves the information to the database and sends a mail with the latest results.
3. If there are files on the ftp-server, the script finishes in about 30 seconds. The scripts logs errors, warnings and information to the log-file.
4. Optional, but recommended: add the script to a task scheduler or crontab for automated execution.


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
