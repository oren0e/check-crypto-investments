from pycoingecko import CoinGeckoAPI

from typing import List, Dict, Optional

import os

from config.common import COIN_LIST_FILEPATH, initial_dict

from utils.logger import logger


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

    def __init__(self, coin_ids: List[str], vs_currency: str = 'usd') -> None:
        self.coin_ids = coin_ids
        self.vs_currency = vs_currency
        self.cg = CoinGeckoAPI()
        self.prices: Optional[Dict[str, float]] = None
        logger.info(f'--------------------- Class {self.__class__.__name__}'
                    f' initiated with parameters: coin_ids={self.coin_ids},'
                    f'vs_currency={self.vs_currency}')

    def _get_prices(self) -> None:
        """
        Calculates dict with coin names
        and their current prices
        """
        raw_prices: Dict[str, Dict[str, float]] = self.cg.get_price(ids=self.coin_ids, vs_currencies=self.vs_currency)
        self.prices: Dict[str, float] = {key: value[self.vs_currency] for key, value in raw_prices.items()}
        logger.info(f'Got prices {self.prices}')

    def calculate_returns(self) -> None:
        self._get_prices()
        result_dict: Dict[str, float] = {}
        for key, value in initial_dict.items():
            result_dict[key] = ((self.prices[key] - value) / value) * 100
            print(f'Return for {key}: {round(result_dict[key], 3)}%')
        logger.info(f'**************** Calculated Returns *********************\n'
                    f'{result_dict}')
