from database_manager import DatabaseManager

db_manager = DatabaseManager('weight_data.db')
db_manager.add_reading(160)
db_manager.import_CSV('weight_data.csv')

print("CSV import complete.")
