import base64
import json
import os
from pathlib import Path
import re
import zlib

from soslyze.utils import parse_text
from soslyze.utils import print_headline
from soslyze.utils import print_value
from soslyze.utils import Style


class SubscriptionManager:
    def __init__(self, path):
        lines = []
        ent_begin = '-----BEGIN ENTITLEMENT DATA-----'
        ent_end = '-----END ENTITLEMENT DATA-----'

        if os.path.isfile(path + '/etc/rhsm/rhsm.conf'):
            self.platform = parse_text(
                path + '/etc/rhsm/rhsm.conf',
                r"^(hostname|baseurl|port|repo_ca_cert|ca_cert_dir|manage_repos).*")
            self.proxy = parse_text(path + '/etc/rhsm/rhsm.conf', r"^proxy.*")

        if os.path.isfile(path + "/environment"):
            self.env_proxy = parse_text(path + "/environment", r".*proxy.*")
        if not hasattr(self, "env_proxy") or not self.env_proxy:
            self.env_proxy = f"{Style.GREY}No proxy references found, or the ./environment file is missing{Style.RESET}"
        
        self.content_access = False

        if os.path.isdir(path + '/etc/pki/entitlement/'):
            for certname in os.listdir(path + '/etc/pki/entitlement/'):
                with open(f"{path}/etc/pki/entitlement/{certname}",
                          encoding="utf-8") as f:
                    pem = re.findall(
                        f'{ent_begin}(.*?){ent_end}', f.read(), re.DOTALL)
                    b64 = base64.b64decode(pem[0])
                    decompressed = zlib.decompress(b64).decode('utf-8')
                    j = json.loads(decompressed)
                    if "subscription" in j and "sku" in j['subscription']:
                        self.content_access = True
                        break
        if os.path.isfile(
                path + "/sos_commands/subscription_manager/" +
                "subscription-manager_list_--consumed"):
            self.consumed = parse_text(
                path + "/sos_commands/subscription_manager/" +
                "subscription-manager_list_--consumed",
                r"^(Subscription Name|Subskriptionsname|Nom de l'abonnement|" +
                "SKU|Start|Ends|Pool ID|Status Details).*")
        if not hasattr(self, "consumed") or not self.consumed:
            self.consumed = f"{Style.GREY}No subscriptions attached, or the subscription-manager_list_--consumed file is missing{Style.RESET}"

        if os.path.isfile(path + '/var/lib/rhsm/cache/installed_products.json'):
            data = json.loads(Path(path + '/var/lib/rhsm/cache/installed_products.json').read_text())
            self.installed_products = json.dumps(data.get('products', {}), indent=2)

        if os.path.isdir(path + '/etc/rhsm/facts/'):
            for fact in os.listdir(path + '/etc/rhsm/facts/'):
                if fact == 'leapp.facts':
                    continue
                if lines:  # Add newline separator only if not the first item
                    lines.append("")
                lines.append(f"{Style.GREY}{fact}{Style.RESET}")
                lines.append(Path(f"{path}/etc/rhsm/facts/{fact}")
                             .read_text(encoding="utf-8"))
            self.facts = '\n'.join(lines)
            lines.clear()

        if os.path.isfile(
                path + "/sos_commands/subscription_manager/" +
                "subscription-manager_identity"):
            self.lfce = Path(
                path + "/sos_commands/subscription_manager/" +
                "subscription-manager_identity").read_text(encoding="utf-8")
        if os.path.isfile(path + '/dmidecode'):
            parse_text(path + '/dmidecode', r".*uuid.*", options=re.IGNORECASE)

    def output(self):
        print_headline("# SUBSCRIPTIONS & REPOSITORIES")
        if hasattr(self, "platform"):
            print_value("## How is the system registered:", self.platform)
        if hasattr(self, "proxy"):
            print_value("## Proxy information (rhsm.conf):", self.proxy)
        if hasattr(self, "env_proxy"):
            print_value("## Proxy information (env vars):", self.env_proxy)
        if hasattr(self, "content_access"):
            print_value("## SCA:", f"{Style.GREY}{str(self.content_access)}{Style.RESET}")
        if hasattr(self, "consumed"):
            print_value("## Subscriptions attached:", self.consumed)
        if hasattr(self, "installed_products"):
            print_value("## Installed products:", self.installed_products)
        if hasattr(self, "lfce"):
            print_value("## CV, LFCE and organization:", self.lfce)
        if hasattr(self, "facts"):
            print_value("## Custom RHSM facts (leapp.facts omitted):", self.facts)
        if hasattr(self, "uuid"):
            print_value("## RHSM/DMI UUID:", self.uuid)
