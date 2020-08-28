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
    sensors_json = sensors_controller.getSensors()
 
    if sensors_json is not None:
        resp = Response(
            response=json.dumps(sensors_json), status=200, mimetype="application/json"
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
