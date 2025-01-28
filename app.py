from flask import Flask, jsonify, request

app = Flask(__name__)

# Endpoint testowy
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Serwer działa poprawnie!"})

# Endpoint do odbierania danych z nRF Cloud
@app.route("/data", methods=["POST"])
def receive_data():
    data = request.json
    print(f"Otrzymano dane: {data}")  # Możesz je logować do terminala
    return jsonify({"status": "received", "data": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
