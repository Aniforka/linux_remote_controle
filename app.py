# -*- coding: utf-8 -*-

import os
import json
import time
import requests
from service import Service
from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_socketio import SocketIO, emit

home_directory = os.path.abspath(os.curdir)

def read_data():
    data = list()

    try:
        with open("services.json", 'r', encoding="utf-8") as file_input:
            data = json.load(file_input)
    except Exception: pass

    return data

def save_data(data):
    raw_data = {service.title: service.status for service in data}

    with open("services.json", 'w', encoding="utf-8") as file_output:
        json.dump(raw_data, file_output, ensure_ascii=False, indent=4)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

services = [Service(key, item) for key, item in read_data().items()]


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/services', methods=["GET"])
def services_page():
    return render_template("services.html", services=services)


@app.route("/control/full_update", methods=["GET"])
def full_update_system():
    os.system("pacman -Suy")

    return jsonify({'status': 200})

@app.route("/control/reboot", methods=["GET"])
def reboot_system():
    os.system("reboot")

@app.route("/control/killswitch", methods=["GET"])
def killswitch():
    os.system("shutdown now")

    return jsonify({'status': 200})


@socketio.on('serviceChange')
def changeServiceStatement(data):
    for service in services:
        if service.title == data:
            service.toggle()
            print(service.title, service.status)

    save_data(services)

@socketio.on('serviceUpdate')
def update_service(data):
    for service in services:
        if service.title == data:
            service_directory = service.get_directory()
            os.system(f"cd {service_directory}")
            os.system("git pull")
            os.system(f"cd {home_directory}")

@socketio.on('serviceRestart')
def restart_service(data):
    for service in services:
        if service.title == data:
            service.restart()
    
    save_data(services)


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=7777, allow_unsafe_werkzeug=True) # from 40 to 60000