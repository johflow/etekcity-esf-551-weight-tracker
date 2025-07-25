from datetime import datetime
import sqlite3

connection = sqlite3.connect('weight_data.db')
cursor = connection.cursor()

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
data_to_insert = (current_time, 185.0
                  )
cursor.execute("INSERT INTO readings (timestamp, value) VALUES (?, ?)", data_to_insert)

connection.commit()
connection.close()

print("Data succesfully inserted.")
