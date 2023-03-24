import datetime
import sqlite3

dates = {datetime.date(2023, 3, 12): 10, datetime.date(2023, 1, 11): 47, datetime.date(2023, 1, 10): 53, datetime.date(2023, 1, 9): 14, datetime.date(2023, 1, 7): 102, datetime.date(2023, 1, 4): 28, datetime.date(2022, 12, 26): 27, datetime.date(2022, 12, 22): 208, datetime.date(2022, 12, 21): 189, datetime.date(2022, 12, 20): 88, datetime.date(2022, 12, 19): 79, datetime.date(2022, 12, 17): 8, datetime.date(2022, 12, 15): 57, datetime.date(2022, 12, 14): 20, datetime.date(2022, 12, 13): 19, datetime.date(2022, 12, 12): 233, datetime.date(2022, 12, 7): 47, datetime.date(2022, 12, 1): 7, datetime.date(2022, 11, 28): 4, datetime.date(2022, 11, 25): 2, datetime.date(2022, 11, 24): 13, datetime.date(2022, 11, 18): 29, datetime.date(2022, 10, 27): 38, datetime.date(2022, 10, 26): 65, datetime.date(2022, 10, 25): 60, datetime.date(2022, 10, 21): 152, datetime.date(2022, 10, 20): 25, datetime.date(2022, 10, 19): 65, datetime.date(2022, 10, 18): 16, datetime.date(2022, 10, 12): 257, datetime.date(2022, 9, 28): 1, datetime.date(2023, 2, 2): 57, datetime.date(2023, 1, 23): 25, datetime.date(2023, 1, 20): 3, datetime.date(2023, 1, 19): 82, datetime.date(2023, 1, 18): 89, datetime.date(2023, 1, 15): 79, datetime.date(2023, 1, 6): 26, datetime.date(2023, 1, 5): 44, datetime.date(2022, 12, 28): 96, datetime.date(2022, 12, 11): 2, datetime.date(2022, 12, 10): 6, datetime.date(2022, 12, 6): 29, datetime.date(2022, 12, 5): 1, datetime.date(2022, 11, 21): 20, datetime.date(2022, 11, 7): 21, datetime.date(2022, 10, 17): 160, datetime.date(2023, 2, 11): 1, datetime.date(2023, 1, 17): 20, datetime.date(2023, 1, 16): 7, datetime.date(2023, 1, 14): 6, datetime.date(2023, 1, 3): 15, datetime.date(2023, 1, 2): 75, datetime.date(2022, 12, 29): 35, datetime.date(2022, 11, 30): 5, datetime.date(2022, 11, 19): 10, datetime.date(2022, 11, 16): 8, datetime.date(2022, 11, 15): 221, datetime.date(2022, 11, 12): 6, datetime.date(2022, 11, 8): 291, datetime.date(2022, 11, 6): 63, datetime.date(2022, 11, 4): 17, datetime.date(2022, 11, 3): 1, datetime.date(2022, 11, 2): 14, datetime.date(2022, 11, 1): 11, datetime.date(2022, 10, 24): 56, datetime.date(2022, 10, 22): 18, datetime.date(2022, 10, 16): 2, datetime.date(2022, 10, 13): 21, datetime.date(2022, 10, 5): 214, datetime.date(2022, 9, 27): 40, datetime.date(2022, 9, 23): 5, datetime.date(2022, 9, 20): 104, datetime.date(2022, 11, 17): 239, datetime.date(2023, 2, 23): 1, datetime.date(2023, 3, 10): 1, datetime.date(2023, 3, 3): 6, datetime.date(2023, 3, 1): 24, datetime.date(2023, 2, 22): 9, datetime.date(2023, 2, 21): 8, datetime.date(2023, 2, 17): 7, datetime.date(2023, 2, 16): 58, datetime.date(2023, 2, 3): 10, datetime.date(2023, 2, 1): 80, datetime.date(2023, 1, 30): 11, datetime.date(2023, 1, 25): 12, datetime.date(2023, 1, 22): 92, datetime.date(2023, 1, 21): 6, datetime.date(2023, 1, 13): 17, datetime.date(2023, 1, 8): 27, datetime.date(2023, 1, 1): 16, datetime.date(2022, 12, 31): 8, datetime.date(2022, 12, 25): 2, datetime.date(2022, 12, 24): 7, datetime.date(2022, 12, 18): 8, datetime.date(2022, 12, 4): 7, datetime.date(2022, 11, 29): 8, datetime.date(2022, 11, 23): 1, datetime.date(2022, 11, 22): 9, datetime.date(2022, 11, 20): 19, datetime.date(2022, 11, 14): 72, datetime.date(2022, 11, 10): 68, datetime.date(2022, 11, 9): 96, datetime.date(2022, 10, 30): 312, datetime.date(2022, 10, 28): 3, datetime.date(2022, 10, 23): 297, datetime.date(2022, 10, 14): 13, datetime.date(2022, 10, 10): 11, datetime.date(2022, 10, 9): 16, datetime.date(2022, 10, 7): 26, datetime.date(2022, 10, 6): 12, datetime.date(2022, 10, 3): 5, datetime.date(2022, 10, 2): 171, datetime.date(2022, 9, 22): 166, datetime.date(2022, 9, 21): 44, datetime.date(2023, 1, 24): 42, datetime.date(2023, 3, 6): 4, datetime.date(2023, 2, 9): 1, datetime.date(2023, 1, 12): 116, datetime.date(2022, 11, 27): 2, datetime.date(2022, 10, 11): 10, datetime.date(2022, 10, 4): 124, datetime.date(2023, 3, 2): 1, datetime.date(2023, 2, 12): 35, datetime.date(2023, 3, 17): 10, datetime.date(2023, 2, 27): 5, datetime.date(2023, 2, 15): 9, datetime.date(2023, 2, 13): 32, datetime.date(2022, 12, 23): 1, datetime.date(2022, 12, 9): 1, datetime.date(2023, 2, 20): 1, datetime.date(2023, 3, 18): 1, datetime.date(2023, 1, 31): 1, datetime.date(2023, 1, 29): 6, datetime.date(2023, 1, 27): 9, datetime.date(2023, 3, 5): 1, datetime.date(2023, 3, 4): 4, datetime.date(2023, 2, 25): 2, datetime.date(2022, 12, 3): 1, datetime.date(2022, 12, 2): 2, datetime.date(2023, 3, 11): 2, datetime.date(2023, 2, 10): 1, datetime.date(2023, 1, 26): 2, datetime.date(2023, 3, 13): 3, datetime.date(2022, 12, 27): 10, datetime.date(2022, 11, 11): 16, datetime.date(2022, 10, 15): 2, datetime.date(2022, 10, 1): 50, datetime.date(2022, 9, 26): 4}

#for i in range(dates):

conn = sqlite3.connect('example.db')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Doping EMPLOYEE table if already exists.
# cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

# Creating table as per requirement
# sql = '''CREATE TABLE Messages(
# Date DATETIME NOT NULL,
# Count INT
# )'''
# cursor.execute(sql)
# print("Table created successfully........")
for date in dates:
    cursor.execute("INSERT INTO Messages (DATE, COUNT) VALUES (?, ?)", (date, dates[date]))

# Commit your changes in the database
conn.commit()

#Closing the connection
conn.close()