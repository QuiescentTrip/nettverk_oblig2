import socket
import sys
import argparse

def create_http_request(host, path):
    """
    Create a simple HTTP GET request for a given host and path.
    """
    return f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

def http_client(host, port, path):
    """
    Simple HTTP client that sends a GET request to a specified host and port,
    and prints the server response.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        request = create_http_request(host, path)
        client_socket.sendall(request.encode())
        
        response = ""
        while True:
            part = client_socket.recv(1024)
            if not part:
                break
            response += part.decode()
        
        print(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple HTTP client")
    parser.add_argument("-i", "--ip", required=True, help="Server IP address or hostname")
    parser.add_argument("-p", "--port", type=int, required=True, help="Server port")
    parser.add_argument("-f", "--filename", required=True, help="Path of the requested object")

    args = parser.parse_args()
    
    http_client(args.ip, args.port, args.filename)
