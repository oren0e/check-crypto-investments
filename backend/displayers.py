from typing import Dict

from backend.interfaces import DataDisplayer


class GasDisplayer(DataDisplayer):
    @staticmethod
    def generate(data: str) -> str:
        return f"*Gas:* {data} Gwei"


class ReturnsDisplayer(DataDisplayer):
    @staticmethod
    def generate(data: Dict[str, float]) -> str:
        msg: str = ""
        for key, value in data.items():
            msg += f"Return for {key}: {value}%\n"
        return msg
