import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.0.110', 10000)
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)


def handle_input(con, data):
    if data == "BENCH":
        return True
    elif data == "START":
        start_attack()
        return True
    return False


def start_attack():
    #start attack to target machine
    print("Starting attack")
    pass


while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(32).decode("utf-8")
            print('received {!r}'.format(data))
            if data:
                if handle_input(connection, data):
                    break
            else:
                break

    finally:
        # Clean up the connection
        print('connection closed')
        connection.close()






