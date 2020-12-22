# Webex Status Light

 This is a project originally created by Matthew Fugel (https://github.com/matthewf01/Webex-Teams-Status-Box), which I have forked and improved for my needs. It utilizes a Raspberry Pi computing platform (any model from v3 forward should work - I am using a Pi Zero Wireless), an LED setup connected to the GPIO headers, and the Webex Teams API Python SDK. The Python script is run as a background service in Debian Linux and, utilizing the SDK, it makes an API call to Webex every 60 seconds to check the current presence status of the user configured during setup.

 I have encountered regular connection rejects from the API, possibly due to rate-limiting, which I handle by backing off for 10 seconds and then re-running the API call.  The service and script will run indefinitely unless explicitly killed via a root privileged user, or if the service encounters a fatal error. Historical logging for the service is handled by the system Journal daemon (`journalctl`).

# Table of Contents

1. [Parts List](#parts-list)
2. [SD Card Setup](#sd-card-setup)
3. [Assembly](#assembly)
4. [Installation](#installation)
5. [Testing and Troubleshooting](#testing-and-troubleshooting)

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
5.
