import os

import requests

from typing import Optional

API_TOKEN: Optional[str] = os.environ.get('TELEGRAM_API_TOKEN')
CHAT_ID: Optional[str] = os.environ.get('TELEGRAM_CHAT_ID')


def telegram_send(message: str) -> None:
    if API_TOKEN and CHAT_ID:
        send_msg = 'https://api.telegram.org/bot' + API_TOKEN + '/sendMessage?chat_id=' + CHAT_ID + '&parse_mode=Markdown&text=' + message
        requests.get(send_msg)
    else:
        raise RuntimeError("Missing Telegram token or chat id")
