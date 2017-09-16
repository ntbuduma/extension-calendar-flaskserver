from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/")
def hi():
    return "yo this works"

@app.route("/add_event", methods=['GET', 'POST'])
def add_event():
    request_data = request.get_data()
    return request_data

if __name__ == "__main__":
	app.run()
