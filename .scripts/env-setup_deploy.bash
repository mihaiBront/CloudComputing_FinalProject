#!/bin/bash
echo off
# Name of the directory to check
VENV_DIR="../.venv" # Replace 'venv' with your specific virtual environment folder name if different.

if python -m venv --help &>/dev/null; then
  echo "python is already installed."
elif python3 -m venv --help &>/dev/null; then
  echo "python3 is installed but python does not point to python3..."
  ln -s $(which python3) /usr/bin/python
else
  echo "no python installed...aborted"
  # Detect package manager and install python3-venv
  if [ -f /etc/debian_version ]; then
      # Debian/Ubuntu-based systems
      apt update
      apt install -y python3-venv
  elif [ -f /etc/redhat-release ]; then
      # Red Hat-based systems
      yum install -y python3-venv
  elif [ -f /etc/arch-release ]; then
      # Arch-based systems
      pacman -S --noconfirm python-virtualenv
  elif [ -f /etc/SuSE-release ]; then
      # SUSE-based systems
      zypper install -y python3-virtualenv
  else
      echo "Unsupported Linux distribution. Please install python3-venv manually."
      exit 1
  fi

  # Confirm installation
  if python3 -m venv --help &>/dev/null; then
      echo "python3-venv has been successfully installed."
      apt install -y python-is-python3
  else
      echo "Failed to install python3-venv. Please check your package manager."
      exit 1
  fi
fi

if dpkg -l | grep -qw "python3-venv"; then
    echo "python3-venv is already installed."
else
    echo "python3-venv is not installed. Installing now..."
    apt update
    apt install -y python3-venv
    if [ $? -eq 0 ]; then
        echo "python3-venv was successfully installed."
    else
        echo "There was an error installing python3-venv."
        exit 1
    fi
fi

# Check if the virtual environment exists
if [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/pyvenv.cfg" ]; then
    echo "Virtual environment found in $VENV_DIR."
else
    echo "No virtual environment found in $VENV_DIR, creating environment"
    python -m venv .venv
    echo 'Virtual environment created'
fi

if [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/activate" ]; then
  echo "Activating the virtual environment..."
  . $VENV_DIR/bin/activate
else
  echo "Failed creating environment"
  exit -1
fi

# Install necessary dependencies
if [ -f "requirements.txt" ]; then
  echo "Installing dependencies from requirements.txt..."
  pip install -U pip
  pip install -r requirements.txt
else
  echo "requirements.txt not found. Skipping installation."
fi

# Download the needed model
FILE_URL="https://www.dropbox.com/scl/fi/zx3q65yaoigwpdwyovlip/reggressionGlucoseSimple.joblib?rlkey=lfig1q76rmtea2dr5tr2qwq53&st=6nmy2bpk&dl=1"
FILE_NAME="../reggressionGlucoseSimple.joblib"

if [ -f "$FILE_NAME" ]; then # Only if it does not already exist
    echo "File '$FILE_NAME' already exists. Skipping download."
else
    echo "File '$FILE_NAME' not found. Downloading..."
    curl -L "$FILE_URL" -o "$FILE_NAME"
    echo "Download complete."
fi