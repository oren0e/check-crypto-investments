import os

ROOT_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
COIN_LIST_DIR = os.path.join(ROOT_DIR, 'lists')
COIN_LIST_FILENAME = 'coins_list.txt'
COIN_LIST_FILEPATH = os.path.join(COIN_LIST_DIR, COIN_LIST_FILENAME)

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(COIN_LIST_DIR, exist_ok=True)

LOG_FILEPATH = os.path.join(LOG_DIR, f'log_coin_returns.txt')
