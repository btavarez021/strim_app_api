from flask import Flask, render_template, jsonify, request
from requests.exceptions import RequestException
import requests
import json

app = Flask(__name__)

striim_api_url = "http://localhost:5001/api/v1"
auth_path = '/security/authenticate'

SHIP_API_MAP = {"Ship 1":"http://localhost:5001/api/v1", "Ship 2":"http://localhost:5001/api/v1", "Ship 3":"http://localhost:5001/api/v1", 
                "Ship 4":"http://localhost:5001/api/v1", "Ship 5":"http://localhost:5001/api/v1"
                }

@app.route('/')
def index():
    return render_template('index.html')

# def get_token(username, password):
#         payload = {'username': username, 'password': password}

#         try:
#             url = striim_api_url + auth_path
#             resp = requests.post(url, data=payload)
#             if resp.status_code != 200:
#                 return "Likely: wrong username / password"
#             tokenjson = json.loads(resp.text)
#             return tokenjson["token"]
#         except RequestException as ex:
#             raise ex
        
# def health_stats(authToken):
#     resp = requests.get(f'http://{striim_api_url}/health?token={authToken}')
#     data = json.loads(resp.text)
#     print(data)
#     return data


@app.route('/striim/sendcommands', methods=['POST'])
def send_commands_to_ship():

    data = request.get_json()
    selected_ship = data.get('ship')
    command = data.get('command')

    ship_url = SHIP_API_MAP.get(selected_ship)
    print(SHIP_API_MAP[selected_ship] )


    print(f"This is the ship chosen: {selected_ship}")
    print(f"This command was received:{command}")

    if not command or not selected_ship:
        return jsonify({"error": "Commands and ship(s) must be provided"}), 400

    if not ship_url:
        return jsonify({"error": f"Could not find {selected_ship}"}), 404
    
    if len(command) <= 5:
        return jsonify({"error": f"Please enter a longer command."}), 404
    
    payload = {
        "ship": selected_ship, 
        "command": command}
    
    print(f"PAYLOAD: {payload}")
    
    try:
        response = requests.post(f'{ship_url}/server/restart', json=payload)
        if response.status_code == 200:
            # return jsonify(response.json()), 200
            return jsonify({"message": f"Sent command(s) to {selected_ship}"}), 200

        else:
            print(f"failed with statuscode {response.status_code}")
            return jsonify({"error": f"Failed to send command(s) to {selected_ship}"}), response.status_code
    except requests.RequestException as e:
        print(f'RequestException: {str(e)}')
        return jsonify({"error": str(e)}), 500


@app.route('/striim/stop', methods=['POST'])
def stop_server():
    
    selected_ship = request.form.get('ship')
    ship_url = SHIP_API_MAP.get(selected_ship)

    print(SHIP_API_MAP[selected_ship] )


    print(f"Selected ship {selected_ship}")
    print(f"Stopping ship {selected_ship}")

    if not selected_ship:
        return jsonify({"error": "please select a ship"}), 400
    
    if not ship_url:
        return jsonify({"error": f"Could not find {selected_ship}"}), 404

    try:
        response = requests.post(f'{ship_url}/server/stop')
        if response.status_code == 200:
            return jsonify({"message":f"Server on {selected_ship} is stopping", "status":"stopped"}), 200
        elif response.status_code == 202:
            return jsonify({"message":f"Server on {selected_ship} is being stopped", "status":"pending"}), 202
        else:
            return jsonify({"error": f"Failed to stop {selected_ship}"}), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": f"{e}"}), 500
        
@app.route('/striim/start', methods=['POST'])
def start_server():

    selected_ship = request.form.get('ship')
    ship_url = SHIP_API_MAP.get(selected_ship)

    print(SHIP_API_MAP[selected_ship] )

    print(f"Selected ship {selected_ship}")
    print(f"Starting ship {selected_ship}")

    if not selected_ship:
        return jsonify({"error": "please select a ship"}), 400
    

    if not ship_url:
        return jsonify({"error": f"Could not find {selected_ship}"}), 404

    try:
        response = requests.post(f'{ship_url}/server/start')
        if response.status_code == 200:
            return jsonify({"message":f"Server on {selected_ship} is starting", "status":"running"}), 200
        elif response.status_code == 202:
            return jsonify({"message":f"Server on {selected_ship} is being started", "status":"pending"}), 202
        else:
            return jsonify({"error": f"Failed to start {selected_ship}"}), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": f"{e}"}), 500


@app.after_request    
def add_header(response):
    response.headers['Cache-Control'] ='no-store, no-chache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    # auth_token = get_token('admin', 'admin')
    # health_stats(auth_token)
    app.run(debug=True, port=5000)