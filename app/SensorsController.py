import mysensors.mysensors as mysensors
import json
import os

def event(message):
    """Callback for mysensors updates."""
    print('sensor_update ' + str(message.node_id))


class SensorsController:
    def __init__(self):
        #
        serial_port = os.environ['MYSENSOR_SERIAL']
        if serial_port == None:
            print("MYSENSOR_SERIAL env variable missing!")
        else:
            print("Using serial port: "+str(os.environ['MYSENSOR_SERIAL']))
        self.gateway = mysensors.SerialGateway(os.environ['MYSENSOR_SERIAL'], event)
        self.gateway.start_persistence()
        self.gateway.start()
        #self.sensors_tests = [{"sensor_id":6,"type":16,"children":[{"id":2,"type":"S_HUM","values":[{"V_HUM":60}]}]}]


    def getSensors(self):
        return self.gateway.sensors.values()