"""HW2-B login-form backend. Demo credentials are for local coursework only."""

from contextlib import closing
from pathlib import Path
import sqlite3

import bcrypt
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4096
DATABASE = Path(__file__).with_name("users.db")

DEMO_EMAIL = "student@example.com"
DEMO_PASSWORD = "StudentPass123!"


def init_db():
    """Create the database and seed one demo account with a salted hash."""
    with closing(sqlite3.connect(DATABASE)) as connection:
        with connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    password_hash BLOB NOT NULL
                )"""
            )
            existing = connection.execute(
                "SELECT id FROM users WHERE email = ?", (DEMO_EMAIL,)
            ).fetchone()

            if existing is None:
                password_hash = bcrypt.hashpw(
                    DEMO_PASSWORD.encode("utf-8"), bcrypt.gensalt()
                )
                connection.execute(
                    "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                    (DEMO_EMAIL, password_hash),
                )


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/login")
def login():
    # Validate on the server even if the browser's checks are bypassed.
    data = request.get_json(silent=True) if request.is_json else request.form

    if not isinstance(data, dict) and not hasattr(data, "get"):
        return jsonify(message="Please submit email and password fields."), 400

    email = data.get("email", "")
    password = data.get("password", "")

    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify(message="Email and password must be text."), 400

    email = email.strip().lower()

    if not email or not password:
        return jsonify(message="Email and password are required."), 400

    if "@" not in email or len(email) > 254:
        return jsonify(message="Enter an email containing @ (maximum 254 characters)."), 400

    if len(password) < 8:
        return jsonify(message="Password must be at least 8 characters."), 400

    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        return jsonify(message="Password must be no more than 72 UTF-8 bytes."), 400

    # The placeholder keeps the email as data, rather than SQL instructions.
    with closing(sqlite3.connect(DATABASE)) as connection:
        user = connection.execute(
            "SELECT password_hash FROM users WHERE email = ?", (email,)
        ).fetchone()

    if user is None or not bcrypt.checkpw(password_bytes, user[0]):
        return jsonify(message="Invalid email or password."), 401

    # This demo verifies credentials; it does not create a persistent session.
    return jsonify(message="Login successful."), 200


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)

