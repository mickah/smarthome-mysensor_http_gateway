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
source env/bin/activate
python3 -m venv env
source env/bin/activate
# Dependency
pip3 install pyrequirement.txt
```

## Run server (not prod ready)
```
flask run
```

## Next steps
- Run as service instructions
- Store all sensors data into a distant mongodb database