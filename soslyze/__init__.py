import argparse
import os
from pathlib import Path
import re
from soslyze.plugins.discovery import Discovery
from soslyze.plugins.insights import Insights
from soslyze.plugins.os import Rhel7
from soslyze.plugins.os import Rhel8
from soslyze.plugins.os import UnknownOS
from soslyze.plugins.package_manager import Dnf
from soslyze.plugins.package_manager import Yum
from soslyze.plugins.rhui import Rhui
from soslyze.plugins.satellite import Satellite
from soslyze.plugins.subscription_manager import SubscriptionManager
from soslyze.utils import package_present, Style


class SoSLyze:

    def valid_path(self, path):
        print(f"{Style.YELLOW_BOLD}Using path: {path}{Style.RESET}")
        if os.path.exists(f"{path}/sos_reports"):
            return path
        else:
            raise argparse.ArgumentTypeError(
                f"'{path}' is not a valid sosreport path.\n"
            )

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Summarize data from an extracted sosreport archive, "
                        + "focusing on Red Hat Satellite, Subscription Management, "
                        + "and Red Hat Insights (Lightspeed)."
            )
        self.parser.add_argument(
            'path',
            help='Path to sosreport. Default: `./`.',
            default=os.getcwd(),
            type=self.valid_path,
            nargs='?'
            )
        self.parser.add_argument(
            '--output-file', '-o',
            help='Save output to file (markdown format, no ANSI colors)',
            type=str,
            default=None
            )
        self.args = self.parser.parse_args()

        # Disable ANSI colors BEFORE instantiating plugins if saving to file
        if self.args.output_file:
            from soslyze.utils import disable_ansi_colors
            disable_ansi_colors()

        if len(re.findall('8[.]', Path(
            f"{self.args.path}/etc/redhat-release")
            .read_text(encoding="utf-8"))) == 1 or len(
                re.findall('9[.]', Path(
                    f"{self.args.path}/etc/redhat-release")
                    .read_text(encoding="utf-8"))) == 1:
            self.os = Rhel8(self.args.path)
        elif len(re.findall('6[.]', Path(
            f"{self.args.path}/etc/redhat-release")
            .read_text(encoding="utf-8"))) == 1 or len(
                re.findall('7[.]', Path(
                    f"{self.args.path}/etc/redhat-release")
                    .read_text(encoding="utf-8"))) == 1:
            self.os = Rhel7(self.args.path)
        else:
            self.os = UnknownOS(self.args.path)

        try:
            if package_present(self.args.path, "dnf"):
                self.package_manager = Dnf(self.args.path)
            elif package_present(self.args.path, "yum"):
                self.package_manager = Yum(self.args.path)
            if package_present(self.args.path, "subscription-manager"):
                self.subscription_manager = SubscriptionManager(self.args.path)
            if package_present(self.args.path, "insights-client"):
                self.insights = Insights(self.args.path)
            if package_present(self.args.path, "satellite"):
                self.satellite = Satellite(self.args.path)
            if os.path.isfile(self.args.path + "/etc/rhui/rhui-tools.conf"):
                self.rhui = Rhui(self.args.path)
            if os.path.isdir(self.args.path + "/sos_commands/discovery"):
                self.discovery = Discovery(self.args.path)
        except Exception as e:
            print(f"ERROR package_manager: {e}")

    def output(self):
        if self.args.output_file:
            from soslyze.utils import enable_ansi_colors
            import sys
            import io

            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()

        self.os.output()

        if hasattr(self, "subscription_manager"):
            self.subscription_manager.output()

        if hasattr(self, "package_manager"):
            self.package_manager.output()

        if hasattr(self, "insights"):
            self.insights.output()

        if hasattr(self, "satellite"):
            self.satellite.output()

        if hasattr(self, "rhui"):
            self.rhui.output()

        if hasattr(self, "discovery"):
            self.discovery.output()

        if self.args.output_file:
            sys.stdout = old_stdout
            with open(self.args.output_file, 'w') as f:
                f.write(buffer.getvalue())
            enable_ansi_colors()
            print(f"{Style.YELLOW_BOLD}Output saved to: {self.args.output_file}{Style.RESET}")


#SoSLyze().output()
