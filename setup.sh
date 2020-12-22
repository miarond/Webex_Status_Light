#!/bin/sh
# Webex App Status Light - Forked and improved by Aron Donaldson, original concept by:
# 2020-04-03 Matthew Fugel
# https://github.com/matthewf01/Webex-Teams-Status-Box/

cd /home/pi

# Retrieve user-specific values that will be written to the webexapp.service file for use with systemd
echo "Beginning setup. See https://github.com/miarond/Webex_Status_Light for full instructions."
read -p "Enter your Webex BOT token: " accessToken
read -p "Enter the Webex user's personId: " person

# Write the values out to file
echo "---Webex Credentials---" >> mycredentials.txt
echo "---saving here for your reference. This file is not used by the script. Creds are in /etc/systemd/system/webexapp.service.--" >> mycredentials.txt
echo "Environment=WEBEX_TEAMS_ACCESS_TOKEN="$accessToken >> mycredentials.txt
echo "Environment=PERSON="$person >> mycredentials.txt

# Download script files
wget -O webexapp.py https://raw.githubusercontent.com/miarond/Webex_Status_Light/main/webexapp.py
wget -O webexapp.service https://raw.githubusercontent.com/miarond/Webex_Status_Light/main/webexapp.service
wget -O ledclean.py https://raw.githubusercontent.com/miarond/Webex_Status_Light/main/ledclean.py
wget -O rgbtest.py https://raw.githubusercontent.com/miarond/Webex_Status_Light/main/rgbtest.py

# Update service file with creds using 'sed' to find & replace 'foo' and 'bar' placeholders with user's credentials.
sed -i "s/foo/$accessToken/" webexapp.service
sed -i "s/bar/$person/" webexapp.service

# Copy the service's unit file out to systemd, then register app as a service
sudo mv webexapp.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable webexapp.service

# Install external dependencies
sudo pip install webexteamssdk
sudo pip install RPi.GPIO

# Finally, reboot
echo "Install complete. Rebooting..."
sleep 5
sudo reboot now
