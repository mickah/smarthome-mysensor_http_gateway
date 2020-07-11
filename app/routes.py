from app import app
import json
from flask import Response
from .SensorsController import SensorsController

# Create the controller instance
sensors_controller = SensorsController()


@app.route("/")
@app.route("/index")
def index():
    return "Welcome to mysensors API server"


@app.route("/sensors", methods=["GET"])
def sensors():
    # List all sensors as JSON
    node_json = None
    sensors_json = {}
    for node in sensors_controller.getSensors():
        child_list = []
        for ch_id in node.children:
            child = node.children[ch_id]
            child_list.append(
                {
                    "child_id": ch_id,
                    "child_type": child.type,
                    "description": child.description,
                    "values": child.values,
                    "stamp": sensors_controller.getLiveStampStr(
                        node.sensor_id, ch_id, child.type
                    ),
                }
            )

        node_json = {
            "sensor_id": node.sensor_id,
            "sketch_name": node.sketch_name,
            "sketch_version": node.sketch_version,
            "battery_level": node.battery_level,
            "heartbeat": node.heartbeat,
            "protocol_version": node.protocol_version,
            "children": child_list,
        }
        sensors_json[node.sensor_id] = node_json
    if node_json is not None:
        resp = Response(
            response=json.dumps(node_json), status=200, mimetype="application/json"
        )
        return resp
    else:
        resp = Response(
            response=json.dumps({}), status=503, mimetype="application/json"
        )
        return resp


@app.route("/sensors/id/<sensor_id>/<child_id>", methods=["GET"])
def sensors_data(sensor_id, child_id):
    # List all sensors as JSON
    data = sensors_controller.getSensorsRecordedValues(int(sensor_id), int(child_id))

    if data is not None:
        resp = Response(
            response=json.dumps(data), status=200, mimetype="application/json"
        )
        return resp
    else:
        resp = Response(
            response=json.dumps({}), status=503, mimetype="application/json"
        )
        return resp
