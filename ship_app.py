from flask import Flask, render_template, jsonify, request
from requests.exceptions import RequestException
import requests

app = Flask(__name__)

striim_api_url = "http://localhost:5001/api/v1"

SHIP_API_MAP = {"Ship 1":"http://ship1", "Ship 2":"http://localhost:5001/api/v1", "Ship 3":"http://ship3", "Ship 4":"http://ship4", "Ship 5":"http://ship5"
                }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/striim/sendcommands', methods=['POST'])
def send_commands_to_ship():

    ship = request.form.get('ship').capitalize()
    commands = request.form.get('commands')

    api_url = SHIP_API_MAP.get('ship')
    
    if not commands or not ship:
        return jsonify({"error": "Commands and ship(s) must be provided"}), 400

    print(f"This is the ship chosen: {ship}")
    print(f"This command was received:{commands}")

    try:
        response = requests.post(f'{api_url}/server/commands', json={"commands": commands, "ship": ship})
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to send command"}), response.status_code

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)