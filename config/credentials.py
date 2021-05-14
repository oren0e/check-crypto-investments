import yaml
import os

from pathlib import Path
from typing import Dict


def parse_credentials(config_file_path: str = "config.yml") -> Dict[str, Dict[str, str]]:
    config_path = Path(config_file_path)

    if config_path.is_file():
        with open(config_path, 'r') as f:
            config_dict = yaml.load(f, Loader=yaml.FullLoader)
    else:
        config_dict = yaml.safe_load(os.environ.get("CCI_CREDENTIALS"))

    if all(key in config_dict for key in ["aws", "ethscan"]):
        return config_dict
    raise RuntimeError("Some essential keys are missing from config")
