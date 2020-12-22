# Webex Status Light

 This is a project originally created by Matthew Fugel (https://github.com/matthewf01/Webex-Teams-Status-Box), which I have copied and improved for my needs. It utilizes a Raspberry Pi computing platform (any model from v3 forward should work - I am using a Pi Zero Wireless), an LED setup connected to the GPIO headers, and the Webex Teams API Python SDK. The Python script is run as a background service in Debian Linux and, utilizing the SDK, it makes an API call to Webex every 60 seconds to check the current presence status of the user configured during setup.

 I have encountered regular connection rejects from the API, possibly due to rate-limiting, which I handle by backing off for 10 seconds and then re-running the API call.  The service and script will run indefinitely unless explicitly killed via a root privileged user, or if the service encounters a fatal error. Historical logging for the service is handled by the system Journal daemon (`journalctl`).

# Table of Contents

1. [Parts List](#parts-list)
2. [SD Card Setup](#sd-card-setup)
3. [Assembly](#assembly)
4. [Collect Webex Credentials](#collect-webex-credentials)
5. [Installation](#installation)
6. [Testing and Troubleshooting](#testing-and-troubleshooting)

## Parts List

<b><u>Parts to purchase:</u></b>
- Pi Traffic Light (available from Amazon)
  - https://lowvoltagelabs.com/products/pi-traffic/
  - https://www.amazon.com/Pi-Traffic-Light-Raspberry-pack/dp/B00P8VFA42/
  - ![Image from www.amazon.com](/images/Pi_Traffic_Light.jpg)
- Raspberry Pi Zero WH (Wireless with Headers pre-installed)
  - https://www.adafruit.com/product/3708
  - ![Image from www.adafruit.com](/images/Pi_Zero_WH.jpg)
- Raspberry Pi Zero Case (comes with camera ribbon cable, not needed)
  - https://www.adafruit.com/product/3446
  - ![Image from www.adafruit.com](/images/Pi_Zero_Case.jpg)
- 16 or 32 GB Micro SDHC card
  - https://www.amazon.com/Sandisk-Ultra-Micro-UHS-I-Adapter/dp/B073K14CVB/
  - https://www.amazon.com/Samsung-MicroSDHC-Adapter-MB-ME32GA-AM/dp/B06XWN9Q99/
  - ![Image from www.sandisk.com](/images/SDHC.jpg)

<b><u>Bring your own:</u></b>
- Micro USB charging cable (standard phone cable will work)
  - ![Image from www.bestbuy.com](/images/Micro_USB_Cable.jpg)
- 5v USB charging block (minimum 1 Amp capacity)
- Windows or Mac laptop for SSH and SFTP file transfer
- SD Card reader (if you are creating the bootable SD card on your own)
- WPA2 wireless network with Pre-Shared Key, DHCP/DNS and Internet connectivity
- Cisco CCO account with Webex messaging user license

## SD Card Setup

The Raspberry Pi computing platform most commonly runs a distribution of the Linux operating system, written for ARM processor architectures. In this case I am using the standard Debian Linux distribution recommended by the creators of the RPi. This comes in two versions: Desktop (has a GUI interface) and Lite (CLI only).  I am using the Lite version to save on system resources and because I intend to run the Pi in "**headless**" mode, without a keyboard, mouse or video display.  Let's get started!

1. Insert your Micro SD Card in a card reader and ensure that it is readable.
2. Visit the "Getting Started" guide and follow the instructions [here](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/2) to setup your SD card.
    - This requires downloading the Raspberry Pi Imager application, then choosing an installation image to download (you can also download the image manually and pick it from your local machine via the Imager app). **This guide assumes you are choosing the "Lite" version.**
3. Using the Imager application, write the image file to the SD card.
4. Once writing is complete, open the SD card in Finder or Windows Explorer. We will be creating two text files and editing one existing file in the root directory of the SD card, in order to pre-set some basic configuration parameters.
    - This setup process is known as "**headless**" mode and is really well documented on Adafruit's website [here](https://learn.adafruit.com/raspberry-pi-zero-creation).
    - The text file setup process is explained on [this](https://learn.adafruit.com/raspberry-pi-zero-creation/text-file-editing) page of the guide.
5. Create a *blank* text file called `ssh` - there should be **NO** file extension in the filename.  This file tells Debian to enable SSH access permanently on first bootup.
6. Create a text file named `wpa_supplicant.conf` and add the text below. MAKE SURE to replace `"YOURSSID"` and `"YOURPASSWORD"` with your actual wireless SSID and PSK. This pre-loads Debian with your wireless network info so it will automatically connect.
  ```
  ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
  update_config=1
  country=US

  network={
    ssid="YOURSSID"
    psk="YOURPASSWORD"
    scan_ssid=1
  }
  ```
7. Edit the `config.txt` file that already exists and add the following lines at the *bottom* of the file.  This setting allows you to use the USB cable for direct console access for emergency troubleshooting.
  ```
  # Enable UART
  enable_uart=1
  ```
8. Last but not least, safely eject the SD card from your computer.

## Assembly

In this step we will install all the necessary components, insert the Pi Zero in the plastic case, install the Pi Traffic Light on the correct GPIO pins and finally, power up your Pi Zero.

1. Insert the Micro SD card into the correct slot on the Pi Zero. The connection pins on the board face upward so the SD card's connectors should face downward, toward the circuit board.
2. Insert the Pi Zero board into the plastic case's bottom half (red plastic section). The best method to prevent damage is to insert the long edge containing the HDMI and USB ports first to make sure they line up with the holes properly and extend slightly into the openings. There is a small retainer "bump" on each long edge of the case. Finally, firmly press down the opposite long edge until it snaps into place below the opposite retainer "bump".
3. Select the white case cover with the long opening that exposes all of the GPIO header pins, then install it on the case.
4. Install the Pi Traffic Light circuit board onto the correct GPIO header pins. The LEDs on the circuit board should be facing outward, away from the edge of the Pi Zero circuit board.
    - The pins are GPIO 10, 9, 11, and Ground - physical pin numbers 19, 21, 23, and 25 - as shown in the diagram below.
    - ![Pi Zero GPIO Pinout Diagram](/images/Pi0_GPIO_Pinout.png)
    - ![Light Placement](/images/Light_Placement.png)
5. Connect the Micro USB cable and charging block to the `PWR IN` connector on the Pi Zero (the connector closest to the corner of the circuit board) and power on the system.
6. Start a continuous ping on your computer to **raspberrypi.local** and cancel it when the device begins responding. This hostname should always resolve to the Pi's local IP address on your network but if it does not, check your switch/router/DHCP server to determine what IP address the Pi obtained.

## Collect Webex Credentials

The Webex API will require two sets of credentials to utilize in this script.  The first is a Webex Bot Token that you will generate when you create a new Webex Bot.  The Bot is the actual application that will be checking the status of the Webex user.  The second piece of information is the Webex user's Person ID - a unique identifying string assigned to each user.  The script passes this Person ID to the Webex Bot to tell it which user to check the status of.

1. Go to https://developer.webex.com/my-apps/new/bot and log in with your Cisco CCO account.
2. Fill out all the necessary fields, then collect and document the Bot Token that is generated.
3. Go to https://developer.webex.com/docs/api/v1/people/get-my-own-details and log in with your CCO account (if necessary).
4. You should see a "Try It" button at the top-right of the webpage and a hidden "Bearer" token under the Header section.  Click the **Run** button near the bottom.
    - ![Get My Details Page](/images/Get_My_Details.png)
5. Below the **Run** button you should see output in the "Response" section. Copy and document the value from the `id` key at the top of the output (copy only the characters, not the double quotes "").
    - ![Get ID](/images/Get_ID.png)
    - BONUS: You just made your first API call :grin:

## Installation

In this section we'll begin the installation and setup process. We'll start by installing Python 3 (the Debian image comes with Python 2 pre-installed but this script is not fully backward compatible) and the necessary Python modules. Then we will install the Python script and configure the background service.

1. Establish an SSH session to your Pi Zero.
    - Username: `pi`
    - Password: `raspberry`
2. Verify Internet connectivity and then begin installing Python 3 and Pip 3 (the Python package manager) by running the following commands:
    - `sudo apt-get update`
    - `sudo apt-get install python3.6 python3-pip`
3. Check that Python 3 and Pip 3 are installed properly:
    - `python3 --version`
    - `pip3 --version`
4. Install the RPi.GPIO and Webex Teams SDK Python packages *system-wide*:
    - `sudo pip3 install RPi.GPIO`
    - `sudo pip3 install webexteamssdk`
5. Check that the Python packages were properly installed:
    - `sudo pip3 list`
6. Ensure that you are in your home directory, then download the setup script from this Github repository:
    - `cd`
      - Issuing this command with no arguments changes directory back to the current user's Home directory.
    - `wget -O setup.sh https://raw.githubusercontent.com/miarond/Webex_Status_Light/main/setup.sh`
7. Start the setup script to begin installation:
    - `sudo ./setup.sh`
    - The setup Bash script will prompt you for the Webex Bot token and the Person ID collected in the previous section.  It will then download additional files from the Github repo and configure the background service.
8. When finished, the Bash script will force a reboot of the Pi Zero. If the configuration was successful and the API access tokens are valid, the background service should start automatically on bootup and the LEDs should activate.

## Testing and Troubleshooting

Wait, you mean it *didn't* work right the first time???  It's a well known axiom that code rarely works right on the first try...and if it does, you should be suspicious! There are several places where this setup process could go wrong and its always best to watch the SSH console output carefully as the installation progresses. Detailed error messages or warnings will often be displayed on the console.

Some common spots for trouble could be:
- Installation failures due to insufficient privileges.
    - Most system modifying commands will require the use of the `sudo` prefix.  The `sudo` command stands for "Superuser Do" and it is the equivalent of choosing "Run as Administrator" on Windows operating systems.
- Installation failures due to missing dependencies.
    - Be sure to leverage the Aptitude (`apt-get`) package manager for installing programs.
    - Be sure to use the Pip package manager for installing Python modules.
    - When installing the Python modules listed above, make sure to run the command using `sudo` because this will install the package at the system level, making it available to all users and Python instances.
- Run the script using Python3 - a few of the code conventions used in the script are not backward compatible with Python2. If you aren't sure whether you're using Python3, make sure you're running the script with the command `python3 <script_name>`.
- Webex credentials aren't working, causing the API calls to fail.
    - If you copied the Bot token or your ID token incorrectly, you can repeat the steps in the earlier section to obtain them again. **NOTE**: The Bot token is only displayed once - if you have to obtain the token again, a brand new one will be generated.
    - If your tokens need to be updated post-installation, you can edit the service configuration file directly to change them.  Follow this procedure:
        - `sudo nano /etc/systemd/system/webexapp.service`
        - Edit the proper lines for the token(s)
        - Press `Ctrl + O` to save the file, then `Ctrl + Z` to exit.
        - Refresh the System Daemon by running the command `sudo systemctl daemon-reload`
        - Restart the service with the command `sudo systemctl start webexapp.service`
- Not sure why the service is crashing?
    - Run the command `sudo systemctl status webexapp.service` to view the last few lines of log output. These normally give some indication why the service crashed.
    - You can also run the command `sudo journalctl -f -u webexapp.service` to follow the "tail" output of the Journal log for the service.
- Need to view the output of the script to troubleshoot?
    - The `webexapp.py` Python script is the heart of this service and it is stored in the `/home/pi` directory. In order to run it directly you will need to edit the file and manually enter the Bot token and Person ID in the code, in place of the environmental variables that are registered by the `webexapp.service` config file.
        - Once edited, you can run the file with the command `python3 webexapp.py`.  To stop the script, press `Ctrl + C`.
        - Once stopped the LED lights will likely remain on. To turn them off after stopping the script, run the command `python3 ledclean.py`.
- If all else fails, Google the error message :grin:

## Directory Structure

The following is a directory tree structure that illustrates the files installed and where they are placed.

```
/
└─── home
|    └─── pi
|         └─── setup.sh
|         └─── webexapp.py
|         └─── ledclean.py
|         └─── rgbtest.py
└─── etc
     └─── systemd
          └─── system
               └─── webexapp.service
```

Environmental Variables
```
WEBEX_TEAMS_ACCESS_TOKEN
PERSON
```
