# My Sensors Http Gateway

## Description
This project aims to make a [mysensors](https://www.mysensors.org/about/arduino) gateway accessible via an http API server. It is based on pymysensors.

## Current endpoints
- /sensors: list all sensors currently connected

## Configuration
The configuration is done through environment variables:
- MYSENSOR_SERIAL: serial port on which the mysensor device is connected

## Install with virtual env
```bash
apt install python3-venv
python3 -m venv env
source env/bin/activate
# Dependency
pip3 install -r requirement.txt
```

## Run server (not prod ready)
```
LANG=C.UTF-8 MYSENSOR_SERIAL=/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_00000000-if00-port0 flask run
```

## Use docker for developpement
```
./scripts/start_dev.sh
python3 -m venv env
source env/bin/activate
# Dependency
pip3 install -r requirement.txt
```

## Next steps
- Run as service instructions
- Store all sensors data into a distant mongodb database


# Annexes 
## Setup udev rule for non root serial permission read/write
'/etc/udev/rules.d/99-serial.rules'
KERNEL=="ttyUSB[0-9]*",MODE="0666"

## Mount dev, and previlegied
`-v /dev:/dev --privileged`

## use /dev/serial/by-id

