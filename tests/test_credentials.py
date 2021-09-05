from config.credentials import parse_credentials


def test_correct_config_file() -> None:
    result_dict = parse_credentials("tests/data/correct_config.yml")
    assert len(result_dict) >= 2
