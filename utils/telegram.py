import os

import requests

from typing import Optional, Set, Dict

from dataclasses import dataclass, field

API_TOKEN: Optional[str] = os.environ.get('TELEGRAM_API_TOKEN')
CHAT_ID: Optional[str] = os.environ.get('TELEGRAM_CHAT_ID')


@dataclass
class Chat:
    name: str
    chat_id: str


@dataclass
class Bot:
    name: str
    api_token: str
    chats: Dict[str, Chat] = field(default_factory=dict)

    def add_chat(self, chat: Chat) -> None:
        self.chats[chat.name] = chat

    def __hash__(self) -> int:
        return hash((self.name, self.api_token))


if API_TOKEN and CHAT_ID:
    bot_pool: Set[Bot] = set(Bot(name="cci_bot", api_token=API_TOKEN, chats={"cci_chat": Chat("cci_chat", chat_id=CHAT_ID)}))


def telegram_send(bot: Bot, chat: str, message: str) -> None:
    if bot.api_token and chat in bot.chats:
        send_msg = 'https://api.telegram.org/bot' + bot.api_token + '/sendMessage?chat_id=' +\
                   bot.chats[chat].chat_id + '&parse_mode=Markdown&text=' + message
        requests.get(send_msg)
    else:
        raise RuntimeError("Missing Telegram token or chat id")
