import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Twój Team ID z nRF Cloud
TEAM_ID = "9d162da3-172c-4189-b92c-cf557dc9f0c9"

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Serwer działa poprawnie!"})

@app.route("/data", methods=["POST"])
def receive_data():
    # Odbierz dane w formacie JSON
    data = request.json
    print(f"Otrzymano dane: {data}")

    # Obsługa czujników
    if isinstance(data, dict) and "messages" in data:
        for message in data["messages"]:
            sensor_data = message.get("message", {})

            # Jeśli to dane z czujników (np. TEMP, HUMID, AIR_PRESS)
            if "appId" in sensor_data:
                app_id = sensor_data["appId"]
                value = sensor_data["data"]
                socketio.emit('sensor_data', {"sensor": app_id, "value": value}, broadcast=True)

            # Jeśli to dane z akcelerometru (przyjmiemy ten sam format dla gyro i mag)
            elif "x" in sensor_data and "y" in sensor_data and "z" in sensor_data:
                imu_data = {
                    "imu": {
                        "acc": {
                            "x": sensor_data["x"],
                            "y": sensor_data["y"],
                            "z": sensor_data["z"]
                        },
                        "gyro": {  # Gyro będzie miało te same wartości co acc
                            "x": sensor_data["x"],
                            "y": sensor_data["y"],
                            "z": sensor_data["z"]
                        },
                        "mag": {  # Mag będzie miał te same wartości co acc
                            "x": sensor_data["x"],
                            "y": sensor_data["y"],
                            "z": sensor_data["z"]
                        }
                    }
                }
                socketio.emit('imu_data', imu_data, broadcast=True)

            # Jeśli to dane GPS (latitude, longitude)
            elif "latitude" in sensor_data and "longitude" in sensor_data:
                gps_data = {
                    "location": {
                        "latitude": sensor_data["latitude"],
                        "longitude": sensor_data["longitude"]
                    }
                }
                socketio.emit('gps_data', gps_data, broadcast=True)

    # Tworzenie odpowiedzi z nagłówkiem wymaganym przez nRF Cloud
    response = jsonify({"status": "success"})
    response.headers["x-nrfcloud-team-id"] = TEAM_ID
    return response

@socketio.on('connect')
def on_connect():
    print('Client connected')
    emit('message', {'message': 'Connected to WebSocket!'})

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Dynamiczny port dla Render
    socketio.run(app, host="0.0.0.0", port=port)
