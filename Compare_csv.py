"""
Run this as a standalone script to compare the difference between csv files. Script is tailormade for the returned data from the previous scripts.
Diff files will be placed inside `./data/diff`.

===NOTE===
Before running this script create a folder named `old` and move all the old csv files you want to compare into this folder.
"""
import pathlib
import config

# Edit this list if something is missing. e.g checkList_objects = ["Address-Networks.csv"]
CHECKLIST_OBJECTS = ["Address-fqdns.csv", "Address-Hosts.csv", "Address-Networks.csv", "Address-Ranges.csv",
                     "AddressGroups.csv", "Services.csv", "ServiceGroups.csv", "Urls.csv", "UrlGroups.csv"]

if __name__ == "__main__":
    pathlib.Path('data/diff').mkdir(parents=True, exist_ok=True)
    # ===================== #
    # Compare Objects csv's
    # ===================== #
    for name in CHECKLIST_OBJECTS:
        try:
            with open(f"./old/{name}", 'r') as t1, open(f"./data/{name}", 'r') as t2:
                fileone = t1.readlines()
                filetwo = t2.readlines()

            with open(f"./data/diff/diff_{name}", 'w') as outFile:
                for line in filetwo:
                    if line not in fileone:
                        outFile.write(line)
        except FileNotFoundError as err:
            print("Error: ", err)

    # ===================== #
    # Compare Policies csv's
    # ===================== #
    policies = config.POLICIES
    for dic in policies:
        for policy_name, uuid in dic.items():
            checklist = [f"SecurityRules_{policy_name}.csv", f"SecurityRulesApplications_{policy_name}.csv"]
            for name in checklist:
                try:
                    with open(f"./old/{name}", 'r') as t1, open(f"./data/{name}", 'r') as t2:
                        fileone = t1.readlines()
                        filetwo = t2.readlines()

                    with open(f"./data/diff/diff_{name}", 'w') as outFile:
                        for line in filetwo:
                            if line not in fileone:
                                outFile.write(line)
                except FileNotFoundError as err:
                    print("Error: ", err)
