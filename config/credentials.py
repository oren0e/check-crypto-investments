import yaml
import os

from pathlib import Path
from typing import Dict, Optional


def parse_credentials(config_file_path: Optional[str] = None) -> Dict[str, Dict[str, str]]:
    if config_file_path:
        config_path = Path(config_file_path)

        if config_path.is_file():
            with open(config_path, 'r') as f:
                config_dict = yaml.load(f, Loader=yaml.FullLoader)
        else:
            raise ValueError(f"File {config_path} does not exist!")
    else:
        config_dict = yaml.safe_load(os.environ.get("CCI_CREDENTIALS"))
    if all(key in config_dict for key in ["aws", "ethscan"]):
        return config_dict
    raise RuntimeError("Some essential keys are missing from config")
