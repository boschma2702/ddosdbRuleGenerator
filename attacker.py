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
next_phase = False
attack_times_all_sigs = dict()


def rewrite_pcap(target_ip: str, target_mac: str, source_pcap: str):
    execute("tcprewrite --dstipmap=0.0.0.0/0:{target_ip}/32 --enet-dmac={target_mac} --infile={pcap_file} "
            "--outfile=attack.pcap".format(target_ip=target_ip, target_mac=target_mac, pcap_file=source_pcap)).wait()


def launch_attack(adapter, speed=1):
    return execute("sudo tcpreplay -i {adapter} --mbps={speed} attack.pcap".format(adapter=adapter, speed=speed)).pid
# sudo tcpreplay -i enp0s25 --mbps=90 attack.pcap
# sudo tcpreplay -i lo attack.pcap


def handle_input(con, data: str):
    global current_attack, current_attack_pid, start_attack, end_attack, attack_times, next_phase
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
    elif data == "NEXT":
        next_phase = True
        s = "SINGLE SIGNATURE TIMES:\n"
        for key in attack_times:
            s += "Times for: {}\n".format(key)
            s += "\n".join(attack_times[key]) + "\n"
        with open("results-attacker.txt", "w") as f:
            f.write(s)
    elif data.startswith("STOP"):
        # Retrieve which attack to start
        prefix = data[4:]
        if current_attack == prefix:
            end_attack = time.clock()
            os.killpg(os.getpgid(current_attack_pid), signal.SIGTERM)

            if not next_phase:
                if current_attack in attack_times:
                    attack_times[current_attack].append(str(end_attack-start_attack))
                else:
                    attack_times[current_attack] = [str(end_attack-start_attack)]
            else:
                if current_attack in attack_times_all_sigs:
                    attack_times_all_sigs[current_attack].append(str(end_attack-start_attack))
                else:
                    attack_times_all_sigs[current_attack] = [str(end_attack-start_attack)]

            current_attack = ""
            current_attack_pid = None
            start_attack = -1
            end_attack = -1
        else:
            pass
            # print("Retrieved {}, while this is not current attack: {}".format(data, current_attack))
    elif data == "QUIT":

        s = "SINGLE SIGNATURE TIMES:\n"
        for key in attack_times:
            s += "Times for: {}\n".format(key)
            s += "\n".join(attack_times[key])+"\n"

        s += "ALL SIGNATURE TIMES\n"
        for key in attack_times_all_sigs:
            s += "Times for: {}\n".format(key)
            s += "\n".join(attack_times_all_sigs[key])+"\n"

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
# rewrite_pcap(target_ip, target_mac, "pcap_files/dd2696c95810dce317587292d6c9a65e.pcap")
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



