from flask import Flask
from flask import request
import calendar_helper
import json
app = Flask(__name__)

@app.route("/")
def hi():
    return "yo this works"

@app.route("/add_event", methods=['POST'])
def add_event():
    request_data = request.get_data()
    return json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True)

@app.route("/get_event_list", methods=['GET'])
def get_event_list():
    return calendar_helper.getEventList();

@app.route("/get_event_grid", methods=['GET'])
def get_event_grid():
    pass

if __name__ == "__main__":
	app.run()
