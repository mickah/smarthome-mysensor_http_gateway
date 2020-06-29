import mysensors.mysensors as mysensors
import json
import os
from datetime import datetime, timezone


class SensorsController:
    """ Sensors Controller class. It handles all interactions with mysensors """

    def __init__(self):
        serial_port = os.environ["MYSENSOR_SERIAL"]
        if serial_port == None:
            print("MYSENSOR_SERIAL env variable missing!")
        else:
            print("Using serial port: " + str(os.environ["MYSENSOR_SERIAL"]))

        self.gateway = None
        self.gateway = mysensors.SerialGateway(
            os.environ["MYSENSOR_SERIAL"],
            baud=38400,
            event_callback=self.event,
            persistence=True,
            persistence_file="./mysensors.pickle",
            protocol_version="2.2",
        )
        self.gateway.start_persistence()
        self.gateway.start()

    def getSensors(self):
        return self.gateway.sensors.values()

    def event(self, message):
        """Callback for mysensors updates"""
        if (
            self.gateway
            and message.node_id != 0
            and message.child_id != 255
            and message.type in [1, 2]
            and self.gateway.is_sensor(message.node_id, message.child_id)
        ):
            child = self.gateway.sensors[message.node_id].children[message.child_id]

            if message.sub_type in [
                0,
                1,
                3,
                4,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                17,
                18,
                23,
                34,
                35,
                37,
                38,
                39,
            ]:
                """ Send float types as float"""
                payload = float(message.payload)
            elif message.sub_type in [
                2,
                15,
                16,
            ]:
                """ Send int types as int"""
                payload = int(message.payload)
            else:
                payload = message.payload

            child_json = {
                "node_id": message.node_id,
                "child_id": message.child_id,
                "child_type": child.type,
                "data_type": message.sub_type,
                "payload": payload,
            }

            if message.type == 1:
                print("sensor_updated: {}".format(json.dumps(child_json)))
            elif message.type == 2:
                print("sensor_request: {}".format(json.dumps(child_json)))
