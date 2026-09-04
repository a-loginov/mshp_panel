import psycopg2
import psycopg2.extras
import config
from flask_login import UserMixin


def _get_db():
    return psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )


def init_db():
    conn = _get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            login VARCHAR(80) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password VARCHAR(256) NOT NULL,
            is_confirmed BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


class User(UserMixin):
    def __init__(self, id, login, email, password, is_confirmed):
        self.id = id
        self.login = login
        self.email = email
        self.password = password
        self.is_confirmed = is_confirmed


def _row_to_user(row):
    if row:
        return User(row["id"], row["login"], row["email"], row["password"], row["is_confirmed"])
    return None


def get_user_by_id(user_id):
    conn = _get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return _row_to_user(row)


def get_user_by_login(login):
    conn = _get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE login = %s", (login,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return _row_to_user(row)


def get_user_by_email(email):
    conn = _get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return _row_to_user(row)


def create_user(login, email, password):
    conn = _get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "INSERT INTO users (login, email, password, is_confirmed) VALUES (%s, %s, %s, FALSE) RETURNING *",
        (login, email, password)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return _row_to_user(row)


def confirm_user(user_id):
    conn = _get_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_confirmed = TRUE WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()


def reject_user(user_id):
    conn = _get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()


def get_all_users():
    conn = _get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, login, email, is_confirmed FROM users ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in rows]


def get_stats():
    conn = _get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM users WHERE is_confirmed = TRUE")
    confirmed = cur.fetchone()[0]
    cur.close()
    conn.close()
    return {"total": total, "confirmed": confirmed, "pending": total - confirmed}


init_db()
