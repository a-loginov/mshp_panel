import sqlite3
import os
from flask_login import UserMixin

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mshp.db")


def _get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_confirmed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


class User(UserMixin):
    def __init__(self, id, login, email, password, is_confirmed):
        self.id = id
        self.login = login
        self.email = email
        self.password = password
        self.is_confirmed = bool(is_confirmed)


def get_user_by_id(user_id):
    conn = _get_db()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if row:
        return User(row["id"], row["login"], row["email"], row["password"], row["is_confirmed"])
    return None


def get_user_by_login(login):
    conn = _get_db()
    row = conn.execute("SELECT * FROM users WHERE login = ?", (login,)).fetchone()
    conn.close()
    if row:
        return User(row["id"], row["login"], row["email"], row["password"], row["is_confirmed"])
    return None


def get_user_by_email(email):
    conn = _get_db()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    if row:
        return User(row["id"], row["login"], row["email"], row["password"], row["is_confirmed"])
    return None


def create_user(login, email, password):
    conn = _get_db()
    cursor = conn.execute(
        "INSERT INTO users (login, email, password, is_confirmed) VALUES (?, ?, ?, 0)",
        (login, email, password)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return get_user_by_id(user_id)


def confirm_user(user_id):
    conn = _get_db()
    conn.execute("UPDATE users SET is_confirmed = 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


def reject_user(user_id):
    conn = _get_db()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


def get_all_users():
    conn = _get_db()
    rows = conn.execute("SELECT * FROM users ORDER BY id").fetchall()
    conn.close()
    return [
        {"id": r["id"], "login": r["login"], "email": r["email"], "is_confirmed": bool(r["is_confirmed"])}
        for r in rows
    ]


def get_stats():
    conn = _get_db()
    total = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    confirmed = conn.execute("SELECT COUNT(*) FROM users WHERE is_confirmed = 1").fetchone()[0]
    conn.close()
    return {"total": total, "confirmed": confirmed, "pending": total - confirmed}


init_db()
