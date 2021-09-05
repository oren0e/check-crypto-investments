import os
from typing import Dict

from etherscan import Etherscan
from pycoingecko import CoinGeckoAPI

from backend.interfaces import DataReader
from config.credentials import parse_credentials


class InvestmentReader(DataReader):
    def get_data(self):
        initial_investments = os.environ.get("INITIAL_INVESTMENTS")
        initial_dict = {
            line.strip().split()[0]: float(line.strip().split()[1])
            for line in initial_investments.split("\n")
            if not line.startswith("#")
        }
        return initial_dict


class PricesReader(DataReader):
    def __init__(self, vs_currency: str) -> None:
        self.vs_currency = vs_currency

    def get_data(self):
        coingecko = CoinGeckoAPI()
        initial_investments = os.environ.get("INITIAL_INVESTMENTS")
        coin_ids = [line.strip().split()[0] for line in initial_investments.split("\n") if not line.startswith("#")]
        raw_prices: Dict[str, Dict[str, float]] = coingecko.get_price(ids=coin_ids, vs_currencies=self.vs_currency)
        return {key: value[self.vs_currency] for key, value in raw_prices.items()}


class GasReader(DataReader):
    def get_data(self) -> str:
        credentials = parse_credentials()
        eth = Etherscan(credentials["ethscan"]["api_key"])
        return eth.get_gas_oracle()["ProposeGasPrice"]
