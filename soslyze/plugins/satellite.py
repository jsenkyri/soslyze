import os.path
from pathlib import Path

from soslyze.utils import parse_text, parse_text_exclude,\
    print_headline, print_value


class Satellite:
    def __init__(self, path):
        if os.path.isfile(path + "/installed-rpms"):
            self.release = parse_text(path + "/installed-rpms",
                                      r"satellite-6.*|capsule-6.*")
        if os.path.isfile(path + "/sos_commands/foreman/hammer_ping"):
            self.health = Path(
                path + "/sos_commands/foreman/hammer_ping").read_text()
        if os.path.isfile(
                path + "/etc/foreman-installer/scenarios.d/" +
                "satellite-answers.yaml"):
            self.certs = parse_text(
                path + "/etc/foreman-installer/scenarios.d/" +
                "satellite-answers.yaml",
                r".*(server_key|server_cert_req|server_ca_cert|server_cert).*")
        if os.path.isfile(path + "/etc/foreman-installer/custom-hiera.yaml"):
            self.hiera = parse_text_exclude(
                path + "/etc/foreman-installer/custom-hiera.yaml", r"^#.*")
        if os.path.isfile(path + "/sos_commands/foreman/smart_proxies"):
            self.capsules = Path(path + "/sos_commands/foreman/smart_proxies")\
                .read_text()
        if os.path.isfile(
                path + "/etc/foreman-installer/scenarios.d/satellite.yaml"):
            self.tuning_profile = parse_text(
                path + "/etc/foreman-installer/scenarios.d/satellite.yaml",
                r".*tuning.*")
        if os.path.isfile(
                path + "/etc/systemd/system/foreman.service.d/installer.conf"):
            self.puma_workers = parse_text(
                path + "/etc/systemd/system/foreman.service.d/installer.conf",
                r".*(PUMA_THREADS|PUMA_WORKERS).*")
        if os.path.isfile(path + "/sos_commands/foreman/foreman-puma-status"):
            self.puma_stats = Path(
                path + "/sos_commands/foreman/foreman-puma-status").read_text()
        if os.path.isfile(path + "/etc/foreman/database.yml"):
            self.puma_pool = parse_text(path + "/etc/foreman/database.yml",
                                        r".*pool.*")
        if os.path.isfile(path + "/sos_commands/foreman/dynflow_units"):
            self.dynflow = Path(
                path + "/sos_commands/foreman/dynflow_units").read_text()
        if os.path.isfile(path + "/etc/httpd/conf.modules.d/event.conf"):
            self.httpd = Path(
                path + "/etc/httpd/conf.modules.d/event.conf").read_text()
        if os.path.isfile(path + "/etc/sysconfig/puppetserver"):
            self.puppet = parse_text(path + "/etc/sysconfig/puppetserver",
                                     r"^JAVA_ARGS=.*")
        if os.path.isfile(path + "/var/lib/pgsql/data/postgresql.conf"):
            self.pgsql = parse_text(
                path + "/var/lib/pgsql/data/postgresql.conf",
                r".*(max_connections|shared_buffers|work_mem" +
                "|autovacuum_vacuum_cost_limit).*")
