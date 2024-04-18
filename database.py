"""create connection to the database and return the connection"""
import sqlite3


def create_connection():
    """
    create connection to database.

    if table "employee" doesn't exists, create it
    """
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS employee
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  department TEXT NOT NULL
                  )"""
    )
    conn.commit()
    return conn
