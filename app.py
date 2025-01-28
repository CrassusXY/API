from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# Twój Team ID z nRF Cloud
TEAM_ID = "9d162da3-172c-4189-b92c-cf557dc9f0c9"  # Zamień na swój rzeczywisty Team ID

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
            if "appId" in sensor_data:
                app_id = sensor_data["appId"]
                value = sensor_data["data"]
                print(f"Sensor {app_id} - Wartość: {value}")
            elif "x" in sensor_data and "y" in sensor_data and "z" in sensor_data:
                x, y, z = sensor_data["x"], sensor_data["y"], sensor_data["z"]
                print(f"Akcelerometr - X: {x}, Y: {y}, Z: {z}")

    # Tworzenie odpowiedzi z nagłówkiem
    response = make_response(jsonify({"status": "success"}), 200)
    response.headers["x-nrfcloud-team-id"] = TEAM_ID
    return response

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Dynamiczny port dla Render
    app.run(host="0.0.0.0", port=port)
