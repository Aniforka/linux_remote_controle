# -*- coding: utf-8 -*-

import os
import time
import requests
from pytube import YouTube
from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/control/full_update", methods=["GET"])
def full_update_system():
    os.system("pacman -Suy")

    return jsonify({'status': 200})

@app.route("/control/reboot", methods=["GET"])
def reboot_system():
    os.system("reboot")

@app.route("/control/immediate_shutdown", methods=["GET"])
def reboot_system():
    os.system("shutdown now")

    return jsonify({'status': 200})

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=7777, allow_unsafe_werkzeug=True) # from 40 to 60000