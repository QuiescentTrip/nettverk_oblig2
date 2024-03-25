#import socket module
from socket import *
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverPort = 8080
not_connected = True
while not_connected:
    try:
        serverSocket.bind(('', serverPort))
        not_connected = False
    except OSError:
        serverPort += 1
    except OverflowError:
        print("There are no available ports")
        sys.exit(1)

serverSocket.listen(1)

print(f'Server is up at port {serverPort}')
try:
    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        
        try:
            message = connectionSocket.recv(1024).decode()
            if not message:
                continue

            filename = message.split()[1]
            with open('.'+filename, 'r') as f:
                outputdata = f.read()
            # Prepare HTTP response header and content
            header = 'HTTP/1.1 200 OK\n\n'
            httpResponse = header + outputdata

            # Send HTTP response in one go
            connectionSocket.sendall(httpResponse.encode())

        except IOError:
            # Prepare and send HTTP response for file not found
            header = 'HTTP/1.1 404 Not Found\n\n'
            errorResponse = header + "<html><head></head><body><h1>404 Not Found</h1></body></html>\n"
            connectionSocket.sendall(errorResponse.encode())

        finally:
            # Ensure the connection is closed after handling the request
            connectionSocket.close()

except KeyboardInterrupt:
    print("Server is shutting down...")
    serverSocket.close()
    sys.exit()
