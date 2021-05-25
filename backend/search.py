from pycoingecko import CoinGeckoAPI

from typing import List, Dict, Optional

import os

from config.common import COIN_LIST_FILEPATH

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
