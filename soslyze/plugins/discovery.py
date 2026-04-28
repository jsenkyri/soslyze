import os.path
from pathlib import Path

from soslyze.utils import print_headline, print_value


class Discovery:
    def __init__(self, path):
        if os.path.isfile(path + "/sos_commands/podman/podman_ps_-a"):
            self.container_status = Path(
                path + "/sos_commands/podman/podman_ps_-a").read_text()
        if os.path.isfile(
                path + "/sos_commands/discovery/podman_logs_-t_discovery"):
            self.discovery_log = Path(
                path + "/sos_commands/discovery/podman_logs_-t_discovery")\
                .read_text()
        if os.path.isfile(
                path + "/sos_commands/discovery/podman_logs_-t_dsc-db"):
            self.dsc_db_log = Path(
                path + "/sos_commands/discovery/podman_logs_-t_dsc-db")\
                .read_text()
        if os.path.isfile(path + "/sos_commands/discovery/" +
                          "podman_logs_-t_discovery-toolbox"):
            self.toolbox_log = Path(
                path + "/sos_commands/discovery/" +
                "podman_logs_-t_discovery-toolbox").read_text()

    def output(self):
        print_headline("# DISCOVERY INFORMATION")
        if hasattr(self, "container_status"):
            print_value("## Container status:", self.container_status)
        if hasattr(self, "discovery_log"):
            print_value("## Log Discovery:", self.discovery_log)
        if hasattr(self, "toolbox_log"):
            print_value("## Log Toolbox:", self.toolbox_log)
        if hasattr(self, "dsc_db_log"):
            print_value("## Log dsc-db:", self.dsc_db_log)
