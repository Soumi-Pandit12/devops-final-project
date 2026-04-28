import os
import time
import pymysql
import pymysql.cursors
from flask import Flask, render_template, request, redirect, url_for

# -- DB config from environment (Defaults match your Docker setup) --
DB_HOST = os.getenv("MYSQL_HOST", "terraform-20260428030748881300000001.cnqimo8iklww.ap-south-1.rds.amazonaws.com")
DB_USER = os.getenv("MYSQL_USER", "notesuser")
DB_PASS = os.getenv("MYSQL_PASSWORD", "notespass")
DB_NAME = os.getenv("MYSQL_DB", "quicknotes_db")

app = Flask(__name__)

def get_db_connection():
    """ Connect to MySQL with retry logic to handle Docker startup delays. """
    for attempt in range(1, 11):
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME,
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=5
            )
            print(f"[DB] Connected successfully on attempt {attempt}")
            return conn
        except pymysql.Error as e:
            print(f"[DB] Connection attempt {attempt}/10 failed. Retrying in 3s...")
            time.sleep(3)
    raise RuntimeError("[DB] Could not connect to MySQL after 10 attempts.")

def init_db():
    """ Automatically creates the notes table if it doesn't exist. """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        conn.commit()
        conn.close()
        print("[DB] Database initialization complete.")
    except Exception as e:
        print(f"[DB] Initialization failed: {e}")

# -- Routes --

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
    # 'note_content' should match the 'name' attribute in your HTML <textarea> or <input>
    content = request.form.get("note_content", "").strip()
    if content:
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

# -- Entry Point --

if __name__ == "__main__":
    init_db()  # <--- CRITICAL: Now uncommented for production
    app.run(host="0.0.0.0", port=5000, debug=False)