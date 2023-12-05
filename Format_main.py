#!/usr/bin/python3

import json
import csv
import config
import format_json2csv as j2c

"""
Usage: Format data from `get_objects.py` and `get_policy.py` into csv data that Palo Alto Expedition accepts.
When: Run as a standalone script *after* running `get_objects.py` and `get_policy.py`.
"""
if __name__ == "__main__":
    # Write CSV Header, i.e. Column Header for each Address object

    # Address-fqdns.csv
    with open("data/Address-fqdns.csv", "w", newline="", encoding="utf-8") as f:
        header = csv.writer(f, delimiter=";")
        header.writerow(["name", "ipaddress_cidr", "type"])
    with open("data/json/objects.fqdns.json", 'r', encoding='utf-8') as f:
        python_obj = json.load(f)
        j2c.format_AddressFqdns("data/Address-fqdns.csv", python_obj)

    # Address-Hosts.csv
    with open("data/Address-Hosts.csv", "w", newline="", encoding="utf-8") as f:
        header = csv.writer(f, delimiter=";")
        header.writerow(["name", "ipaddress", "type"])
    with open("data/json/objects.hosts.json", 'r', encoding='utf-8') as f:
        python_obj = json.load(f)
        j2c.format_AddressHosts("data/Address-Hosts.csv", python_obj)

    # Address-Networks.csv
    with open("data/Address-Networks.csv", "w", newline="", encoding="utf-8") as f:
        header = csv.writer(f, delimiter=";")
        header.writerow(["name", "ipaddress_cidr", "type"])
    with open("data/json/objects.networks.json", 'r', encoding='utf-8') as f:
        python_obj = json.load(f)
        j2c.format_AddressNetworks("data/Address-Networks.csv", python_obj)

    # Address-Ranges.csv
    with open("data/Address-Ranges.csv", "w", newline="", encoding="utf-8") as f:
        header = csv.writer(f, delimiter=";")
        header.writerow(["name", "ipaddress_range", "type"])
    with open("data/json/objects.ranges.json", 'r', encoding='utf-8') as f:
        python_obj = json.load(f)
        j2c.format_AddressRanges("data/Address-Ranges.csv", python_obj)

    # Networkgroups.csv
    with open("data/AddressGroups.csv", "w", newline="", encoding="utf-8") as f:
        header = csv.writer(f, delimiter=";")
        header.writerow(["name", "members"])
    with open("data/json/objects.networkgroups.json", 'r', encoding='utf-8') as f:
        python_obj = json.load(f)
        j2c.format_Groups("data/AddressGroups.csv", python_obj)

    # Ports.csv
    with open("data/Services.csv", "w", newline="", encoding="utf-8") as f:
        header = csv.writer(f, delimiter=";")
        header.writerow(["name", "dport", "protocol"])
    with open("data/json/objects.ports.json", 'r', encoding='utf-8') as f:
        python_obj = json.load(f)
        j2c.format_Ports("data/Services.csv", python_obj)

    # PortsGroups.csv
    with open("data/ServiceGroups.csv", "w", newline="", encoding="utf-8") as f:
        header = csv.writer(f, delimiter=";")
        header.writerow(["name", "members"])
    with open("data/json/objects.portobjectgroups.json", 'r', encoding='utf-8') as f:
        python_obj = json.load(f)
        j2c.format_Groups("data/ServiceGroups.csv", python_obj)

    # Urls.csv
    with open("data/Urls.csv", "w", newline="", encoding="utf-8") as f:
        header = csv.writer(f, delimiter=";")
        header.writerow(["name", "ipaddress_cidr", "type"])
    with open("data/json/objects.urls.json", 'r', encoding='utf-8') as f:
        python_obj = json.load(f)
        j2c.format_AddressUrls("data/Urls.csv", python_obj)

    # UrlGroups.csv
    with open("data/UrlGroups.csv", "w", newline="", encoding="utf-8") as f:
        header = csv.writer(f, delimiter=";")
        header.writerow(["name", "members"])
    with open("data/json/objects.urlgroups.json", 'r', encoding='utf-8') as f:
        python_obj = json.load(f)
        j2c.format_Groups("data/UrlGroups.csv", python_obj)

    # Security Rules
    policies = config.POLICIES
    for dic in policies:
        for policy_name, uuid in dic.items():
            with open(f"data/SecurityRules_{policy_name}.csv", "w", newline="", encoding="utf-8") as f:
                header = csv.writer(f, delimiter=";")
                header.writerow(["index", "name", "from", "to", "action", "src", "dst", "app", "sport", "service", "type"])
            with open(f"data/SecurityRulesApplications_{policy_name}.csv", "w", newline="", encoding="utf-8") as f:
                header = csv.writer(f, delimiter=";")
                header.writerow(["index", "name", "from", "to", "action", "src", "dst", "app", "sport", "service", "type"])
            with open(f"data/json/policy.{policy_name}.json", 'r', encoding='utf-8') as f:
                python_obj = json.load(f)
                j2c.format_SecurityPolicy(policy_name, python_obj)


