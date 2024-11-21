#!/bin/bash

# Name of the directory to check
VENV_DIR="./.venv" # Replace 'venv' with your specific virtual environment folder name if different.

# Check if the virtual environment exists
if [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/pyvenv.cfg" ]; then
    echo "Virtual environment found in $VENV_DIR."
else
    echo "No virtual environment found in $VENV_DIR, creating environment"
    python -m venv .venv
    echo 'Virtual environment created'
fi

# Install necessary dependencies
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

# Program end
echo "All requirements satisfied"