from app.robo_advisor import to_usd, dash_attack, compile_url, get_response, calculate_prices, write_to_csv
#import pytest


def test_to_usd():
    assert to_usd(2.5) == "$2.50"

    assert to_usd(2.50) == "$2.50"

    assert to_usd(2.555556) == "$2.56"

    assert to_usd(1234567890.678) == "$1,234,567,890.68"

    assert to_usd(2.555556) == "$2.56"
    assert to_usd(2.555556) == "$2.56"


