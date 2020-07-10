# My Sensors Http Gateway

## Description

This project aims to make a [mysensors](https://www.mysensors.org/about/arduino) gateway accessible via an http API server. It is based on pymysensors.

## Current endpoints

- /sensors: list all sensors that has been connected with their last value
- /sensors/id/<node_id>/<child_id>: get the recorded values for a specific sensor

## Configuration

The configuration is done through environment variables in the .env file:

- MYSENSOR_SERIAL: serial port on which the mysensor device is connected

## Setup

```
# update .env file with your passwords, serial id...
docker-compose up

# The http server should running on http://127.0.0.1:5000
```

## Developpement instructions

### Use docker for developpement

```
./scripts/start_dev.sh
python3 -m venv env
source env/bin/activate
# Dependency
pip3 install -r requirements.txt
```

### Without docker developpement

```bash
apt install python3-venv
python3 -m venv env
source env/bin/activate
# Dependency
pip3 install -r requirements.txt
```

### Run server locally (not prod ready)

```
LANG=C.UTF-8 MYSENSOR_SERIAL=/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_00000000-if00-port0 flask run
```

## Notes

- use /dev/serial/by-id
