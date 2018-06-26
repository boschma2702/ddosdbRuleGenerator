import json
import os
import signal
import time

import generator
from definitions import execute, send_message, network_device_ids

runs = 2

def time_send():
    times = []
    for i in range(0, runs):
        start = time.clock()
        send_message("BENCH")
        end = time.clock()
        times.append(str(end-start))
    return times


def generate_signature(filename, file):
    json_file = json.load(file)
    rule_name = "STOP"+filename[:4]
    with open("sig.sig", "w") as sig_file:
        rule = generator.write_rule(rule_name, json_file)
        sig_file.write(rule)


def time_generate_file(filename, file_path):
    times = []
    for i in range(0, runs):
        start = time.clock()
        generate_signature(filename, open(file_path))
        stop = time.clock()
        times.append(str(stop-start))
    return times


def start_bro():
    # return execute("sudo /usr/local/bro/bin/bro -b -i eth0 sigEventHandler.bro").pid
    return execute("sudo /usr/local/bro/bin/bro -b -i {} /home/boschma/Documents/ddosdbRuleGenerator/sigEventHandler.bro".format(network_device_ids)).pid


def stop_bro(pid):
    os.killpg(os.getpgid(pid), signal.SIGTERM)


# generate_signature("7bf0c3f9fff85d3fe81f71279d6ae73e.json", 'json_files/7bf0c3f9fff85d3fe81f71279d6ae73e.json')



if __name__ == '__main__':
    time_sending = "send to attacker times: \n{}\n".format("\n".join(time_send()))

    directory = os.fsencode("json_files/")

    json_files = []
    for f in os.listdir(directory):
        filename = os.fsdecode(f)
        json_files.append((filename, "json_files/"+filename))

    generating_times = ""
    for fn, p in json_files:
        generating_times += "Time for: {}\n".format(fn)
        generating_times += "\n".join(time_generate_file(fn, p))+"\n"

    with open("results-ids.txt", "w") as f:
        f.write(time_sending + generating_times)

    print("Starting attacks")
    # handle attacks
    for fn, p in json_files:
        # generate sig
        generate_signature(fn, open(p))
        for i in range(0, runs):
            # start bro
            pid = start_bro()
            # Send start command of attack
            send_message("START"+fn[:4])
            time.sleep(7)
            # Kill bro
            stop_bro(pid)

    send_message("QUIT")


    pass


