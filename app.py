from flask import Flask, redirect
from flask_sock import Sock
from main import run


app = Flask(__name__, static_folder="web", static_url_path="/")


@app.route("/")
def home():
    return redirect("/index.html")


sock = Sock(app)


@sock.route("/websocket")
def route(ws):  # sends { type: letter | eeg | image, data: {} | '' }
    run(ws)

