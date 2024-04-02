from socket import *
import sys

def handle_client(connectionSocket) -> None:
    """
    Handles client requests, requests are not handled asynchronous
    """
    try:
        message = connectionSocket.recv(1024).decode()

        if not message:
            return

        #gets the string in the http get requests that shows what request should be handled
        filename = message.split()[1]
        
        #reads the entire file
        with open('.' + filename, 'r') as f:
            outputdata = f.read()
        
        
        header = 'HTTP/1.1 200 OK\n\n'
        httpResponse = header + outputdata

        #i ignored loops and sending packets, rather we send the entire message
        #this loops the sends for us
        connectionSocket.sendall(httpResponse.encode())

    except IOError:
        # Prepare and send HTTP response for file not found
        header = 'HTTP/1.1 404 Not Found\n\n'
        errorResponse = header + "<html><head></head><body><h1>404 Not Found</h1></body></html>\n"
        connectionSocket.sendall(errorResponse.encode())

    finally:
        # Ensure the connection is closed after handling the request
        connectionSocket.close()

def start_server(port) -> None:
    '''
    starts a TCP socket and binds it to port 8080.
    if 8080 is busy it goes through each port to find a free one. 
    '''
    serverSocket = socket(AF_INET, SOCK_STREAM)
    not_connected = True
    while not_connected:
        try:
            serverSocket.bind(('', port))
            not_connected = False
        except OSError:
            print(f"Port {port} is busy, trying port {port + 1}")
            port += 1
        except OverflowError:
            print("There are no available ports")
            sys.exit(1)

    serverSocket.listen(5)
    print(f'Server is up at port {port}')

    try:
        while True:
            print('Ready to serve...')
            connectionSocket, addr = serverSocket.accept()
            handle_client(connectionSocket)

    #let's us use ctrl+c to close the server
    except KeyboardInterrupt:
        print("Server is shutting down...")
        serverSocket.close()
        sys.exit()

if __name__ == "__main__":
    '''
    tries to start server on port 8080
    '''
    start_server(8080)

