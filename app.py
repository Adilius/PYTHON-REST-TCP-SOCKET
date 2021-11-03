import socket
import sys

HOST = '127.0.0.1'
PORT = 80

# Create server socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket
try:
    serversocket.bind((HOST, PORT))
    print(f'Binding server socket to host:{HOST} and port {PORT}')
except:
    print(f'Bind failed. Error: {str(sys.exc_info())}')
    sys.exit()

# Enable server to accept connections
serversocket.listen(5)

while True:

    # Accept connections
    (clientsocket, address) = serversocket.accept()
    ip, port = str(address[0]), str(address[1])
    print(f'Connection from {ip}:{port} has been established.')

    # Handle connection
    with clientsocket:

        # Listen to incomming data
        while True:
            data = clientsocket.recv(512)


            if data:
                print(data)
