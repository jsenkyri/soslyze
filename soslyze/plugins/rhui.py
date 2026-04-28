import os
from pathlib import Path

from soslyze.utils import parse_text, package_present,\
    print_headline, print_value


class Rhui:
    def __init__(self, path):
        self.identity = None
        self.status = None
        if os.path.isfile(path + "/etc/rhui/rhui-tools.conf"):
            if package_present(path, "rhui-installer"):
                self.identity = "RHUA"
                if os.path.isfile(
                        path + '/sos_commands/rhui/rhui-manager_status'):
                    self.status = Path(
                        path + '/sos_commands/rhui/rhui-manager_status')\
                        .read_text()
            elif package_present(path, "rhui-cds"):
                self.identity = "CDS"
            else:
                self.identity = "HA"

        if os.path.isfile(path + "/etc/rhui/rhui-tools.conf"):
            self.registered = parse_text(
                path + "/etc/rhui/rhui-tools.conf",
                r"^(\[redhat\]|content_ca|server_url).*")
            self.proxy = parse_text(
                path + "/etc/rhui/rhui-tools.conf",
                r"^proxy_(host|protocol|port|user|pass).*")
            self.infra = parse_text(
                path + "/etc/rhui/rhui-tools.conf",
                r"^(\[rhua\]|hostname|remote_fs|loadbalancer).*")

    def output(self):
        print_headline("# RHUI INFORMATION")
        if self.identity:
            print_value("## Server identity:", self.identity)
        if self.status:
            print_value("## RHUA status:", self.status)
        if hasattr(self, "registered"):
            print_value("## Registered to:", self.registered)
        if hasattr(self, "proxy"):
            print_value("## RHUA proxy:", self.proxy)
        if hasattr(self, "infra"):
            print_value("## RHUI infrastructure:", self.infra)
