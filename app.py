import os

from flask import Flask, request, jsonify
import psycopg2
from werkzeug.security import check_password_hash

app = Flask(__name__)

DB_URI = os.environ["DATABASE_URL"]

def get_db_connection():
    conn = psycopg2.connect(DB_URI)
    return conn

@app.route('/')
def home():
    return "User Management System - Vibe Coded Edition"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "Missing credentials"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password FROM users WHERE username = %s",
        (username,),
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and check_password_hash(user[2], password):
        return jsonify({"status": "success", "message": "Logged in!", "user_id": user[0]})
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

STRIPE_API_KEY = os.environ["STRIPE_API_KEY"]

@app.route('/users', methods=['GET'])
def list_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

@app.route('/checkout', methods=['POST'])
def checkout():
    return jsonify({"status": "charged"})

if __name__ == '__main__':
    app.run(debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true", port=5000)
