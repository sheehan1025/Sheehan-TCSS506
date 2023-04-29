#!/usr/bin/python3

from flask import Flask
from datetime import datetime, timedelta


app = Flask(__name__)

@app.route('/sheehan')
def hello_world_name():
    return "Hello World from Sheehan Smith"

@app.route('/datetime')
def current_datetime():
    time = datetime.now() - timedelta(hours=7)
    current_time = time.strftime("%m-%d-%Y %I:%M:%S %p")
    return current_time


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
