from pycoingecko import CoinGeckoAPI
from etherscan import Etherscan

from typing import List, Dict, Optional

import os

from config.common import ROOT_DIR

from utils.logger import logger
from utils import s3_settings

from interfaces import DataReaderInterface, DataDisplayerInterface, DataProcessorInterface, DataSenderInterface





























class PriceHandler:
    def __init__(self, vs_currency: str = 'usd') -> None:
        self.vs_currency = vs_currency
        self.cg = CoinGeckoAPI()
        self.coin_ids: Optional[List[str]] = None
        self.prices: Optional[Dict[str, float]] = None

    def get_prices(self, initial_investments: Dict[str, float]) -> "PriceHandler":
        """
        Calculates dict with coin names
        and their current prices
        """
        self.coin_ids = list(initial_investments.keys())
        raw_prices: Dict[str, Dict[str, float]] = self.cg.get_price(ids=self.coin_ids, vs_currencies=self.vs_currency)
        self.prices = {key: value[self.vs_currency] for key, value in raw_prices.items()}
        logger.info(f'Got prices {self.prices}')
        return self

    def calculate_returns(self, initial_investments: Dict[str, float]) -> Dict[str, float]:
        result_dict: Dict[str, float] = {}
        for key, value in initial_investments.items():
            result_dict[key] = round(((self.prices[key] - value) / value) * 100, 1)
        logger.info(f"Got dictionary of returns: {result_dict}")
        return result_dict


class DataReader:
    def __init__(self) -> None:
        self.eth = Etherscan(os.environ.get('ETHSCAN_API_KEY'))

    @staticmethod
    def get_initial_investments_from_source(filename: str, source: str = "local") -> Dict[str, float]:
        if source == "local":
            initial_inv_list = os.path.join(ROOT_DIR, 'lists', filename)
            if os.path.exists(initial_inv_list):
                with open(initial_inv_list, 'r') as f:
                    initial_dict: Dict[str, float] = {line.strip().split()[0]: float(line.strip().split()[1]) for line in f
                                                      if not line.startswith("#")}
                logger.info("Initial investments read from file successfully")
                return initial_dict
            logger.warning("Initial_investments file was not found, using defaults instead.")
            return {'bitcoin': 500, 'ethereum': 300}
        elif source == "remote":
            print("Getting base prices from S3...")
            s3_resource = s3_settings.session.resource('s3')
            body = s3_resource.Object(s3_settings.S3_BUCKET, filename).get()['Body'].read().decode('utf-8')
            return {line.strip().split()[0]: float(line.strip().split()[1]) for line in
                                     body.split('\n') if not line.startswith("#")}
        logger.error("Unsupported data source")
        raise ValueError("Unsupported data source")

    def get_gas_estimate(self) -> str:
        return self.eth.get_gas_oracle()["ProposeGasPrice"]


class DataDisplayer:
    @staticmethod
    def display_returns(returns: Dict[str, float]) -> str:
        msg: str = ""
        for key, value in returns.items():
            msg += f'Return for {key}: {value}%\n'
        return msg

    @staticmethod
    def display_eth_gas(gas_price: str) -> str:
        return f"*Gas:* {gas_price} Gwei\n"
