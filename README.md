[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/miarond/Webex_Status_Light)

# Webex Status Light

 This is a project originally created by Matthew Fugel (https://github.com/matthewf01/Webex-Teams-Status-Box), which I have copied and improved for my needs. It utilizes a Raspberry Pi computing platform (any model from v3 forward should work - I am using a Pi Zero Wireless), an LED setup connected to the GPIO headers, and the Webex Teams API Python SDK. The Python script is run as a background service in Debian Linux and, utilizing the SDK, it makes an API call to Webex every 60 seconds to check the current presence status of the user configured during setup.

 I have encountered regular connection rejects from the API, possibly due to rate-limiting, which I handle by backing off for 10 seconds and then re-running the API call.  The service and script will run indefinitely unless explicitly killed via a root privileged user, or if the service encounters a fatal error. Historical logging for the service is handled by the system Journal daemon (`journalctl`).

### Improvements on Original Code

- Error handling and recovery via the Webex Teams API
- Functions for turning the LED on and off
- Previous state tracking for the LED status
- LED test on initial startup
- Changing the single multi-color LED to a 3-LED pre-built circuit board that is commercially available (eliminates the need to build your own LED with resistors)
- LED state cleanup on service stop or crash
- Improved instructions for full build process, improved code comments and cleanup

# Table of Contents

1. [Parts List](#parts-list)
2. [SD Card Setup](#sd-card-setup)
3. [Assembly](#assembly)
4. [Collect Webex Credentials](#collect-webex-credentials)
5. [Installation](#installation)
6. [Testing and Troubleshooting](#testing-and-troubleshooting)
7. [Directory Structure](#directory-structure)

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
- Micro USB **data transfer** cable. Normally a standard smartphone cable will work as long as it is not a *charging only* cable.
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
4. Once writing is complete you will need to remove and reinsert the SD card. Next, open the SD card in Finder or Windows Explorer. We will be creating two text files and editing two existing files in the root directory of the SD card, in order to pre-set some basic configuration parameters. The guide on Adafruit's website below mentions a folder named **boot** on the SD card - in testing on Windows I have found that the readable partition of the SD card is labeled **boot**, not a subdirectory on the SD card.
    - This setup process is known as "**headless**" mode and is really well documented on Adafruit's website [here](https://learn.adafruit.com/raspberry-pi-zero-creation).
    - The text file setup process is explained on [this](https://learn.adafruit.com/raspberry-pi-zero-creation/text-file-editing) page of the guide.
5. Create a *blank* text file called `ssh` - there should be **NO** file extension in the filename.  This file tells Debian to enable SSH access permanently on first bootup.
6. Create a text file named `wpa_supplicant.conf` and add the text below. MAKE SURE to replace `YOURSSID` and `YOURPASSWORD` with your actual wireless SSID and PSK (leave the "" surrounding your SSID and PSK). This pre-loads Debian with your wireless network info so it will automatically connect.
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

  # Enable Ethernet over USB
  dtoverlay=dwc2
  ```
8. Edit the `cmdline.txt` file that already exists and add the text `modules-load=dwc2,g_ether` after `rootwait`. This file should contain a single line of text with no line breaks and the text you add should be separated from `rootwait` by a single space. The end result should look like this:
```
console=serial0,115200 console=tty1 root=PARTUUID=eabcf7ff-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait modules-load=dwc2,g_ether
```
  - More detailed instructions on how to utilize Ethernet over USB will be covered in the Testing and Troubleshooting section below.
9. Last but not least, safely eject the SD card from your computer.

## Assembly

In this step we will install all the necessary components, insert the Pi Zero in the plastic case, install the Pi Traffic Light on the correct GPIO pins and finally, power up your Pi Zero.

1. Insert the Micro SD card into the correct slot on the Pi Zero. The connection pins on the board face upward so the SD card's connectors should face downward, toward the circuit board.
2. Insert the Pi Zero board into the plastic case's bottom half (red plastic section). The best method to prevent damage is to insert the long edge containing the HDMI and USB ports first to make sure they line up with the holes properly and extend slightly into the openings. There are 4 plastic studs on the bottom of the case which should line up with and sit inside the 4 standoff holes in the Pi's circuit board.  Finally, firmly press down the opposite long edge until it snaps into place below the opposite side's retainer clip.
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

In this section we'll begin the installation and setup process. We'll start by verifying that Python 3 is installed (the Debian image comes with Python 2 and 3 pre-installed but this script is not fully backward compatible with Python 2) and the necessary Python modules. Then we will install the Python script and configure the background service. Additionally, in the Testing and Troubleshooting section I've given an explanation of the `sudo` command prefix that you'll find in this section.

1. Establish an SSH session to your Pi Zero.
    - Username: `pi`
    - Password: `raspberry`
    - To change the default password, log in via SSH then run the command `passwd`.  Follow the prompts to change the password.
2. Verify Internet connectivity and then check if Python 3 and Pip 3 (the Python package manager)  are installed by running the following commands:
    - `sudo apt-get update`
    - `python3 --version`
    - `pip3 --version`
3. In my testing Python 3.7.3 was installed by default but Pip was not.  If either need to be installed, run the following commands:
    - `sudo apt-get install python3.7`
    - `sudo apt-get install python3-pip`
    - Re-run the version check command(s) in step 2 to verify the installation worked.
4. Ensure that you are in your home directory, then download the setup script from this Github repository:
    - `cd`
      - Issuing this command with no arguments changes directory back to the current user's Home directory.
    - `wget -O setup.sh https://raw.githubusercontent.com/miarond/Webex_Status_Light/main/setup.sh`
5. Verify the file permissions of the newly created setup.sh file:
    - Run the command `ls -al | grep setup` to view the file and its attributes.
      - My output looked like this:
      ```
      pi@raspberrypi:~ $ ls -al | grep setup
      -rw-r--r-- 1 pi   pi   1848 Dec 23 12:41 setup.sh
      ```
      - File attributes are shown in the format `drwxrwxrwx` where the first letter denotes either a file (`-`) or a directory (`d`). The next groupings of 3 letters denote read (`r`), write (`w`) and execute (`x`) permissions. As you can see, my file is missing the execute permission.
    - Add execute permissions to the file by running the command `chmod +x setup.sh`.  Because the `pi` user account is the owner of the file, we can run this command without adding the `sudo` prefix.
5. Start the setup script to begin installation:
    - `sudo ./setup.sh`
    - The setup Bash script will prompt you for the Webex Bot token and the Person ID collected in the previous section.  It will then download additional files from the Github repo and configure the background service.
6. When finished, the Bash script will force a reboot of the Pi Zero. If the configuration was successful and the API access tokens are valid, the background service should start automatically on bootup and the LEDs should activate.

## Testing and Troubleshooting

Wait, you mean it *didn't* work right the first time???  It's a well known axiom that code rarely works right on the first try...and if it does, you should be suspicious! There are several places where this setup process could go wrong and its always best to watch the SSH console output carefully as the installation progresses. Detailed error messages or warnings will often be displayed on the console.

Some common spots for trouble could be:
- Installation failures due to insufficient privileges.
    - Most system modifying commands will require the use of the `sudo` prefix.  The `sudo` command stands for "Superuser Do" and it is the equivalent of choosing "Run as Administrator" on Windows operating systems.
    - As mentioned in the previous section, files that need to be executed (like Bash scripts) will require execute permissions which may not be set by default.  To view the permissions of any file or directory you can change directory to where that file or folder exists, then run the `ls -al` command. Running the `chmod +x <filename>` command will add execute permissions - using `+r` or `+w` will add read or write permissions.
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
        - Press `Ctrl + O` to save the file, then `Ctrl + X` to exit.
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

If your Pi doesn't come online and connect to your wireless network automatically, you can try connecting a keyboard, mouse and monitor if you have the proper adapters for both Micro USB and Mini HDMI. However, if you don't have those adapters you CAN use the USB data cable to establish an emergency terminal/console session. The process is partially documented on this website [The Polyglot Developer](https://www.thepolyglotdeveloper.com/2016/06/connect-raspberry-pi-zero-usb-cable-ssh/). Windows users will need to install Apple's [Bonjour Print Services](https://support.apple.com/kb/DL999?locale=en_US) application to communicate with the Pi over USB (this is the only method I have personally tested). Mac users should not need this additional step (as documented [here](https://learn.adafruit.com/bonjour-zeroconf-networking-for-windows-and-linux)).

Once setup is complete on your computer, connect the Micro USB cable to the **USB** port on the Pi (NOT the PWR IN port) and to a USB port on your computer. The Pi should power on and establish a network connection to your computer via the USB cable. You can then simply SSH to `raspberrypi.local` from your computer and you should be able to connect to the Pi just like you would over a network connection.

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
