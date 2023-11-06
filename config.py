# ip address or domain name
IP = "someDomain.com"

# Policies, i.e. POLICIES = [{"Policy Name 1": "UUID"}, {"Policy Name 2": "UUID"}]
POLICIES = []

# Objects, i.e. OBJECTS = ["networks", "fqdns", "hosts", "ranges", "urls", "urlgroups", "ports", "portobjectgroups", "networkgroups"]
OBJECTS = ["networks", "fqdns", "hosts", "ranges", "urls", "urlgroups", "ports", "portobjectgroups", "networkgroups"]

# Verify SSL Certificate
SSL_VERIFY = True

# Application mapping from Cisco to Palo Alto. Configure by adding more known mappings. {"Cisco app": "Palo Alto app"}
APP_MAPPING = {"HTTP": "web-browsing",
               "HTTPS": "ssl"
               }
