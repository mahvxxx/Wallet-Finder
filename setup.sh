#!/bin/bash

# Update package list
echo "Updating package list..."
sudo apt-get update

# Check if Python3 is installed, if not, install it
echo "Checking if Python3 is installed..."
if ! command -v python3 &> /dev/null
then
    echo "Python3 not found. Installing Python3..."
    sudo apt-get install python3 -y
else
    echo "Python3 is already installed."
fi

# Check if pip3 is installed, if not, install it
echo "Checking if pip3 is installed..."
if ! command -v pip3 &> /dev/null
then
    echo "pip3 not found. Installing pip3..."
    sudo apt-get install python3-pip -y
else
    echo "pip3 is already installed."
fi

# Specify the URL of the GitHub repository (or any other URL where you have uploaded the files)
echo "Downloading program files from GitHub repository..."
git clone https://github.com/yourusername/yourrepository.git

# Navigate into the project directory
cd yourrepository

# Install the required Python libraries from requirements.txt
echo "Installing required Python libraries from requirements.txt..."
pip3 install -r requirements.txt

# Run the Python script
echo "Running the Python script..."
python3 your_script_name.py
