"""
QuickNotes - Flask Application
A lightweight CRUD web app for managing personal notes.
Connects to a MySQL database via PyMySQL.
"""

import os
import time
import pymysql
import pymysql.cursors
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

# ── DB config from environment ─────────────────────────────────────
DB_HOST = os.getenv("MYSQL_HOST", "mysql")
DB_USER = os.getenv("MYSQL_USER", "notesuser")
DB_PASS = os.getenv("MYSQL_PASSWORD", "notespass")
DB_NAME = os.getenv("MYSQL_DB", "quicknotes_db")

app = Flask(__name__)


def get_db_connection():
    """
    Connect to MySQL with retry logic.
    Retries up to 10 times (30s total) — handles Docker startup delay.
    """
    for attempt in range(1, 11):
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME,
                connect_timeout=5
            )
            print(f"[DB] Connected on attempt {attempt}")
            return conn
        except pymysql.Error as e:
            print(f"[DB] Attempt {attempt}/10 failed: {e}")
            time.sleep(3)
    raise RuntimeError("[DB] Could not connect to MySQL after 10 attempts. Exiting.")


def init_db():
    """Create the notes table if it doesn't exist."""
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id         INT AUTO_INCREMENT PRIMARY KEY,
                content    TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()
    conn.close()
    print("[DB] Table ready.")


# ── Routes ─────────────────────────────────────────────────────────

@app.route("/")
def index():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC")
        all_notes = cursor.fetchall()
    conn.close()
    return render_template("index.html", notes=all_notes)


@app.route("/add", methods=["POST"])
def add_note():
    content = request.form.get("note_content", "").strip()
    if not content:
        return redirect(url_for("index"))
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO notes (content) VALUES (%s)", (content,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


# ── Entry Point ────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
