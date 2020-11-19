import os
import datetime

ROOT_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

CURRENT_DATE = datetime.datetime.now().strftime('%Y-%m-%d')

LOG_FILEPATH = os.path.join(LOG_DIR, f'log_{CURRENT_DATE}.txt')
