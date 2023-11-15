# Firewall Migration

## Preface

> [!NOTE]
> Tested with Cisco FMC version `v2.0` and Expedition version `v1.2.72`.

Python scripts for migrating from **Cisco FMC** to **Palo Alto** via Expedition CSV import option.

<br>

## Preparation

Prepare the scripts by modifying `config.py` first. `IP` is the ip address or domain name for the API. `POLICIES` is where you state what policy rules the script will fetch. Likewise, `OBJECTS` is where you define what objects to include.

> You can get the policy UUID from Cisco api explorer.

- Edit `config.py`
  - `IP = "somedomain.com"`
  - `POLICIES = [{"Some Policy 1":"UUID"},{"Some Policy 2":"UUID"}]`
  - `OBJECTS = ["networks", "fqdns", "hosts", "ranges", "urls", "urlgroups", "ports", "portobjectgroups", "networkgroups"]`

<br>

## Get the data

Before running the scripts you need an API user from Cisco FMC with GET privileges. When ready run `Get_objects.py` and `Get_policy.py` as standalone scripts to retrieve the data. The scripts will prompt you for the _username_ and _password_ to the specified Cisco FMC.

- Create API user
- Run `Get_objects` and `Get_policy` separately. And use the credentials from above when prompted.

The data will be saved as a selection of the most important data in JSON format inside the `./data` folder.

### SSL Issues

> [!WARNING]
> Ignore if the retrieval of data was successful.

If the retrieval of data fails because of SSL, and you for some reason want to ignore the SSL certificate verification. You can do so by editing `config.py`.

- Edit `SSL_VERIFY` variable inside `config.py` to **False**

<br>

## Format the data

Now we want to format our JSON data into acceptable CSV data. `format_main.py` is a wrapper for the functions inside `format_json2csv.py` and is responsible for creating the CSV file and writing the CSV header. `format_json2csv.py` is responsible for formating the Cisco objects/policies in raw JSON into equivalent CSV that Expedition understands. Before running the formater, configure `APP_MAPPING` inside `config.py` by adding more known applications. Check out: https://applipedia.paloaltonetworks.com for an overview over paloalto applications.

- Run `format_main` to format the JSON into CSV.

Output data will be inside `./data` folder.

<br>

## CSV Import

> If you are not familiar with how to import via CSV inside Expedition. I recommend reading the first pages from [this](https://live.paloaltonetworks.com/t5/expedition-articles/a-how-to-guide-on-the-import-csv-option/ta-p/258388?attachment-id=8061).

Import Objects in the following order, then Policies. _(The **\*** (star) represents a wildcard)_

- Import Objects _(and other objects you may have included)_

  - `Address-*.csv`
  - `AddressGroups.csv`
  - `Services.csv`
  - `ServiceGroups.csv`
  - `Urls.csv`
  - `UrlGroups.csv`

- Import Policies
  - `SecurityRules_*.csv`

> [!NOTE]
> Because of how PaloAlto differs from Cisco, `SecurityRulesApplications_*.csv` has been added as a reference to inspect the rules from Cisco that include applications. **Note** however that these application security rules are not excluded or separated from **Security\_\*.csv**, simply duplicated. Which means you can safely ignore these reference files if you have no need for them.

<br>

## Compare CSV changes

If you want to compare and output the difference between two or more csv files. Read and modify **Compare_csv.py** by adding csv files you want to compare. Create a new folder inside the working directory called **old**, and move all the old csv files from **./data** folder into **./old**. Then run **Compare_csv.py**. The output will be inside **./data/diff**.

_Compare_csv.py_

```python

# Edit this list if something is missing. e.g checkList_objects = ["Address-Networks.csv"]

checkList_objects = []

```

<br>

## License and Usage

You are free to use, distribute and modify the code however you want under the [MIT](https://mit-license.org/) license.
