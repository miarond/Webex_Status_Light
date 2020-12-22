# Webex Status Light
 This is a project originally created by Matthew Fugel (https://github.com/matthewf01/Webex-Teams-Status-Box), which I have forked and improved for my needs. It utilizes a Raspberry Pi computing platform (any model from v3 forward should work - I am using a Pi Zero Wireless), an LED setup connected to the GPIO headers, and the Webex Teams API Python SDK. The Python script is run as a background service in Debian Linux and utilizing the SDK, it makes an API call to Webex every 60 seconds to check the current presence status of the user configured during setup.

 I have encountered regular connection rejects from the API, possibly due to rate-limiting, which I handle by backing off for 10 seconds and then re-running the API call.  The service and script will run indefinitely unless explicitly killed via a root privileged user, or if the service encounters a fatal error. Historical logging for the service is handled by the system Journal daemon (`journalctl`).

# Table of Contents
1. [Parts List](#parts-list)
2. [SD Card Setup](#sd-card-setup)
3. [Assembly](#assembly)
4. [Installation](#installation)
5. [Testing and Troubleshooting](#testing-and-troubleshooting)

## Parts List

<u>Parts to purchase:</u>
- Pi Traffic Light
  - https://www.amazon.com/Pi-Traffic-Light-Raspberry-pack/dp/B00P8VFA42/ref=sr_1_5?dchild=1&keywords=Raspberry%2BPi%2BLED&qid=1608300350&sr=8-5&th=1
  - ![Image from www.amazon.com](/images/Pi_Traffic_Light.jpg)
- Raspberry Pi Zero WH (Wireless with Headers pre-installed)
  - https://www.adafruit.com/product/3708
  - ![Image from www.adafruit.com](/images/Pi_Zero_WH.jpg)
- Raspberry Pi Zero Case (comes with camera ribbon cable, not needed)
  - https://www.adafruit.com/product/3446
  - ![Image from www.adafruit.com](/images/Pi_Zero_Case.jpg)
- 16 or 32 GB Micro SDHC card
  - https://www.amazon.com/Sandisk-Ultra-Micro-UHS-I-Adapter/dp/B073K14CVB/ref=sr_1_4?dchild=1&keywords=16gb+microsd&qid=1608314289&sr=8-4
  - https://www.amazon.com/Samsung-MicroSDHC-Adapter-MB-ME32GA-AM/dp/B06XWN9Q99/ref=sr_1_5?dchild=1&keywords=16gb+microsd&qid=1608314402&sr=8-5
  - ![Image from www.sandisk.com](/images/SDHC.jpg)

<u>Bring your own:</u>
- Micro USB charging cable (standard phone cable will work)
  - ![Image from www.bestbuy.com](/images/Micro_USB_Cable.jpg)
- 5v USB charging block (minimum 1 Amp capacity)
- Windows or Mac laptop for SSH and SFTP file transfer
- WPA2 wireless network with Pre-Shared Key, DHCP/DNS and Internet connectivity
- Cisco CCO account with Webex messaging user license
