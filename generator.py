import json

add_src_ip = True
add_dst_ports = True
add_src_ports = True
pretty_print = True

with open('json_files/7bf0c3f9fff85d3fe81f71279d6ae73e.json') as data_file:
    d = json.load(data_file)


def write_rule(rule_name, data):
    rule = "signature {} {".format(rule_name)
    protocol = data["protocol"]

    if pretty_print: rule += "\n"

    if add_src_ip:
        add_to_str(rule, write_src_ips(data["src_ips"]))

    if add_src_ports:
        add_to_str(rule, write_src_ports(data["src_ports"]))

    if add_dst_ports:
        add_to_str(rule, write_dst_ports(data["dst_ports"]))

    if protocol == "ICMP":
        pass
    elif protocol == "NTP":
        pass
    elif protocol == "UDP":
        pass
    elif protocol == "TCP":
        pass

    rule += "}"


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
        return "src-ip == {}".format(", ".join(ports))
    return ""


def write_dst_ports(ports: list):
    if len(ports) > 0:
        return "dst-ip == {}".format(", ".join(ports))
    return ""


def write_dns_query(query: str):
    return "payload /{} /".format(query.replace(".", "\."))


def write_icmp_type(t: int):
    return "header icmp[0:1] == {}".format(str(t))


def add_to_str(rule: str, to_add:str):
    if pretty_print:
        rule += "\t"+to_add+"\n"
    else:
        rule += to_add