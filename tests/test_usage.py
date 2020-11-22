from backend.data_tools import DataHandler, CoinSearch

from unittest import mock

import pytest


@pytest.fixture
def cs() -> CoinSearch:
    return CoinSearch()


@pytest.fixture
def dh() -> DataHandler:
    return DataHandler()


@mock.patch("backend.data_tools.DataHandler._get_prices")
def test_calculate_returns(mock_initial_dict: mock.Mock, dh) -> None:
    mock_initial_dict.return_value = {'coin_A': 100, 'coin_B': 400, 'coin_C': 10.12}
