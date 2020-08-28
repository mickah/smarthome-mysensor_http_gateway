import mysensors.mysensors as mysensors
import json
import os
from datetime import datetime, timezone
import pymongo
import pickle

from .LocalPersistence import LocalPersistence

class SensorsController:
    """ Sensors Controller class. It handles all interactions with mysensors """

    def __init__(self):
        serial_port = os.environ["MYSENSOR_SERIAL"]
        if serial_port == None:
            print("MYSENSOR_SERIAL env variable missing!")
        else:
            print("Using serial port: " + str(os.environ["MYSENSOR_SERIAL"]))

        self.local_persistence = LocalPersistence()
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

        self.mongodb_client = None
        self.mongodb_database = None
        self.mongodb_collection = None

    def getSensorsRaw(self):
        return self.gateway.sensors.values()

    def event(self, message):
        """Callback for mysensors updates"""
        print(message)
        is_valid_node = self.gateway
        stamp = datetime.now()

        # update node stamp
        node_update = {"stamp":stamp.strftime("%Y-%m-%d %H:%M:%S")}

        if is_valid_node:
            if message.child_id == 255:
                # Pure node update
                if message.command == 0:
                    node_update["type"]=self.getStringPresentation(message.type)
                if message.command == 3:
                    if message.type == 11:
                        node_update["sketch_name"]=message.payload
                    if message.type == 12:
                        node_update["sketch_version"]=message.payload
                    if message.type == 19:
                        node_update["presentation"]=message.payload
                    if message.type == 0:
                        node_update["battery_lvl"]=message.payload

            # update local persistence node
            self.local_persistence.updateNode(node_update)

            is_node_update_or_req = (
                message.child_id != 255
                and message.type in [1, 2]
                and self.gateway.is_sensor(message.node_id, message.child_id)
            )
            is_child_update_or_req = (
                message.child_id != 255
                and message.type in [1, 2]
                and self.gateway.is_sensor(message.node_id, message.child_id)
            )
            if is_child_update_or_req:
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

                    # local last value persistence
                    self.local_persistence.updateChild(message.node_id, message.child_id, child.type, payload, stamp)

                    # mongo db persistence
                    db_interface = self.getDBInterface()
                    if db_interface is not None:
                        try:
                            child_json["date"] = datetime.now()
                            x = db_interface.insert_one(child_json)
                        except Exception as e:
                            print("Could not connect to database: %s" % e)

                elif message.type == 2:
                    print("sensor_request: {}".format(json.dumps(child_json)))

    def getSensorsRecordedValues(self, node_id, child_id):
        db_interface = self.getDBInterface()
        output = {"node_id": node_id, "child_id": child_id, "data": {}}

        if db_interface is not None:
            request = {
                "node_id": node_id,
                "child_id": child_id,
            }
            query_result = db_interface.find(
                request, {"node_id": 0, "child_id": 0}
            ).sort("date")
            for elem in query_result:
                if elem["data_type"] not in output["data"]:
                    output["data"][elem["data_type"]] = {"x": [], "y": []}
                output["data"][elem["data_type"]]["x"].append(elem["date"].isoformat())
                output["data"][elem["data_type"]]["y"].append(elem["payload"])
            return output
        else:
            return {}

    def getSensors(self):
      # List all sensors as JSON
      return self.local_persistence.getSensors()

    def getDBInterface(self):
        if self.mongodb_collection is None:
            self.setup_db_connection()
        return self.mongodb_collection

    def setup_db_connection(self):
        mongo_hostname = os.environ.get("MONGODB_HOSTNAME")
        if mongo_hostname is not None and len(mongo_hostname) > 0:
            database = os.environ.get("MONGODB_DATABASE")
            username = os.environ.get("MONGODB_USERNAME")
            password = os.environ.get("MONGODB_PASSWORD")
            self.mongodb_client = pymongo.MongoClient(
                "mongodb://" + mongo_hostname + ":27017/",
                username=username,
                password=password,
            )
            self.mongodb_database = self.mongodb_client[database]
            self.mongodb_collection = self.mongodb_database["sensors_data"]
            print("Connected to mongodb :)")
            return True
        else:
            return False

    def getStringPresentation(self, number):
        if number == 6:
            return "S_TEMP"
        else if number == 7:
            return "S_HUM"
        else if number == 17:
            return "S_ARDUINO_NODE"
        else if number == 18:
            return "S_ARDUINO_REPEATER_NODE"
        else if number == 35:
            return "S_MOISTURE"
        else:
            return "unknown"    
            

    def __test_feed_dummy_data(self):
        child_json = {
            "node_id": 35,
            "child_id": 3,
            "child_type": 4,
            "data_type": 4,
            "payload": 5.2,
        }
        child_json["date"] = datetime.now()

        print("test inserting : {}".format(child_json))
        db_interface = self.getDBInterface()
        if db_interface is not None:
            try:
                x = db_interface.insert_one(child_json)
                print("test inserted")
            except Exception as e:
                print("Could not connect to database: %s" % e)
