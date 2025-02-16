from flask import Flask, redirect
from flask_sock import Sock
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
import time
import numpy as np
import json
from main import run


app = Flask(__name__, static_folder="web", static_url_path="/")


@app.route("/")
def home():
    return redirect("/index.html")


sock = Sock(app)


@sock.route("/websocket")
def route(ws):  # sends { type: letter | eeg, data: {} | '' }
    run(ws)

