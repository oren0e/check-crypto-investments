from backend.data_tools import DataHandler, CoinSearch, initial_dict

from unittest import mock

import pytest

from typing import Dict


@pytest.fixture
def cs() -> CoinSearch:
    return CoinSearch()


@pytest.fixture
def dh() -> DataHandler:
    return DataHandler()


@mock.patch('backend.data_tools.initial_dict')
@mock.patch('backend.data_tools.telegram_send')
@mock.patch("backend.data_tools.CoinGeckoAPI.get_price")
def test_calculate_returns(mock_new_prices, tele_mock, initial_dict_mock, dh) -> None:
    mock_new_prices.return_value = {'coin_A': {'usd': 50}, 'coin_B': {'usd': 200}}
    d: Dict[str, float] = {'coin_A': 10, 'coin_B': 20}
    initial_dict_mock.__getitem__.side_effect = d.__getitem__
    initial_dict_mock.__iter__.side_effect = d.__iter__
    initial_dict_mock.items.side_effect = d.items
    dh.calculate_returns()
    tele_mock.assert_has_calls([mock.call('Return for coin_A: 400.0%'), mock.call('Return for coin_B: 900.0%')])
