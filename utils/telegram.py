import os

import requests

API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')


def telegram_send(message: str) -> None:
    send_msg = 'https://api.telegram.org/bot' + API_TOKEN + '/sendMessage?chat_id=' + CHAT_ID + '&parse_mode=Markdown&text=' + message
    requests.get(send_msg)
