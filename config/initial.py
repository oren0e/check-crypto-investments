import os

from typing import Dict

from utils.logger import logger

from config.common import ROOT_DIR

# initial investments
INITIAL_INV = os.path.join(ROOT_DIR, 'lists', 'initial_investments')
if os.path.exists(INITIAL_INV):
    with open(INITIAL_INV, 'r') as f:
        initial_dict: Dict[str, float] = {line.strip().split()[0]: float(line.strip().split()[1]) for line in f}
else:
    initial_dict: Dict[str, float] = {'bitcoin': 500, 'ethereum': 300}
    logger.warning("!!! Warning: initial_investments file was not found, using defaults instead.")
