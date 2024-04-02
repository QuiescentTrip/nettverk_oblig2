from socket import *
import sys

def handle_client(connectionSocket):
    """
    Handles client requests. Each request runs in its own thread.
    """
    try:
        message = connectionSocket.recv(1024).decode()
        if not message:
            return

        filename = message.split()[1]
        print(filename)
        with open('.' + filename, 'r') as f:
            outputdata = f.read()
        header = 'HTTP/1.1 200 OK\n\n'
        httpResponse = header + outputdata
        connectionSocket.sendall(httpResponse.encode())

    except IOError:
        # Prepare and send HTTP response for file not found
        header = 'HTTP/1.1 404 Not Found\n\n'
        errorResponse = header + "<html><head></head><body><h1>404 Not Found</h1></body></html>\n"
        connectionSocket.sendall(errorResponse.encode())

    finally:
        # Ensure the connection is closed after handling the request
        connectionSocket.close()

def start_server(port):
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

    except KeyboardInterrupt:
        print("Server is shutting down...")
        serverSocket.close()
        sys.exit()

if __name__ == "__main__":\
    start_server(8080)

