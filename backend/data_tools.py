from pycoingecko import CoinGeckoAPI
from etherscan import Etherscan

from typing import List, Dict, Optional
import enum

import os

from config.common import COIN_LIST_FILEPATH, ROOT_DIR

from utils.logger import logger
from utils.telegram import telegram_send, Bot, Chat, BotPool
from utils import s3_settings


class CoinSearch:
    def __init__(self) -> None:
        self.cg = CoinGeckoAPI()
        logger.info(f'--------------------- Class {self.__class__.__name__} initalized')

    def _get_coins_list(self) -> None:
        """
        Gets the coin list supported by CoinGecko
        """
        coin_list: List[Dict] = self.cg.get_coins_list()
        with open(COIN_LIST_FILEPATH, 'w') as f:
            for d in coin_list:
                for key, value in d.items():
                    f.write(f'{key}:{value} ')
                f.write('\n')
        logger.info('get_coins_list() has been called')

    def search_for_coin(self, text: str, get_list: Optional[bool] = False) -> None:
        """
        Method to look for specific IDs or symbols of coins
        """
        if not get_list:
            if os.path.exists(COIN_LIST_FILEPATH):
                os.system(f"cat {COIN_LIST_FILEPATH} | grep {text}")
            else:
                self._get_coins_list()
                os.system(f"cat {COIN_LIST_FILEPATH} | grep {text}")
        else:
            self._get_coins_list()
            os.system(f"cat {COIN_LIST_FILEPATH} | grep {text}")


"""
Everytime you'll want to add a bot you'll have to couple it with a dedicated handler
"""


class DataSource(enum.Enum):
    LOCAL = enum.auto()
    REMOTE = enum.auto()


class PriceHandler:
    def __init__(self, initial_investments: Dict[str, float], vs_currency: str = 'usd') -> None:
        self.vs_currency = vs_currency
        self.cg = CoinGeckoAPI()
        self.coin_ids: Optional[List[str]] = None
        self.prices: Optional[Dict[str, float]] = None
        self.initial_investments: Dict[str, float] = initial_investments

    def get_prices(self) -> None:
        """
        Calculates dict with coin names
        and their current prices
        """
        self.coin_ids = list(self.initial_investments.keys())
        raw_prices: Dict[str, Dict[str, float]] = self.cg.get_price(ids=self.coin_ids, vs_currencies=self.vs_currency)
        self.prices = {key: value[self.vs_currency] for key, value in raw_prices.items()}
        logger.info(f'Got prices {self.prices}')

    def calculate_returns(self) -> Dict[str, float]:
        result_dict: Dict[str, float] = {}
        for key, value in self.initial_investments.items():
            result_dict[key] = round(((self.prices[key] - value) / value) * 100, 1)
        logger.info(f"Got dictionary of returns: {result_dict}")
        return result_dict


class DataReader:
    def __init__(self) -> None:
        self.eth = Etherscan(os.environ.get('ETHSCAN_API_KEY'))

    @staticmethod
    def get_initial_investments_from_source(filename: str, source: DataSource = DataSource.LOCAL) -> Dict[str, float]:
        if source == DataSource.LOCAL:
            initial_inv_list = os.path.join(ROOT_DIR, 'lists', filename)
            if os.path.exists(initial_inv_list):
                with open(initial_inv_list, 'r') as f:
                    initial_dict: Dict[str, float] = {line.strip().split()[0]: float(line.strip().split()[1]) for line in f
                                                      if not line.startswith("#")}
                logger.info("Initial investments read from file successfully")
                return initial_dict
            logger.warning("Initial_investments file was not found, using defaults instead.")
            return {'bitcoin': 500, 'ethereum': 300}
        elif source == DataSource.REMOTE:
            s3_resource = s3_settings.session.resource('s3')
            body = s3_resource.Object(s3_settings.S3_BUCKET, filename).get()['Body'].read().decode('utf-8')
            return {line.strip().split()[0]: float(line.strip().split()[1]) for line in
                                     body.split('\n') if not line.startswith("#")}
        logger.error("Unsupported data source")
        raise ValueError("Unsupported data source")

    def get_gas_estimate(self) -> str:
        return self.eth.get_gas_oracle()["ProposeGasPrice"]











