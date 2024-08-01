import sqlite3 as sql
from .models.user import User

db_connection = sql.connect("user")

def get_db_connection():
    db_connection = sql.connect("user")
    cursor = db_connection.cursor()
    return cursor

