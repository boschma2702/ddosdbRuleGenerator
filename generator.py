import json

add_src_ip = True
add_dst_ports = True
add_src_ports = True
pretty_print = True


def write_rule(rule_name, data):
    rule = ["signature {} {{".format(rule_name)]
    protocol = data["protocol"]

    if pretty_print: rule.append("\n")

    if add_src_ip:
        add_to_str(rule, write_src_ips(data["src_ips"]))

    if add_src_ports:
        add_to_str(rule, write_src_ports(data["src_ports"]))

    if add_dst_ports:
        add_to_str(rule, write_dst_ports(data["dst_ports"]))

    if protocol == "ICMP":
        add_to_str(rule, write_icmp_type(int(float(data["additional"]["icmp_type"].split(",")[0]))))
        pass
    elif protocol == "NTP":
        pass
    elif protocol == "UDP":
        pass
    elif protocol == "TCP":
        pass
    elif protocol == "DNS":
        add_to_str(rule, write_dns_query(data["additional"]["dns_query"]))
        pass

    rule.append("}")

    return "".join(rule)


def write_protocol(protocol: str):
    return "ip-proto == {}".format(protocol)


def write_src_ips(ips: list):
    if len(ips) > 0:
        return "src-ip == {}".format(", ".join(ips))
    return ""


def write_dst_ips(ips: list):
    if len(ips) > 0:
        return "dst-ip == {}".format(", ".join(ips))
    return ""


def write_src_ports(ports: list):
    if len(ports) > 0:
        s = str(int(ports[0]))
        for i in range(1, len(ports)-1):
            s += str(int(ports[i]))
        return "src-ports == {}".format(s)
    return ""


def write_dst_ports(ports: list):
    if len(ports) > 0:
        s = str(int(ports[0]))
        for i in range(1, len(ports)-1):
            s += ", "+str(int(ports[i]))
        return "dst-ports == {}".format(s)
    return ""


def write_dns_query(query: str):
    return "payload /{} /".format(query.replace(".", "\."))


def write_icmp_type(t: int):
    return "header icmp[0:1] == {}".format(str(t))


def add_to_str(rule: list, to_add:str):
    if not to_add == "":
        if pretty_print:
            rule.append("\t"+to_add+"\n")
        else:
            rule.append(to_add)


with open('json_files/072a16f4c24332ec1dbbc8ea6df36087.json') as data_file:
    d = json.load(data_file)
    print(write_rule("test", d))
