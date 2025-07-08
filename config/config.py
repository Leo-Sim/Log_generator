import yaml
import os

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
        return self.config.get("log_type")