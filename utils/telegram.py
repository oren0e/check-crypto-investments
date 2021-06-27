from dataclasses import dataclass, field
from typing import Dict, Optional

import requests

from utils.logger import logger


@dataclass
class Chat:
    name: Optional[str]
    chat_id: Optional[str]


@dataclass
class Bot:
    name: Optional[str]
    api_token: Optional[str]
    chats: Dict[Optional[str], Chat] = field(default_factory=dict)

    def add_chat(self, chat: Chat) -> None:
        self.chats[chat.name] = chat

    def __hash__(self) -> int:
        return hash((self.name, self.api_token))


@dataclass
class BotPool:
    pool: Dict[Optional[str], Bot] = field(default_factory=dict)

    def add_bot(self, bot: Bot) -> None:
        if not (bot.api_token and bot.chats):
            logger.error("Missing Telegram token or chat id")
            raise RuntimeError("Missing Telegram token or chat id")
        self.pool[bot.name] = bot


def telegram_send(bot: Bot, chat: str, message: str) -> None:
    if bot.api_token and chat in bot.chats:
        send_msg = "".join([
            'https://api.telegram.org/bot',
            bot.api_token,
            '/sendMessage?chat_id=',
            bot.chats[chat].chat_id, # type: ignore
            '&parse_mode=Markdown&text=',
            message
            ])

        requests.get(send_msg)
        logger.info(f"Message:\n {message}\n was sent!")
    else:
        logger.error("Missing Telegram token or chat id")
        raise RuntimeError("Missing Telegram token or chat id")
