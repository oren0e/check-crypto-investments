from utils import s3_settings

from unittest import mock

import pytest

import os

from backend.data_tools import CoinGeckoAPI
from utils.telegram import Bot, Chat, BotPool
from cci import main


def test_calculate_returns(initial_investments, price_handler, mock_returns, mock_new_prices) -> None:
    with mock.patch.object(price_handler, "prices", mock_new_prices):
        assert price_handler.calculate_returns(initial_investments) == mock_returns


@mock.patch("backend.data_tools.CoinGeckoAPI.get_price")
def test_get_prices(new_prices_mock, initial_investments, price_handler) -> None:
    new_prices_mock.return_value = {'coin_A': {'usd': 50}, 'coin_B': {'usd': 200}}
    assert price_handler.get_prices(initial_investments).prices == {'coin_A': 50, 'coin_B': 200}


def test_display_returns(data_displayer, mock_returns) -> None:
    assert data_displayer.display_returns(mock_returns) == 'Return for coin_A: 400.0%\nReturn for coin_B: 900.0%\n'


def test_default_get_initial_investments_from_source(data_reader) -> None:
    assert data_reader.get_initial_investments_from_source("abcdr") == {'bitcoin': 500, 'ethereum': 300}


@mock.patch("cci.DataReader.get_gas_estimate")
@mock.patch("cci.DataDisplayer.display_eth_gas")
@mock.patch('cci.telegram_send')
def test_telegram_send(telegram_send_mock, mock_gas, mock_gas_api, data_reader) -> None:
    bot_pool = BotPool()
    bot_pool.add_bot(Bot(name="cgroup_bot", api_token=os.environ.get("TELEGRAM_CGROUP_TOKEN"),
                         chats={"cgroup_chat": Chat("cgroup_chat", chat_id=os.environ.get("TELEGRAM_CGROUP_CHAT_ID"))}))
    mock_gas_api.return_value = ""
    mock_gas.return_value = "*Gas:* 118 Gwei\n"
    main("local", only_gas=True)
    telegram_send_mock.assert_called_with(bot_pool.pool["cgroup_bot"], "cgroup_chat", "*Gas:* 118 Gwei\n")


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