class DataHandler0:

    def __init__(self, vs_currency: str = 'usd', remote_initial: bool = False) -> None:
        self.coin_ids: Optional[List[str]] = None
        self.vs_currency = vs_currency
        self.cg = CoinGeckoAPI()
        self.eth = Etherscan(ETHSCAN_API_KEY)
        self.prices: Dict[str, float]
        self.remote_initial = remote_initial
        self.the_initial_dict: Optional[Dict[str, float]] = None
        self.bot_pool = BotPool()
        self.API_TOKEN: Optional[str] = os.environ.get('TELEGRAM_API_TOKEN')
        self.CHAT_ID: Optional[str] = os.environ.get('TELEGRAM_CHAT_ID')
        logger.info(f'--------------------- Class {self.__class__.__name__}'
                    f' initiated with parameters: coin_ids={self.coin_ids},'
                    f'vs_currency={self.vs_currency}, remote_initial={self.remote_initial}, the_initial_dict={self.the_initial_dict}')

    def _initialize_bots(self) -> None:
        self.bot_pool.add_bot(
            Bot(name="cci_bot", api_token=self.API_TOKEN, chats={"cci_chat": Chat("cci_chat", chat_id=self.CHAT_ID)}))

    def _get_prices(self) -> None:
        """
        Calculates dict with coin names
        and their current prices
        """
        self.coin_ids = list(self.the_initial_dict.keys())
        raw_prices: Dict[str, Dict[str, float]] = self.cg.get_price(ids=self.coin_ids, vs_currencies=self.vs_currency)
        self.prices = {key: value[self.vs_currency] for key, value in raw_prices.items()}
        logger.info(f'Got prices {self.prices}')

    def _initialize_initial_dict(self) -> None:
        if self.remote_initial:
            s3_resource = s3_settings.session.resource('s3')
            body = s3_resource.Object(s3_settings.S3_BUCKET, "initial_investments").get()['Body'].read().decode('utf-8')
            self.the_initial_dict = {line.strip().split()[0]: float(line.strip().split()[1]) for line in body.split('\n') if not line.startswith("#")}
        else:
            self.the_initial_dict = initial_dict

    def _get_gas_estimate(self) -> str:
        return self.eth.get_gas_oracle()["ProposeGasPrice"]

    def _calculate_returns(self) -> str:
        result_dict: Dict[str, float] = {}
        msg: str = ""
        for key, value in self.the_initial_dict.items():
            result_dict[key] = round(((self.prices[key] - value) / value) * 100, 1)
            msg += f'Return for {key}: {round(result_dict[key], 3)}%\n'
        logger.info(f'**************** Calculated Returns *********************\n'
                    f'{result_dict}')
        return msg

    def add_gas_to_msg(self, msg: str) -> str:
        msg += f"*Gas:* {self._get_gas_estimate()} Gwei\n"
        return msg

    def send_msg(self) -> None:
        self._initialize_bots()
        self._initialize_initial_dict()
        self._get_prices()
        msg = self._calculate_returns()
        telegram_send(self.bot_pool.pool["cci_bot"], "cci_chat", self.add_gas_to_msg(msg))
        logger.info(f"Message:\n {msg}\n was sent!")


class CGroupHandler(DataHandler):
    def __init__(self) -> None:
        self.eth = Etherscan(ETHSCAN_API_KEY)
        self.API_TOKEN: Optional[str] = os.environ.get("TELEGRAM_CGROUP_TOKEN")
        self.CHAT_ID: Optional[str] = os.environ.get("TELEGRAM_CGROUP_CHAT_ID")
        self.bot_pool = BotPool()

    def _initialize_bots(self) -> None:
        self.bot_pool.add_bot(Bot(name="cgroup_bot", api_token=self.API_TOKEN,
                             chats={"cgroup_chat": Chat("cgroup_chat", chat_id=self.CHAT_ID)}))

    def send_msg(self) -> None:
        self._initialize_bots()
        msg = ""
        telegram_send(self.bot_pool.pool["cgroup_bot"], "cgroup_chat", self.add_gas_to_msg(msg))