#        if os.path.isfile(path + "/sos_commands/foreman/foreman_tasks_tasks"):
#            self.tasks_running = Path(
#                path + "/sos_commands/foreman/foreman_tasks_tasks")\
#                .read_text().splitlines()[0]
#            self.tasks_running = self.tasks_running + "\n" + parse_text(
#                path + "/sos_commands/foreman/foreman_tasks_tasks",
#                r".*running.*")

        if os.path.isfile(path + "/sos_commands/foreman/foreman_tasks_tasks"):
            self.tasks_running = Path(
                path + "/sos_commands/foreman/foreman_tasks_tasks")\
                .read_text().splitlines()[0]
            running_tasks = parse_text(
                path + "/sos_commands/foreman/foreman_tasks_tasks",
                r".*running.*")
            # Exclude "Check for long running tasks" entries
            filtered_tasks = "\n".join([line for line in running_tasks.split("\n")
                                       if "CheckLongRunningTasks" not in line])
            self.tasks_running = self.tasks_running + "\n" + filtered_tasks

            self.tasks_paused = Path(
                path + "/sos_commands/foreman/foreman_tasks_tasks")\
                .read_text().splitlines()[0]
            self.tasks_paused = self.tasks_paused + "\n" + parse_text(
                path + "/sos_commands/foreman/foreman_tasks_tasks",
                r".*paused.*")
        if os.path.isfile(
                path + "/sos_commands/foreman/foreman_settings_table"):
            self.settings = Path(
                path + "/sos_commands/foreman/foreman_settings_table"
            ).read_text().splitlines()[0]
            self.settings = self.settings + "\n" + parse_text(
                path + "/sos_commands/foreman/foreman_settings_table",
                r".*(http_proxy|allow_auto_inventory_upload" +
                "|destroy_vm_on_host_delete" +
                "|foreman_tasks_proxy_batch_trigger|" + ""
                "foreman_tasks_proxy_batch_size|remote_execution_ssh_user" +
                "|remote_execution_effective_user" +
                "|foreman_ansible_proxy_batch_size" +
                "|content_default_http_proxy|subscription_connection_enabled" +
                "|default_download_policy|default_redhat_download_policy).*")
        if os.path.isfile(path + "/etc/foreman-proxy/ansible.env"):
            self.ansible = parse_text(
                path + "/etc/foreman-proxy/ansible.env",
                r".*(ANSIBLE_ROLES_PATH" +
                "|ANSIBLE_COLLECTIONS_PATHS|ANSIBLE_SSH_ARGS).*")
        if os.path.isfile(
                path + "/sos_commands/candlepin/simple_content_access"):
            self.sca = Path(
                path + "/sos_commands/candlepin/simple_content_access")\
                .read_text()
        if os.path.isfile(
                path + "/sos_commands/candlepin/du_-sh_.var.lib.candlepin"):
            self.fs_cp = Path(
                path + "/sos_commands/candlepin/du_-sh_.var.lib.candlepin")\
                .read_text()
        if os.path.isfile(
                path + "/sos_commands/postgresql/du_-sh_.var.lib.pgsql"):
            self.fs_pgsql = Path(
                path + "/sos_commands/postgresql/du_-sh_.var.lib.pgsql")\
                .read_text()
        if os.path.isfile(
                path + "/sos_commands/foreman/foreman_db_tables_sizes"):
            self.db_foreman = "\n".join(Path(
                path + "/sos_commands/foreman/foreman_db_tables_sizes")
                                        .read_text().splitlines()[0:12])
        if os.path.isfile(
                path + "/sos_commands/candlepin/candlepin_db_tables_sizes"):
            self.db_candlepin = "\n".join(Path(
                path + "/sos_commands/candlepin/candlepin_db_tables_sizes")
                                          .read_text().splitlines()[0:12])
        if os.path.isfile(
                path + "/sos_commands/foreman/fact_names_prefixes"):
            self.db_facts = "\n".join(Path(
                path + "/sos_commands/foreman/fact_names_prefixes")
                                      .read_text().splitlines()[0:10])
        if os.path.isfile(
                path + "/var/lib/foreman-maintain/satellite_metrics.yml"):
            self.metrics_header = Path(
                path + "/var/lib/foreman-maintain/satellite_metrics.yml"
            ).read_text().splitlines()[1]
            self.metrics = parse_text(
                path + "/var/lib/foreman-maintain/satellite_metrics.yml",
                r".*(hosts_by_managed_count|total_users_count" +
                "|custom_roles_count|modified_settings|hosts_by_os_count" +
                "|ldap_auth_source_free_ipa_count|ldap_auth_source_posix_count" +
                "|ldap_auth_source_active_directory_count|smart_proxies_count" +
                "|total_users_count|non_admin_users_count|taxonomies_counts).*")
        if os.path.isdir(path + "/var/log/foreman-installer/"):
            self.installer = []
            for f in os.listdir(path + "/var/log/foreman-installer/"):
                if f.endswith(".log"):
                    for line in Path(
                        path + f"/var/log/foreman-installer/{f}"
                    ).read_text().splitlines():
                        if "Running installer with args" in line:
                            l = line.translate({ord(i): None for i in '[]",'}).split(" ")
                            if len(l) > 10:
                                self.installer.append(
                                    f"{l[0]}T{l[1]} foreman-installer {" ".join(l[9:])}")
        self.installer.sort(reverse=True)
        if os.path.isdir(path + "/var/log/foreman-maintain/"):
            self.maintain = []
            for f in os.listdir(path + "/var/log/foreman-maintain/"):
                if not f.endswith(".gz"):
                    for line in Path(
                        path + f"/var/log/foreman-maintain/{f}"
                    ).read_text().splitlines():
                        if "Running foreman-maintain" in line:
                            l = line.translate({ord(i): None for i in '[]",'}).split(" ")
                            if l[13] in ["service", "upgrade", "update"]:
                                self.maintain.append(
                                    f"{l[1]}T{l[2]} foreman-maintain {" ".join(l[13:])}")
            self.maintain.sort(reverse=True)


    def output(self):
        print_headline("### SATELLITE INFORMATION ###")
        if hasattr(self, "release"):
            print_value("Satellite version:", self.release)
        if hasattr(self, "health"):
            print_value("Hammer ping:", self.health)
        if hasattr(self, "certs"):
            print_value("Custom or default certificates:", self.certs)
        if hasattr(self, "hiera"):
            print_value("Custom hiera:", self.hiera)
        if hasattr(self, "capsules"):
            print_value("Capsule overview:", self.capsules)
        if hasattr(self, "sca"):
            print_value("Organizations & SCA:", self.sca)
        if hasattr(self, "tasks_running"):
            print_value("Running tasks:", self.tasks_running)
        if hasattr(self, "tasks_paused"):
            print_value("Paused tasks:", self.tasks_paused)
        if hasattr(self, "settings"):
            print_value("Satellite settings(nil=default:)", self.settings)
        if hasattr(self, "ansible"):
            print_value("Ansible integration:", self.ansible)
        if hasattr(self, "tuning_profile"):
            print_value("Tuning profile:", self.tuning_profile)
        if hasattr(self, "puma_stats"):
            print_value("Puma status:", self.puma_stats)
        if hasattr(self, "puma_workers"):
            print_value("Puma workers & threads:", self.puma_workers)
        if hasattr(self, "puma_pool"):
            print_value("Puma DB pool:", self.puma_pool)
        if hasattr(self, "dynflow"):
            print_value("Dynflow sidekiq status:", self.dynflow)
        if hasattr(self, "httpd"):
            print_value("Httpd tuning:", self.httpd)
        if hasattr(self, "puppet"):
            print_value("Puppet tuning:", self.puppet)
        if hasattr(self, "pgsql"):
            print_value("Postgresql tuning:", self.pgsql)
        if hasattr(self, "fs_cp"):
            print_value("/var/lib/candlepin usage:", self.fs_cp)
        if hasattr(self, "fs_pgsql"):
            print_value("/var/lib/pgsql usage:", self.fs_pgsql)
        if hasattr(self, "db_foreman"):
            print_value("Foreman db table sizes:", self.db_foreman)
        if hasattr(self, "db_candlepin"):
            print_value("Candlepin db table sizes:", self.db_candlepin)
        if hasattr(self, "db_facts"):
            print_value("Fact names:", self.db_facts)
        if hasattr(self, "metrics"):
            print_value("Usage Metrics:", self.metrics)
        if hasattr(self, "installer"):
            print_value("Installer:", "\n".join(self.installer[0:5])) 
        if hasattr(self, "maintain"):
            print_value("Maintain:", "\n".join(self.maintain[0:5])) 
