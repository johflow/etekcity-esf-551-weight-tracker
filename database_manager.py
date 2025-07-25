import sqlite3
from datetime import datetime
import csv

class DatabaseManager:
    db_path = None

    def __init__(self, db_path):
        self.db_path = db_path
        

    def add_reading(self, weight_value, date=None):
        if self.db_path == None:
            return
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        duplicateData = self._find_overlapping_dates(date, cursor)

        if duplicateData is None:
            self._add_new_reading(date, weight_value, cursor)
        else:
            if self._existing_weight_larger(duplicateData, weight_value):
                self._update_existing_reading(date, weight_value, cursor)
        connection.commit()
        connection.close()


    def _find_overlapping_dates(self, date, cursor):
        cursor.execute("SELECT value FROM readings WHERE DATE(timestamp) = ?", (date,))
        return cursor.fetchone()
    

    def _add_new_reading(self, date, weight_value, cursor):
        data_to_insert = (date, weight_value)
        cursor.execute("INSERT INTO readings (timestamp, value) VALUES (?, ?)", data_to_insert)



    def _existing_weight_larger(self, existingData, weight_value):
        existingWeight = existingData[0]
        return existingWeight > weight_value
        

    def _update_existing_reading(self, date, weight_value, cursor):
        cursor.execute("UPDATE readings SET value = ? WHERE DATE(timestamp) = ?", (weight_value, date))

    

    def import_CSV(self, csv_path):
        with open(csv_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                date_string = row[0].split(',')[0]
                datetime_obj = datetime.strptime(date_string, "%m/%d/%Y")
                new_date_str = datetime_obj.strftime("%Y-%m-%d")
                weight_number = row[1].split('l')
                self.add_reading(float(weight_number[0]), new_date_str)
