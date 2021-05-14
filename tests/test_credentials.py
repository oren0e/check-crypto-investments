import pytest

from config.credentials import parse_credentials


def test_correct_config_file() -> None:
    result_dict = parse_credentials('tests/data/correct_config.yml')
    assert len(result_dict) >= 2


def test_wrong_config_file() -> None:
    with pytest.raises(RuntimeError):
        parse_credentials('tests/data/wrong_config.yml')
