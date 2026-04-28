import os.path
import re
from pathlib import Path

from soslyze.utils import print_headline, print_value, parse_text


class Insights:
    def __init__(self, path):
        lines = []
        if os.path.isfile(path + "/installed-rpms"):
            self.client = parse_text(
                path + "/installed-rpms", r"^insights-client.*")
        if os.path.isfile(path + "/etc/insights-client/insights-client.conf"):
            for line in Path(
                    path + "/etc/insights-client/insights-client.conf")\
                    .read_text().splitlines():
                if not re.search(r"^#.*", line) and line != "":
                    lines.append(line)
            self.config = "\n".join(lines)
            lines.clear()
        if os.path.isfile(path +
                          "/sos_commands/insights/" +
                          "insights-client_--test-connection_--net-debug"):
            self.network = Path(
                path + "/sos_commands/insights/" +
                "insights-client_--test-connection_--net-debug").read_text()

    def output(self):
        print_headline("# INSIGHTS")
        if hasattr(self, "client"):
            print_value("## Version of insights-client:", self.client)
        if hasattr(self, "config"):
            print_value("## Insights configuration" +
                        "(shows only non-default settings):", self.config)
        if hasattr(self, "network"):
            print_value("## Insights connectivity check:", self.network)
