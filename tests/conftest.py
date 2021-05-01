import os
import pytest

from typing import Dict

from backend.data_tools import CoinSearch, PriceHandler, DataReader, DataDisplayer


try:
    from .temp_env_vars import TEMP_ENV_VARS, ENV_VARS_TO_SUSPEND
except ImportError:
    TEMP_ENV_VARS = {}
    ENV_VARS_TO_SUSPEND = []


@pytest.fixture
def fake_credentials() -> None:
    # Execute before the first test
    old_environ = dict(os.environ)
    os.environ.update(TEMP_ENV_VARS)
    for env_var in ENV_VARS_TO_SUSPEND:
        os.environ.pop(env_var, default=None)

    yield
    # Execute after the last test
    os.environ.clear()
    os.environ.update(old_environ)


@pytest.fixture
def cs() -> CoinSearch:
    return CoinSearch()


@pytest.fixture
def data_reader() -> DataReader:
    return DataReader()


@pytest.fixture
def data_displayer() -> DataDisplayer:
    return DataDisplayer()


@pytest.fixture
def price_handler() -> PriceHandler:
    return PriceHandler()


@pytest.fixture
def initial_investments() -> Dict[str, float]:
    return {'coin_A': 10, 'coin_B': 20}


@pytest.fixture
def mock_new_prices() -> Dict[str, float]:
    return {'coin_A': 50, 'coin_B': 200}


@pytest.fixture
def mock_returns() -> Dict[str, float]:
    return {'coin_A': 400.0, 'coin_B': 900.0}
