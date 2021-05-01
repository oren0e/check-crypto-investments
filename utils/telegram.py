import requests

from typing import Dict

from dataclasses import dataclass, field

from utils.logger import logger


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


@dataclass
class BotPool:
    pool: Dict[str, Bot] = field(default_factory=dict)

    def add_bot(self, bot: Bot) -> None:
        if not (bot.api_token and bot.chats):
            logger.error("Missing Telegram token or chat id")
            raise RuntimeError("Missing Telegram token or chat id")
        self.pool[bot.name] = bot


def telegram_send(bot: Bot, chat: str, message: str) -> None:
    if bot.api_token and chat in bot.chats:
        send_msg = 'https://api.telegram.org/bot' + bot.api_token + '/sendMessage?chat_id=' +\
                   bot.chats[chat].chat_id + '&parse_mode=Markdown&text=' + message
        requests.get(send_msg)
        logger.info(f"Message:\n {message}\n was sent!")
    else:
        logger.error("Missing Telegram token or chat id")
        raise RuntimeError("Missing Telegram token or chat id")
