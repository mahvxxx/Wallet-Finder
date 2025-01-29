#!/bin/bash

# Specify the URL of the GitHub repository (or any other URL where you have uploaded the files)
echo "Downloading program files from GitHub repository..."
git clone https://github.com/yourusername/yourrepository.git

# Navigate into the project directory
cd yourrepository

# Update package list and install pip (if not installed)
echo "Updating package list and installing pip..."
sudo apt-get update
sudo apt-get install python3-pip -y

# Install the required Python libraries from requirements.txt
echo "Installing required Python libraries from requirements.txt..."
pip3 install -r requirements.txt

# Run the Python script
echo "Running the Python script..."
python3 wallet-founder.py
