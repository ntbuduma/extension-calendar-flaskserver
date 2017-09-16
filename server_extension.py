from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/add_event", methods=['GET', 'POST'])
def add_event():
    request_data = request.get_data()
