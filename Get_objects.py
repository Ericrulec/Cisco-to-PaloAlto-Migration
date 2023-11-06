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

def get_objects(ip: str, header: dict, obj: str) -> list:
    """
    Retrieve relevant objects via GET, and writes to disk (json) the composed list of these objects.

    Args:
        ip (str):       Ipaddress given as a string.
        header (list):  Http header with token inside.
        obj (str):      What object you want to target.
    """
    object_list = []
    count = 0
    i = 0
    y = 0
    r = None
    print(f"=> Start getting {obj} data")
    while y <= count and i <= 80:
        y = i * 500
        offset = "?offset=" + str(y)
        limit = "&limit=500"
        # we need to update our path to account for the domain UUID and pagination
        path = f"/api/fmc_config/v1/domain/{header['DOMAIN_UUID']}/object/{obj}{offset}{limit}&expanded=true"
        try:
            # always verify the SSL cert in prod!
            r = requests.get(f"https://{ip}/{path}", headers=header, verify=config.VERIFY)
            if (not r.status_code == 200):
                r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            raise SystemExit(errh)
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

        try:
            json_data_dict = r.json()
            count = int(json_data_dict["paging"]["count"])
            if not (json_data_dict.get("items")):
                i += 1
                continue
            for objects in json_data_dict["items"]:
                object_list.append({
                    "name": objects.get("name", ""),
                    "value": objects.get("value", ""),
                    "type": objects.get("type", ""),
                    "port": objects.get("port", ""),
                    "protocol": objects.get("protocol", ""),
                    "url": objects.get("url", ""),
                    "id": objects.get("id", ""),
                    "objects": objects.get("objects", "")})
        except ValueError as e:
            print("Error reading json_data:", e)
        i += 1
    try:
        with open(f'data/objects.{obj}.json', 'w', encoding='utf-8') as f:
            print(f"=> Writing {obj} data to: {str(os.getcwd())}\\data\\objects.{obj}.json")
            json.dump(object_list, f, ensure_ascii=False, indent=4)
    except Exception as err:
        raise SystemExit(err)
    finally:
        print(f"=> Finished writing for objects.{obj}.json\n")
        if r:
            r.close()

"""
Run this as a standalone script to retrive the Cisco FMC objects then write them to json file at ./data/*.
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

    objects = config.OBJECTS
    # retrieve the objects, and then write to file as `objects.{obj}.json`
    for obj in objects:
        get_objects(ip, header, obj)

