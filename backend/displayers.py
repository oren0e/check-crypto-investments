from backend.interfaces import DataDisplayer
from typing import Dict


class GasDisplayer(DataDisplayer):
    @staticmethod
    def generate(gas_price: str) -> str:
        return f"*Gas:* {gas_price} Gwei\n"


class ReturnsDisplayer(DataDisplayer):
    @staticmethod
    def generate(returns: Dict[str, float]) -> str:
        msg: str = ""
        for key, value in returns.items():
            msg += f"Return for {key}: {value}%\n"
        return msg

