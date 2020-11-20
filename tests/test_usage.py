from backend.data_tools import DataHandler, CoinSearch

import pytest


@pytest.fixture
def cs() -> CoinSearch:
    return CoinSearch()


@pytest.fixture
def dh() -> DataHandler:
    return DataHandler()


# TODO: write test on each part of the flow