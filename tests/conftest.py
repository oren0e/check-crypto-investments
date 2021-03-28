import os
import pytest

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
