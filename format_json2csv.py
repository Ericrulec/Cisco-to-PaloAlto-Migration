import csv
import config

def format_AddressNetworks(filename, jsondata):
    with open(filename, "a+", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        # header.writerow(["name", "ipaddress_cidr", "type"])
        for item in jsondata:
            w.writerow([item["name"],
                        item["value"],
                        item["type"]])

def format_AddressRanges(filename, jsondata):
    with open(filename, "a+", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        # header.writerow(["name", "ipaddress_range", "type"])
        for item in jsondata:
            w.writerow([item["name"],
                        item["value"],
                        item["type"]])

def format_AddressFqdns(filename, jsondata):
    with open(filename, "a+", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        # header.writerow(["name", "ipaddress_cidr", "type"])
        for item in jsondata:
            w.writerow([item["name"],
                        item["value"],
                        item["type"]])

def format_AddressHosts(filename, jsondata):
    with open(filename, "a+", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        # header.writerow(["name", "ipaddress", "ipaddress_range", "type", "ipaddress", "members"])
        for item in jsondata:
            w.writerow([item["name"],
                        item["value"],
                        item["type"]])

def format_AddressUrls(filename, jsondata):
    with open(filename, "a+", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        # header.writerow(["name", "ipaddress_cidr", "type"])
        for item in jsondata:
            w.writerow([item["name"],
                        item["url"],
                        item["type"]])

def format_Ports(filename, jsondata):
    with open(filename, "a+", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        # header.writerow(["name", "port", "protocol"])
        for item in jsondata:
            w.writerow([item["name"],
                        item["port"],
                        item["protocol"].lower()])

def format_Groups(filename, jsondata):
    with open(filename, "a+", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        # header.writerow(["name", "objects"])
        for item in jsondata:
            csvMembers = ""
            for members in item["objects"]:
                csvMembers += members["name"] + ","
            csvMembers = csvMembers[:-1]
            w.writerow([item["name"],
                        csvMembers])


def format_SecurityPolicy(policy_name, jsondata):
    with open(f"data/SecurityRules_{policy_name}.csv", "a+", newline="", encoding="utf-8") as f1, open(f"data/SecurityRulesApplications_{policy_name}.csv", "a+", newline="", encoding="utf-8") as f2:
        w_SR = csv.writer(f1, delimiter=";")
        w_SRA = csv.writer(f2, delimiter=";")

        for item in jsondata:

            # check if disabled rule
            if item["enabled"] == 0:
                print(f'[WARNING] Ignoring disabled rule: {item["name"]}')
                continue

            sourceZones = ""
            if "sourceZones" in item:
                for members in item["sourceZones"]["objects"]:
                    sourceZones += members["name"] + ","
                sourceZones = sourceZones[:-1]

            destinationZones = ""
            if "destinationZones" in item:
                for members in item["destinationZones"]["objects"]:
                    destinationZones += members["name"] + ","
                destinationZones = destinationZones[:-1]

            if item["action"] == "TRUST":
                item["action"] = "ALLOW"

            sourceNetworks = ""
            if "sourceNetworks" in item:
                for members in item["sourceNetworks"]["objects"]:
                    sourceNetworks += members["name"] + ","
                sourceNetworks = sourceNetworks[:-1]
            else:
                sourceNetworks = "any"

            destinationNetworks = ""
            if "destinationNetworks" in item:
                for members in item["destinationNetworks"]["objects"]:
                    destinationNetworks += members["name"] + ","
                destinationNetworks = destinationNetworks[:-1]
            else:
                destinationNetworks = "any"

            sourcePorts = ""
            if "sourcePorts" in item:
                for members in item["sourcePorts"]["objects"]:
                    sourcePorts += members["name"] + ","
                sourcePorts = sourcePorts[:-1]
            else:
                sourcePorts = "any"

            destinationPorts = ""
            if "destinationPorts" in item:
                for members in item["destinationPorts"]["objects"]:
                    destinationPorts += members["name"] + ","
                destinationPorts = destinationPorts[:-1]
            else:
                destinationPorts = "any"

            # IF applications then write to a separate file aswell (data/SecurityRulesApplications.{policy_name}.csv)
            applications = ""
            if "applications" in item:
                for members in item["applications"]["applications"]:
                    member = members["name"]
                    # Define application mapping, to transform Cisco applications into equivalent PaloAlto applications.
                    app_mapping = config.APP_MAPPING
                    if (member in app_mapping):
                        member = app_mapping[member]
                    applications += member + ","
                applications = applications[:-1]
                w_SRA.writerow([item["metadata"]["ruleIndex"],
                                item["name"],
                                sourceZones,
                                destinationZones,
                                item["action"],
                                sourceNetworks,
                                destinationNetworks,
                                applications,
                                sourcePorts,
                                destinationPorts,
                                item["type"]])

            # Write to file policies with no applications
            # HEADER ["index", "name", "from", "to", "action", "src", "dst", "app", "sport", "service", "type"]
            w_SR.writerow([item["metadata"]["ruleIndex"],
                           item["name"],
                           sourceZones,
                           destinationZones,
                           item["action"],
                           sourceNetworks,
                           destinationNetworks,
                           applications,
                           sourcePorts,
                           destinationPorts,
                           item["type"]])

