import sqlite3 as sql

db_connection = sql.connect("analyzer.db")
cursor = db_connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, user_name STRING REQUIRED, hash_password BINARY REQUIRED)")

cursor.execute("CREATE TABLE IF NOT EXISTS files(file_id BINARY(16) PRIMARY KEY, user_id INTEGER REQUIRED, FOREIGN KEY (user_id) REFERENCES users (user_id))")

db_connection.close()
