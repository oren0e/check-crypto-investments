from backend.data_tools import DataHandler, CoinSearch, CoinGeckoAPI
from utils import s3_settings

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
    dh.send_msg()
    tele_mock.assert_called_with('Return for coin_A: 400.0%\nReturn for coin_B: 900.0%\n')


@pytest.mark.integration
def test_api_response() -> None:
    cg = CoinGeckoAPI()
    ans = cg.ping()
    assert ans, "CoinGeckoAPI did not return a response!"


def test_s3() -> None:
    s3_resource = s3_settings.session.resource('s3')
    body = s3_resource.Object(s3_settings.S3_BUCKET, "initial_investments").get()['Body'].read().decode('utf-8')
    assert body
    assert len(body) > 0
