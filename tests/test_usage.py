from unittest import mock

import pytest
from pycoingecko import CoinGeckoAPI

from backend.displayers import GasDisplayer, ReturnsDisplayer
from backend.processors import ReturnsProcessor


def test_gas_displayer() -> None:
    data = "190"
    assert GasDisplayer().generate(data) == f"*Gas:* {data} Gwei"


def test_returns_displayer() -> None:
    fake_returns = {"coin_a": 20.0, "coin_b": 40.0}
    assert ReturnsDisplayer().generate(fake_returns) == "Return for coin_a: 20.0%\nReturn for coin_b: 40.0%\n"


def test_returns_processor() -> None:
    local_data = {"coin_a": 100.0, "coin_b": 200.0}
    remote_data = {"coin_a": 200.0, "coin_b": 100.0}
    processor = ReturnsProcessor()
    result_dict = processor.process(local_data, remote_data)

    assert processor.NAME == "Returns"
    assert len(result_dict) == 2
    assert result_dict["coin_a"] == 100.0
    assert result_dict["coin_b"] == -50.0


@mock.patch("backend.senders.TelegramSender")
def test_telegram_sender(telegram_sender_mock) -> None:
    sender_mock = telegram_sender_mock(api_token="token", chat_id="123")
    sender_mock.send_message("This is a test")
    sender_mock.send_message.assert_called_with("This is a test")


@pytest.mark.integration
def test_api_response() -> None:
    cg = CoinGeckoAPI()
    ans = cg.ping()
    assert ans, "CoinGeckoAPI did not return a response!"
