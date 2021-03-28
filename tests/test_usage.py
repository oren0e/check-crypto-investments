from backend.data_tools import DataHandler, CoinSearch, CoinGeckoAPI, CGroupHandler
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

@pytest.fixture
def cgroup_handler() -> CGroupHandler:
    return CGroupHandler()


@mock.patch("backend.data_tools.bot_pool")
@mock.patch("backend.data_tools.DataHandler.add_gas_to_msg")
@mock.patch('backend.data_tools.initial_dict')
@mock.patch('backend.data_tools.telegram_send')
@mock.patch("backend.data_tools.CoinGeckoAPI.get_price")
def test_calculate_returns(mock_new_prices, tele_mock, initial_dict_mock, add_gas_to_msg, bot_pool_mock, dh) -> None:
    mock_new_prices.return_value = {'coin_A': {'usd': 50}, 'coin_B': {'usd': 200}}
    d: Dict[str, float] = {'coin_A': 10, 'coin_B': 20}
    initial_dict_mock.__getitem__.side_effect = d.__getitem__
    initial_dict_mock.__iter__.side_effect = d.__iter__
    initial_dict_mock.items.side_effect = d.items
    sent_msg = 'Return for coin_A: 400.0%\nReturn for coin_B: 900.0%\n' + f"*Gas:* 118 Gwei\n"
    add_gas_to_msg.return_value = sent_msg
    dh.send_msg()
    tele_mock.assert_called_with(bot_pool_mock.pool["cci_bot"], "cci_chat", sent_msg)


@mock.patch("backend.data_tools.bot_pool")
@mock.patch('backend.data_tools.telegram_send')
@mock.patch("backend.data_tools.DataHandler.add_gas_to_msg")
def test_cgroup_send_msg(add_gas_to_msg, tele_mock, bot_pool_mock, cgroup_handler) -> None:
    sent_msg = f"*Gas:* 118 Gwei\n"
    add_gas_to_msg.return_value = sent_msg
    cgroup_handler.send_msg()
    tele_mock.assert_called_with(bot_pool_mock.pool["cgroup_bot"], "cgroup_chat", sent_msg)


@pytest.mark.integration
def test_api_response() -> None:
    cg = CoinGeckoAPI()
    ans = cg.ping()
    assert ans, "CoinGeckoAPI did not return a response!"


@pytest.mark.integration
def test_s3() -> None:
    s3_resource = s3_settings.session.resource('s3')
    body = s3_resource.Object(s3_settings.S3_BUCKET, "initial_investments").get()['Body'].read().decode('utf-8')
    assert body
    assert len(body) > 0
