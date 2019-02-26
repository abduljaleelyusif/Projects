# server
# TCP Server Code

# host="127.0.0.1"                # Set the server address to variable host
host = "127.168.2.75"  # Set the server address to variable host
port = 4446  # Sets the variable port to 4444

from socket import *  # Imports socket module

s = socket(AF_INET, SOCK_STREAM)
s.bind((host, port))  # Binds the socket. Note that the input to
# the bind function is a tuple
s.listen(1)  # Sets socket to listening state with a  queue
# of 1 connection

print("Listening for connections.. ")
client, addr = s.accept()  # Accepts incoming request from client and returns
# socket and address to variables q and addr

# user
q.send(data)  # Sends data to client
s.close()
# End of code

# Client
# TCP Client Code

# host="127.0.0.1"            # Set the server address to variable host

host = "127.168.2.75"
port = 4446  # Sets the variable port to 4444

from socket import *  # Imports socket module

s = socket(AF_INET, SOCK_STREAM)  # Creates a socket
s.connect((host, port))  # Connect to server address

msg = s.recv(1024)  # Receives data upto 1024 bytes and stores in variables msg

print("Message from server : " + msg.strip().decode('ascii'))

s.close()  # Closes the socket