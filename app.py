import os
import re

from flask import Flask, request, jsonify, session
import psycopg2
from werkzeug.security import check_password_hash
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

Talisman(app)
csrf = CSRFProtect(app)

DB_URI = os.environ["DATABASE_URL"]

def get_db_connection():
    conn = psycopg2.connect(DB_URI)
    return conn

MAX_USERNAME_LENGTH = 150
MAX_PASSWORD_LENGTH = 128
USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_.-]+$")

@app.route('/')
def home():
    return "User Management System - Vibe Coded Edition"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    if not username or not password:
        return jsonify({"status": "error", "message": "Missing credentials"}), 400

    if len(username) > MAX_USERNAME_LENGTH or len(password) > MAX_PASSWORD_LENGTH:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 400

    if not USERNAME_PATTERN.match(username):
        return jsonify({"status": "error", "message": "Invalid credentials"}), 400

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
        session["user_id"] = user[0]
        return jsonify({"status": "success", "message": "Logged in!", "user_id": user[0]})
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

STRIPE_API_KEY = os.environ["STRIPE_API_KEY"]

@app.route('/users', methods=['GET'])
def list_users():
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "Authentication required"}), 401

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
