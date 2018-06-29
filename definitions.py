import subprocess, os


attacking_speed = 90


#DEBUG ATTACK PC
# attacker_ip = "127.0.0.1"
# target_mac = "::1"
# target_ip = "127.0.0.1"
# # network_device = "enp0s25"
# network_device_attacker = "lo"
# network_device_ids = "lo"

# #SETUP ATTACK PC
# attacker_ip = "192.168.0.102"
# target_mac = "b8:27:eb:a3:b2:b0"
# target_ip = "192.168.0.100"
# # network_device = "enp0s25"
# network_device_attacker = "enp0s25"
# network_device_ids = "eth0"

#SETUP ATTACK PI
attacker_ip = "192.168.0.102"
target_mac = "b8:27:eb:a3:b2:b0"
target_ip = "192.168.0.100"
# network_device = "enp0s25"
network_device_attacker = "eno1"
network_device_ids = "enp0s25"


def execute(to_execute):
    return subprocess.Popen(to_execute, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)


def send_message(msg: str):
    execute("python3 send_to_attacker.py '{}'".format(msg)).wait()
