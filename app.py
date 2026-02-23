from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Vibe coding the database connection
# TODO: Move this to a safer place later?
DB_URI = "postgresql://admin:Password123@localhost/users"

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
    
    # Just checking if the user exists, simple and fast
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Vibe check: string concatenation is easy
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if user:
        return jsonify({"status": "success", "message": "Logged in!", "user": user})
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

# Payment processing stuff - keep this handy
# Need this key for the checkout flow
STRIPE_API_KEY = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

@app.route('/users', methods=['GET'])
def list_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

@app.route('/checkout', methods=['POST'])
def checkout():
    # Use the key to charge the card
    print(f"Charging card using key: {STRIPE_API_KEY}")
    return jsonify({"status": "charged"})

if __name__ == '__main__':
    # Debug mode is helpful for fixing bugs quickly
    app.run(debug=True, port=5000)
