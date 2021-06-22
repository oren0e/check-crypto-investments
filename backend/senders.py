import requests

from backend.interfaces import DataSender


class TelegramSender(DataSender):
    def __init__(self, api_token: str, chat_id: str) -> None:
        self.api_token = api_token
        self.chat_id = chat_id

    def send_message(self, msg)  -> None:
        if self.api_token and self.chat_id:
            sent_msg = 'https://api.telegram.org/bot' + self.api_token + '/sendMessage?chat_id=' + self.chat_id + '&parse_mode=Markdown&text=' + msg
            requests.get(sent_msg)
        else:
            raise RuntimeError("Missing Telegram token or chat id")
