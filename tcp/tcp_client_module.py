import socket


def connection(host,port,message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    server_address = (host, port)
    sock.connect(server_address)
    try:
        # Send data
        sock.sendall(message)

    finally:
        print('closing socket')
        sock.close()
