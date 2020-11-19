import os

from typing import Dict

ROOT_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
COIN_LIST_DIR = os.path.join(ROOT_DIR, 'lists')
COIN_LIST_FILENAME = 'coins_list.txt'
COIN_LIST_FILEPATH = os.path.join(COIN_LIST_DIR, COIN_LIST_FILENAME)

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(COIN_LIST_DIR, exist_ok=True)

LOG_FILEPATH = os.path.join(LOG_DIR, f'log_coin_returns.txt')

# initial investments
INITIAL_INV = os.path.join(ROOT_DIR, 'lists', 'initial_investments')
if os.path.exists(INITIAL_INV):
    with open(INITIAL_INV, 'r') as f:
        initial_dict: Dict[str, int] = {line.strip().split()[0]: float(line.strip().split()[1]) for line in f}
else:
    raise RuntimeError("Define initial investments file in lists. See readme in repo for more info.")
