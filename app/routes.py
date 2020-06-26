from app import app
import json
from .SensorsController import SensorsController

sensors_controller = SensorsController()

@app.route('/')
@app.route('/index')
def index():
    return "Welcome to mysensor API server"

@app.route('/sensors', methods=['GET'])
def sensors():
    print(sensors_controller.getSensors())
    return json.dumps(list(sensors_controller.getSensors()))
