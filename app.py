from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import json
from init_db import init_db_once

# Wczytaj zmienne środowiskowe
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
TEAM_ID = 

init_db_once()

app = Flask(__name__)
engine = create_engine(DATABASE_URL)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Server is running!"})

@app.route("/data", methods=["POST"])
def receive_data():
    data = request.json
    print(f"Otrzymano dane: {data}")

    # Zapisz całą wiadomość jako tekst
    try:
        with engine.connect() as conn:
            query = text("INSERT INTO messages (raw_data) VALUES (:raw)")
            conn.execute(query, {"raw": json.dumps(data)})
            conn.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    response = jsonify({"status": "success"})
    response.headers["x-nrfcloud-team-id"] = TEAM_ID
    return response

@app.route("/logs", methods=["GET"])
def get_logs():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM messages ORDER BY timestamp DESC LIMIT 100"))
            logs = [dict(row) for row in result]
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
