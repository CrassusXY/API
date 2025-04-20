from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import Json

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
TEAM_ID = os.getenv("TEAM_ID", "brak_teamu")

app = Flask(__name__)

def insert_message_to_db(data):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id SERIAL PRIMARY KEY,
                data JSONB NOT NULL,
                received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cur.execute("INSERT INTO sensor_data (data) VALUES (%s)", [Json(data)])
        conn.commit()

        cur.close()
        conn.close()
    except Exception as e:
        print(f"[DB ERROR] {e}")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Serwer działa poprawnie!"})

@app.route("/data", methods=["POST"])
def receive_data():
    data = request.get_json()
    print(f"Otrzymano dane: {data}")

    if isinstance(data, dict):
        insert_message_to_db(data)

    response = jsonify({"status": "success"})
    response.headers["x-nrfcloud-team-id"] = TEAM_ID
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
