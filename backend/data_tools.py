from pycoingecko import CoinGeckoAPI
from etherscan import Etherscan

from typing import List, Dict, Optional

import os

from config.common import COIN_LIST_FILEPATH
from config.initial import initial_dict, ETHSCAN_API_KEY

from utils.logger import logger
from utils.telegram import telegram_send, bot_pool
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


class DataHandler:

    def __init__(self, vs_currency: str = 'usd', remote_initial: bool = False) -> None:
        self.coin_ids: Optional[List[str]] = None
        self.vs_currency = vs_currency
        self.cg = CoinGeckoAPI()
        self.eth = Etherscan(ETHSCAN_API_KEY)
        self.prices: Dict[str, float]
        self.remote_initial = remote_initial
        self.the_initial_dict: Optional[Dict[str, float]] = None
        logger.info(f'--------------------- Class {self.__class__.__name__}'
                    f' initiated with parameters: coin_ids={self.coin_ids},'
                    f'vs_currency={self.vs_currency}, remote_initial={self.remote_initial}, the_initial_dict={self.the_initial_dict}')

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
        self._initialize_initial_dict()
        self._get_prices()
        msg = self._calculate_returns()
        telegram_send(self.add_gas_to_msg(msg))
        logger.info(f"Message:\n {msg}\n was sent!")


class CGroupHandler(DataHandler):
    def send_msg(self) -> None:
        msg = ""
        telegram_send(bot_pool.pool["cgroup_bot"], "cgroup_chat", self.add_gas_to_msg(msg))
