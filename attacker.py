import socket, subprocess




def execute(to_execute):
    print("executing: " + to_execute)
    result = subprocess.run(to_execute, shell=True)
    if result.returncode != 0:
        print(result.stderr)
        raise ValueError("error during executing command: "+to_execute)
    return result


def rewrite_pcap(target_ip: str, target_mac: str, source_pcap: str):
    execute("tcprewrite --dstipmap=0.0.0.0/0:{target_ip}/32 --enet-dmac={target_mac} --infile={pcap_file} "
            "--outfile=attack.pcap".format(target_ip=target_ip, target_mac=target_mac, pcap_file=source_pcap))

"tcpreplay -i {adapter} attack.pcap"
"tcpreplay -i enp0s25 --mbps=90.0 attack.pcap"

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


rewrite_pcap("192.168.0.101", "b8:27:eb:a3:b2:b0", "pcap_files/072a16f4c24332ec1dbbc8ea6df36087.pcap")
exit(0)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.0.110', 10000)
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

while False:
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






