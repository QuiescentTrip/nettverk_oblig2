import _thread as thread
from socket import *
import sys

'''
if you want a commented version of this code that does not have
to do with multithreading check out the python code in the "task1" folder
'''

def handle_client(connectionSocket):
    '''
    handles client requests. each request runs in its own thread.
    '''
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

            #this is all we need to have it multithreaded.
            #we assign each run of the funciton handle_client to a new thread
            thread.start_new_thread(handle_client, (connectionSocket,))

    except KeyboardInterrupt:
        print("server is shutting down")
        serverSocket.close()
        sys.exit()

if __name__ == "__main__":
    start_server(8080)
