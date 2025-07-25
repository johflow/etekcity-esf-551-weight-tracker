import sqlite3
connection = sqlite3.connect('weight_data.db')
cursor = connection.cursor()
SQLString = """
CREATE TABLE readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    value REAL NOT NULL
);
"""
cursor.execute(SQLString)
connection.commit()
cursor.close()
connection.close()
