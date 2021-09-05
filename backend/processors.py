from typing import Dict

from .interfaces import DataProcessor


class ReturnsProcessor(DataProcessor):
    NAME = "Returns"

    def process(self, local_data, remote_data):
        result_dict: Dict[str, float] = {}
        for key, value in local_data.items():
            result_dict[key] = round(((remote_data[key] - value) / value) * 100, 1)
        return result_dict
