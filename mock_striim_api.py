from flask import Flask, render_template, redirect, jsonify, request
import os 
import requests

app = Flask(__name__)

striim_status = {
    "status": "running"
}

ships = {
    "ships": ["ship 1", "ship 2", "ship 3"]
}

# @app.route("/api/v1/server/opentransactions", methods=['POST'])
# def create_transactions():
#     payload = {
#         "transaction_id": "12345",
#         "amount": "100.50",
#         "currency": "USD"
# }


@app.route('/api/v1/server/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "Status: " + striim_status["status"]
    })

@app.route('/api/v1/server/commands', methods=['GET'])
def show_commands():

    return jsonify({
        "status": striim_status["status"]
    })



@app.route('/api/v1/server/restart', methods=['POST'])
def restart_server():
    if striim_status["status"] == "running":
        striim_status["status"] = "restarting"
        return jsonify({"message": "Server is restarting", "status":"restarting"}), 200
    else:
        return jsonify({"message":"Server is not running, cannot restart", "status": striim_status["status"]}), 400
    
@app.route('/api/v1/server/stop', methods=['POST'])
def stop_server():

    if striim_status["status"] == "running":
        striim_status["status"] = "stopped"
        return jsonify({"message": "Server is stopping", "status":"stopped"}), 200
    else:
        return jsonify({"message":"Server is not running, cannot stop", "status": striim_status["status"]}), 400

@app.route('/api/v1/server/start', methods=['POST'])
def start_server():

    if striim_status["status"] == "stopped":
        striim_status["status"] = "running"
        return jsonify({"message": "Server is starting", "status":"running"}), 200
    else:
        return jsonify({"message":"Server is already running", "status": striim_status["status"]}), 400
        

if __name__ == '__main__':
    app.run(port=5001, debug=True)