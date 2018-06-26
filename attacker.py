import os
import signal
import socket, subprocess, time

from definitions import execute, target_ip, target_mac, network_device_attacker
from send_to_attacker import attacker_ip

# target_ip = "192.168.0.101"
# target_mac = "b8:27:eb:a3:b2:b0"


current_attack = ""
current_attack_pid = None
start_attack = -1
end_attack = -1
attack_times = dict()

def rewrite_pcap(target_ip: str, target_mac: str, source_pcap: str):
    execute("tcprewrite --dstipmap=0.0.0.0/0:{target_ip}/32 --enet-dmac={target_mac} --infile={pcap_file} "
            "--outfile=attack.pcap".format(target_ip=target_ip, target_mac=target_mac, pcap_file=source_pcap)).wait()


def launch_attack(adapter, speed=90):
    return execute("sudo tcpreplay -i {adapter} --mbps={speed} attack.pcap".format(adapter=adapter, speed=speed)).pid
# sudo tcpreplay -i enp0s25 --mbps=90 attack.pcap

def handle_input(con, data: str):
    global current_attack, current_attack_pid, start_attack, end_attack, attack_times
    if data == "BENCH":
        pass
    elif data.startswith("START"):
        # Retrieve which attack to start
        prefix = data[5:]
        pcap_path = get_pcap(prefix)

        # Rewrite pcap
        rewrite_pcap(target_ip, target_mac, pcap_path)

        if not current_attack_pid == None:
            print("TWO CONSEQUTIVE STARTS")
            raise RuntimeError("TWO CONSEQUTIVE STARTS")

        # Start attack in new thread, return pid to stop attack once stop command received
        current_attack = prefix
        current_attack_pid = launch_attack(network_device_attacker)
        start_attack = time.clock()
    elif data.startswith("STOP"):
        # Retrieve which attack to start
        prefix = data[4:]
        if current_attack == prefix:
            end_attack = time.clock()
            os.killpg(os.getpgid(current_attack_pid), signal.SIGTERM)
            if current_attack in attack_times:
                attack_times[current_attack].append(str(end_attack-start_attack))
            else:
                attack_times[current_attack] = [str(end_attack-start_attack)]
            current_attack = ""
            current_attack_pid = None
            start_attack = -1
            end_attack = -1
        else:
            pass
            # print("Retrieved {}, while this is not current attack: {}".format(data, current_attack))
    elif data == "QUIT":

        s = ""
        for key in attack_times:
            s += "Times for: {}\n".format(key)
            s += "\n".join(attack_times[key])+"\n"
        with open("results-attacker.txt", "w") as f:
            f.write(s)
        return True
    return False


def get_pcap(prefix: str):
    directory = os.fsencode("pcap_files/")
    # print("PREFIX: {}".format(prefix))
    for f in os.listdir(directory):
        filename = os.fsdecode(f)
        if filename.startswith(prefix):
            return "pcap_files/"+filename




# execute("sleep 5")
# exit(0)
# rewrite_pcap(target_ip, target_mac, "pcap_files/151e8f5150a899830f3812a109c06aac.pcap")
# exit(0)
#
# rewrite_pcap(target_ip, target_mac, "pcap_files/d27fba341533dadddccb7af7a39ab450.pcap")
# exit(0)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (attacker_ip, 10000)
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

q = False
while not q:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        # print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(32).decode("utf-8")
            if data:
                print('received {!r}'.format(data))
                q = handle_input(connection, data)
            else:
                break

    finally:
        # Clean up the connection
        print('connection closed')
        connection.close()


# sudo python3 attacker.py
# sudo python3 ids.py



