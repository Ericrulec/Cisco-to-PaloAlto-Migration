#!/usr/bin/python3

# include the necessary modules
import json
import requests
import os
import getpass
import pathlib
# Files
import requestToken as token
import config

def get_policy(ip: str, header: dict, policy_UUID: str, policy_name: str) -> exit:
    """
    Retrieve relevant policy via GET, and then write to disk.

    Args:
        ip (str):           IPaddress given as a string.
        header (list):      Http header with token inside.
        policy_UUID (str):  Container id under which the specific resource is contained.
        policy_name (str):  What policy you want to target.
    """
    object_list = []
    count = 0
    i = 0
    y = 0
    r = None
    print(f"=> Start getting {policy_name} data")
    while y <= count and i <= 15:
        y = i * 500
        offset = "?offset=" + str(y)
        limit = "&limit=500"
        # we need to update our path to account for the domain UUID and pagination
        path = f"/api/fmc_config/v1/domain/{header['DOMAIN_UUID']}/policy/accesspolicies/{policy_UUID}/accessrules{offset}{limit}&expanded=true"
        try:
            # always verify the SSL cert in prod!
            r = requests.get(f"https://{ip}/{path}", headers=header, verify=config.SSL_VERIFY)
            if (not r.status_code == 200):
                r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            raise SystemExit(errh)
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

        # Loop over data from `r`
        try:
            json_data_dict = r.json()
            count = int(json_data_dict["paging"]["count"])
            if not (json_data_dict.get("items")):
                i += 1
                continue
            for policy in json_data_dict["items"]:
                if (policy["metadata"]["accessPolicy"]["name"] == policy_name):
                    object_list.append(policy)
        except ValueError as e:
            print("Error reading json_data:", e)
        i += 1
    try:
        with open(f'data/policy.{policy_name}.json', 'w', encoding='utf-8') as f:
            print(f"=> Writing {policy_name} data to: {str(os.getcwd())}\\data\\policy.{policy_name}.json")
            json.dump(object_list, f, ensure_ascii=False, indent=4)
    except Exception as err:
        raise SystemExit(err)
    finally:
        print(f"=> Finished writing for policy.{policy_name}.json\n")
        if r:
            r.close()

"""
Run this as a standalone script to retrive the Cisco FMC policies then write them to json file at ./data/*.
"""
if __name__ == "__main__":
    # set needed variables to generate a token
    u = input("Username:")
    p = getpass.getpass("Password:")
    ip = config.IP
    path = "/api/fmc_platform/v1/auth/generatetoken"
    header = {}
    header = token.get_token(ip, path, u, p)

    pathlib.Path('data').mkdir(parents=True, exist_ok=True)

    # retrieve the policies, and then write to file as `policy.{policy}.json`
    policies = config.POLICIES
    for dic in policies:
        for name, uuid in dic.items():
            get_policy(ip, header, uuid, name)

