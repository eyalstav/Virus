import sqlite3

dbConnection = sqlite3.connect("victims.db")
dbCursor = dbConnection.cursor()
dbCursor.execute("CREATE TABLE victims (name TEXT, last_connection TEXT, passwords TEXT)")