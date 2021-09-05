import os
from pathlib import Path
from typing import Dict, Optional

import yaml


def parse_credentials(config_file_path: Optional[str] = None) -> Dict[str, Dict[str, str]]:
    if config_file_path:
        config_path = Path(config_file_path)

        if config_path.is_file():
            with open(config_path, 'r') as f:
                config_dict = yaml.load(f, Loader=yaml.FullLoader)
                return config_dict
        else:
            raise ValueError(f"File {config_path} does not exist!")
    else:
        return yaml.safe_load(os.environ.get("CCI_CREDENTIALS")) # type: ignore
