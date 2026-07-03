import os
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "festivaldb")
DB_USER = os.getenv("DB_USER", "festivaluser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "festivalpass")
APP_PORT = int(os.getenv("APP_PORT", "5000"))

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def init_db():
    retries = 20
    while retries > 0:
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS concert_info (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    date VARCHAR(100) NOT NULL,
                    location VARCHAR(255) NOT NULL,
                    description TEXT NOT NULL,
                    artists TEXT NOT NULL
                )
            """)

            cursor.execute("SELECT COUNT(*) FROM concert_info")
            count = cursor.fetchone()[0]

            if count == 0:
                cursor.execute("""
                    INSERT INTO concert_info (name, date, location, description, artists)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    "Pacific DevOps Music Fest",
                    "20 de julio de 2026",
                    "Medellín, Colombia",
                    "Festival que reúne música en vivo, innovación tecnológica y cultura DevOps.",
                    "DJ Container, Flask Beats, MySQL Groove, The Compose Band"
                ))
                connection.commit()

            cursor.close()
            connection.close()
            print("Base de datos inicializada correctamente.")
            return
        except Error as e:
            print(f"Esperando a MySQL... Error: {e}")
            retries -= 1
            time.sleep(5)

    raise Exception("No fue posible conectar a MySQL después de varios intentos.")

TICKET_TYPES = [
    {"id": 1, "name": "General", "price": 80000, "benefits": "Acceso general al festival"},
    {"id": 2, "name": "VIP", "price": 150000, "benefits": "Zona VIP + merchandising oficial"},
    {"id": 3, "name": "Backstage", "price": 250000, "benefits": "Acceso backstage + meet & greet"}
]


@app.route("/api/tickets", methods=["GET"])
def get_tickets():
    return jsonify({"tickets": TICKET_TYPES})


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Backend funcionando correctamente"})

@app.route("/api/artists", methods=["GET"])
def get_artists():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT artists FROM concert_info ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()

        cursor.close()
        connection.close()

        if not row:
            return jsonify({"artists": []})

        artists_raw = [a.strip() for a in row["artists"].split(",")]
        artists = [{"id": idx + 1, "name": name} for idx, name in enumerate(artists_raw)]
        return jsonify({"artists": artists})
    except Error as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/concert", methods=["GET"])
def get_concert():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM concert_info ORDER BY id DESC LIMIT 1")
        concert = cursor.fetchone()

        cursor.close()
        connection.close()

        if concert:
            artists = [artist.strip() for artist in concert["artists"].split(",")]
            return jsonify({
                "id": concert["id"],
                "name": concert["name"],
                "date": concert["date"],
                "location": concert["location"],
                "description": concert["description"],
                "artists": artists
            })

        return jsonify({"error": "No hay información del concierto"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/contact", methods=["POST"])
def post_contact():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"status": "error", "message": "Todos los campos son obligatorios"}), 400

    print(f"[CONTACTO] {name} <{email}>: {message}")
    return jsonify({"status": "ok", "message": "Gracias por tu mensaje, te contactaremos pronto."})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=APP_PORT, debug=False)
