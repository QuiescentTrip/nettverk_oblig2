#import socket module
from socket import *
import sys # In order to terminate the program
from time import sleep

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverPort = 8080
serverSocket.bind(('', serverPort))

serverSocket.listen(1)
print('The server is ready to receive')
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
            if filename == "/":
                filename = "/index.html"
            filename = "./static" + filename
            
            f = open(filename)
            outputdata = f.read()
            f.close()
            # Send one HTTP header line into socket
            header = 'HTTP/1.1 200 OK\n\n'
            information = f"{header}\n {open(outputdata)}\r\n"
            print(information)
            connectionSocket.sendall(information.decode())
            connectionSocket.close()

        except IOError:
            # Send response message for file not found
            header = 'HTTP/1.1 404 Not Found\n\n'
            connectionSocket.send(header.encode())
            connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\n".encode())

            # Close client socket
            connectionSocket.close()
except KeyboardInterrupt:
  serverSocket.close()
  sys.exit()