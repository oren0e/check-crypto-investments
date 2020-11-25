from backend.data_tools import DataHandler, CoinSearch

from unittest import mock

import pytest


@pytest.fixture
def cs() -> CoinSearch:
    return CoinSearch()


@pytest.fixture
def dh() -> DataHandler:
    return DataHandler()


@mock.patch.dict('backend.data_tools.initial_dict', {'coin_A': 10, 'coin_B': 20})
@mock.patch("backend.data_tools.DataHandler.CoinGeckoAPI.get_price")
def test_calculate_returns(mock_new_prices, initial_dict, dh) -> None:
    mock_new_prices.return_value = {'coin_A': {'usd': 50}, 'coin_B': {'usd': 200}}
    with mock.patch('backend.data_tools.telegram_send') as tele_mock:
        dh.calculate_returns()
        tele_mock.assert_has_calls([mock.call('Return for coin_A: 400.0%'), mock.call('Return for coin_A: 900.0%')])
