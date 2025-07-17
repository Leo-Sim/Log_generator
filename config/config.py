import yaml
import os


class ConfigInfo:

    MODE_BATCH = "batch"
    MODE_REALTIME = "realtime"

class Config:
    def __init__(self, config_path=None):

        if config_path is None:

            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, "config.yaml")

        self.config_path = config_path
        self.config = self._load_yaml()

        self.config_path = config_path
        self.config = self._load_yaml()

    def _load_yaml(self):
        with open(self.config_path, "r") as file:
            try:
                config = yaml.safe_load(file)
                return config
            except yaml.YAMLError as e:
                print(f"Error loading YAML file: {e}")
                return {}

    def get_log_type(self):
        return self.config.get("log-type")

    def get_transfer(self):
        return self.config.get("transfer")

    def get_transfer_interval(self):
        return self.get_transfer().get("interval")

    def get_transfer_count(self):
        return self.get_transfer().get("count")

    def get_transfer_target_servers(self):
        return self.get_transfer().get("target-servers")

    def get_transfer_mode(self):
        return self.get_transfer().get("mode")

    def get_transfer_max_log_per_sec(self):
        return self.get_transfer().get("max-log-per-sec")

    def get_include_syslog_header(self):
        return self.get_transfer().get("include-syslog-header")