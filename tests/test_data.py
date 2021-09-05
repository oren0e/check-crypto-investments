import pytest


def test_correct_initial_investment_parsing() -> None:
    with open("tests/data/fake_initial_investments") as f:
        initial_investments = f.read()
    initial_dict = {
        line.strip().split()[0]: float(line.strip().split()[1])
        for line in initial_investments.split("\n")
        if not line.startswith("#")
    }
    assert len(initial_dict) == 2
    assert initial_dict["asset_a"] == 100.0
    assert initial_dict["asset_c"] == 300.0
    with pytest.raises(KeyError):
        cant_exist = initial_dict["asset_b"]  # pylint: disable=unused-variable
