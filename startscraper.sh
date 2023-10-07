#!/bin/bash

# Check the platform
if [[ "$OSTYPE" == "msys" ]]; then
    # Windows: Activate virtual environment using PowerShell
    virtualenv_name="venv"  # Replace with your virtual environment name
    source "${virtualenv_name}/Scripts/activate"
else
    # Linux: Activate virtual environment using Bash
    virtualenv_name="env"  
    source "${virtualenv_name}/bin/activate"
fi

# Run your Python script
python scraper.py
