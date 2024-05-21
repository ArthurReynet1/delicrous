import sqlite3

connection = sqlite3.connect('Delicrous.db')

cursor = connection.cursor()

print("Opened database successfully")


