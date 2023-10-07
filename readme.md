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

## Using the Scraper

To use the scraper, follow these steps:
1. Install all dependencies.
2. Create a 'socomec.ini' configuration file (an 'example.ini' is included).
3. Run the 'startscraper.sh' script.
4. Optionally, you can add the script to a task scheduler or crontab for automated execution.

## Installation

To set up the project, follow these steps:
1. Edit the 'socomec.ini' file and enter the necessary information for 'vpn', 'ftp', 'mail', and 'smtp'.
2. In the 'folders' section, specify a 'base_directory'. This directory will serve as the location for your database, downloaded files, and log file.
3. Copy files from the '_init' directory. This step will create the 'download' and 'backup' folders and copy an empty database. Be careful not to overwrite any existing data.
4. Create a VPN connection with the same name entered in the 'vpn' section of the 'socomec.ini' file.


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
