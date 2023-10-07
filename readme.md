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