"""""
start iperf server
iperf3 -s 

start iperf client 
iperf3 -c [server-ip] -R -n 

results target:
Accepted connection from 192.168.0.100, port 38258
[  5] local 192.168.0.102 port 5201 connected to 192.168.0.100 port 38260
[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd
[  5]   0.00-1.00   sec  11.2 MBytes  94.2 Mbits/sec    0    112 KBytes       
[  5]   1.00-2.00   sec  11.2 MBytes  93.8 Mbits/sec    0    112 KBytes       
[  5]   2.00-3.00   sec  11.2 MBytes  93.8 Mbits/sec    0    119 KBytes       
[  5]   3.00-4.00   sec  11.2 MBytes  94.4 Mbits/sec    0    136 KBytes       
[  5]   4.00-5.00   sec  11.5 MBytes  96.4 Mbits/sec    0    136 KBytes       
[  5]   5.00-6.00   sec  11.2 MBytes  93.8 Mbits/sec    0    136 KBytes       
[  5]   6.00-7.00   sec  11.2 MBytes  93.8 Mbits/sec    0    136 KBytes       
[  5]   7.00-8.00   sec  11.1 MBytes  93.3 Mbits/sec    0    191 KBytes       
[  5]   8.00-9.00   sec  11.7 MBytes  98.0 Mbits/sec    0    273 KBytes       
[  5]   9.00-10.00  sec  11.2 MBytes  93.8 Mbits/sec    0    273 KBytes       
[  5]  10.00-10.04  sec   573 KBytes   105 Mbits/sec    0    273 KBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Retr
[  5]   0.00-10.04  sec   113 MBytes  94.6 Mbits/sec    0             sender
[  5]   0.00-10.04  sec  0.00 Bytes  0.00 bits/sec                  receiver
 
results ids pi (no bro):
Accepted connection from 192.168.0.101, port 36910
[  5] local 192.168.0.102 port 5201 connected to 192.168.0.101 port 36912
[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd
[  5]   0.00-1.00   sec  11.4 MBytes  95.8 Mbits/sec    0    109 KBytes       
[  5]   1.00-2.00   sec  11.2 MBytes  93.8 Mbits/sec    0    116 KBytes       
[  5]   2.00-3.00   sec  11.3 MBytes  94.9 Mbits/sec    0    140 KBytes       
[  5]   3.00-4.00   sec  11.2 MBytes  93.8 Mbits/sec    0    140 KBytes       
[  5]   4.00-5.00   sec  11.2 MBytes  93.8 Mbits/sec    0    154 KBytes       
[  5]   5.00-6.00   sec  11.2 MBytes  93.8 Mbits/sec    0    154 KBytes       
[  5]   6.00-7.00   sec  11.2 MBytes  93.8 Mbits/sec    0    154 KBytes       
[  5]   7.00-8.00   sec  11.2 MBytes  93.8 Mbits/sec    0    154 KBytes       
[  5]   8.00-9.00   sec  11.2 MBytes  93.8 Mbits/sec    0    154 KBytes       
[  5]   9.00-10.00  sec  11.2 MBytes  93.8 Mbits/sec    0    154 KBytes       
[  5]  10.00-10.04  sec   636 KBytes   135 Mbits/sec    0    154 KBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Retr
[  5]   0.00-10.04  sec   113 MBytes  94.3 Mbits/sec    0             sender
[  5]   0.00-10.04  sec  0.00 Bytes  0.00 bits/sec                  receiver

results ids pi bro empty rule:
Accepted connection from 192.168.0.101, port 36914
[  5] local 192.168.0.102 port 5201 connected to 192.168.0.101 port 36916
[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd
[  5]   0.00-1.00   sec  11.3 MBytes  94.7 Mbits/sec    0    110 KBytes       
[  5]   1.00-2.00   sec  11.2 MBytes  94.4 Mbits/sec    0    120 KBytes       
[  5]   2.00-3.00   sec  11.2 MBytes  93.8 Mbits/sec    0    120 KBytes       
[  5]   3.00-4.00   sec  11.2 MBytes  93.8 Mbits/sec    0    120 KBytes       
[  5]   4.00-5.00   sec  11.2 MBytes  93.8 Mbits/sec    0    120 KBytes       
[  5]   5.00-6.00   sec  11.2 MBytes  93.8 Mbits/sec    0    120 KBytes       
[  5]   6.00-7.00   sec  11.2 MBytes  93.8 Mbits/sec    0    120 KBytes       
[  5]   7.00-8.00   sec  11.2 MBytes  93.8 Mbits/sec    0    120 KBytes       
[  5]   8.00-9.00   sec  11.7 MBytes  98.0 Mbits/sec    0    171 KBytes       
[  5]   9.00-10.00  sec  11.2 MBytes  93.8 Mbits/sec    0    171 KBytes       
[  5]  10.00-10.04  sec   382 KBytes  75.4 Mbits/sec    0    171 KBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Retr
[  5]   0.00-10.04  sec   113 MBytes  94.3 Mbits/sec    0             sender
[  5]   0.00-10.04  sec  0.00 Bytes  0.00 bits/sec                  receiver

results ids pi with all rules:
Accepted connection from 192.168.0.101, port 36922
[  5] local 192.168.0.102 port 5201 connected to 192.168.0.101 port 36924
[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd
[  5]   0.00-1.00   sec  4.69 MBytes  39.3 Mbits/sec    0    105 KBytes       
[  5]   1.00-2.00   sec  11.2 MBytes  93.8 Mbits/sec    0    110 KBytes       
[  5]   2.00-3.00   sec  11.2 MBytes  94.4 Mbits/sec    0    122 KBytes       
[  5]   3.00-4.00   sec  11.2 MBytes  93.8 Mbits/sec    0    122 KBytes       
[  5]   4.00-5.00   sec  11.4 MBytes  95.9 Mbits/sec    0    136 KBytes       
[  5]   5.00-6.00   sec  11.2 MBytes  94.4 Mbits/sec    0    150 KBytes       
[  5]   6.00-7.00   sec  11.2 MBytes  93.8 Mbits/sec    0    150 KBytes       
[  5]   7.00-8.00   sec  11.5 MBytes  96.4 Mbits/sec    0    212 KBytes       
[  5]   8.00-9.00   sec  11.4 MBytes  95.4 Mbits/sec    0    212 KBytes       
[  5]   9.00-10.00  sec  10.9 MBytes  91.2 Mbits/sec    0    212 KBytes       
[  5]  10.00-10.65  sec  7.39 MBytes  95.9 Mbits/sec    0    212 KBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Retr
[  5]   0.00-10.65  sec   113 MBytes  89.3 Mbits/sec    0             sender
[  5]   0.00-10.65  sec  0.00 Bytes  0.00 bits/sec                  receiver


"""""