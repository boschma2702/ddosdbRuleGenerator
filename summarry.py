import os, json


directory = os.fsencode("json_files/")

json_files = []
for f in os.listdir(directory):
    filename = os.fsdecode(f)
    json_files.append((filename, "json_files/"+filename))

for filename, path in json_files:
    id = filename[:4]
    data = json.load(open(path))
    protocol = data["protocol"]

    misc = ""
    if protocol == "ICMP":
        misc += "icmp\\_type = {}".format(str(int(float(data["additional"]["icmp_type"].split(",")[0]))))
        pass
    elif protocol == "NTP":
        pass
    elif protocol == "UDP":
        pass
    elif protocol == "TCP":
        pass
    elif protocol == "DNS":
        misc += "dns\\_query = {}".format(data["additional"]["dns_query"])
        pass
    elif protocol == "IPv4":
        pass

    print("{} & {} & {} & {} & {} & {} \\\\ \\hline".format(id, protocol, str(len(data["src_ips"])), str(len(data[
                                                                                                             "src_ports"])), str(len(data["dst_ports"])), misc))