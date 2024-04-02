import socket
import sys
import argparse

'''
Both check functions are from last oblig, 
I still have the same lower limit as in last oblig for the same reason stated there.  
'''

def check_port(val) -> int:
    '''
    Checks val if val is valid port.
    returns val converted to interger if port is valid.
    '''
    upper_limit, lower_limit = 65535, 1024
    try:
        value = int(val)
    except ValueError:
        raise argparse.ArgumentTypeError('Expected an integer but you entered a string')
    
    if not lower_limit <= value <= upper_limit:
        raise argparse.ArgumentTypeError(f"Invalid port. It must be within the range [{lower_limit},{upper_limit}]")

    return value

def check_ip(val) -> str:
    '''
    Checks if IP is valid.
    Returns IP if valid.
    '''
    #Early return to allow localhost as IP, for convenience
    if val.lower() == "localhost":
        return val
     
    split = val.split(".") 
    if len(split) != 4:
        raise argparse.ArgumentTypeError("The IP needs to be written in standard format")
    for num in split:
        try:
            if not 0 <= int(num) <= 255:
                raise argparse.ArgumentTypeError("The IP needs to be written in standard format")
        except ValueError:
             raise argparse.ArgumentTypeError("The IP address should only contain numbers.")

    return val


def create_http_request(host, path) -> str:
    """
    HTTP GET request in string form
    """
    return f"GET /{path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

def http_client(host, port, path) -> None:
    """
    Sends HTTP GET request to IP and PORT and tries to print file found with path to STDOUT
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        
        client_socket.connect((host, port))
        request = create_http_request(host, path)
        client_socket.sendall(request.encode())
        
        response = ""

        #Vi har ikke en "recvall" så vi må laste filen i deler for hver packet
        while True:
            part = client_socket.recv(1024)
            if not part:
                break
            response += part.decode()
        
        #printer hele responsen sammenhengende
        print(response)

if __name__ == "__main__":
    '''
    standard argparse instructions as specified in the oblig
    '''
    parser = argparse.ArgumentParser(description="HTTP client")
    parser.add_argument("-i", "--ip", type=check_ip, required=True, help="Server IP address or hostname")
    parser.add_argument("-p", "--port", type=check_port, required=True, help="Server port")
    parser.add_argument("-f", "--filename", required=False, default="", help="Path of the requested object")

    args = parser.parse_args()
    
    http_client(args.ip, args.port, args.filename)
