# rpz_status
Clock and other status display for an E-ink display for the Raspberry Pi Zero

## Setup
1. https://github.com/PiSupply/PaPiRus
1. Install python packages and also run them with `sudo` (i.e. `sudo pip install geocoder`)
  1. `pip install geocoder`
  1. `pip install Pillow`
  1. `pip install requests`
1.  add `sudo -H -u pi nohup python /home/pi/projects/rpz_status/display.py > /home/pi/projects/rpz_status/output.log &` to `/etc/rc.local` so it runs on startup
