from app.robo_advisor import to_usd, dash_attack, compile_url, get_response, calculate_prices, write_to_csv
#import pytest
import os
import csv


def test_to_usd():
    assert to_usd(2.5) == "$2.50"

    assert to_usd(2.50) == "$2.50"

    assert to_usd(2.555556) == "$2.56"

    assert to_usd(1234567890.678) == "$1,234,567,890.68"

    assert to_usd(2.555556) == "$2.56"


def test_dash_attack():
    result = dash_attack()
    assert result == "-------------------------"

def test_compile_url():
    
    assert (compile_url("MSFT")) == 200

def test_get_response():
    symbol = "MSFT"
    parsed_response = get_response(symbol)

    assert isinstance(parsed_response, dict)
    assert "Meta Data" in parsed_response.keys()
    assert "Time Series (Daily)" in parsed_response.keys()
    assert parsed_response["Meta Data"]["2. Symbol"] == symbol

def test_calculate_prices():
     
    parsed_response = {
        "Meta Data": {
            "1. Information": "Daily Prices (open, high, low, close) and Volumes",
            "2. Symbol": "MSFT",
            "3. Last Refreshed": "2018-06-08",
            "4. Output Size": "Full size",
            "5. Time Zone": "US/Eastern"
        },
        "Time Series (Daily)": {
            "2019-06-08": {
                "1. open": "101.0924",
                "2. high": "101.9500",
                "3. low": "100.5400",
                "4. close": "101.6300",
                "5. volume": "22165128"
            },
            "2019-06-07": {
                "1. open": "102.6500",
                "2. high": "102.6900",
                "3. low": "100.3800",
                "4. close": "100.8800",
                "5. volume": "28232197"
            },
            "2019-06-06": {
                "1. open": "102.4800",
                "2. high": "102.6000",
                "3. low": "101.9000",
                "4. close": "102.4900",
                "5. volume": "21122917"
            }
        }
    }

    transformed_response = [
        {"timestamp": "2019-06-08", "open": 101.0924, "high": 101.95, "low": 100.54, "close": 101.63, "volume": 22165128},
        {"timestamp": "2019-06-07", "open": 102.65, "high": 102.69, "low": 100.38, "close": 100.88, "volume": 28232197},
        {"timestamp": "2019-06-06", "open": 102.48, "high": 102.60, "low": 101.90, "close": 102.49, "volume": 21122917},
    ]

    assert calculate_prices(parsed_response) == transformed_response




def test_write_to_csv():

    # SETUP

    example_rows = [
        {"timestamp": "2019-06-08", "open": "101.0924", "high": "101.9500", "low": "100.5400", "close": "101.6300", "volume": "22165128"},
        {"timestamp": "2019-06-07", "open": "102.6500", "high": "102.6900", "low": "100.3800", "close": "100.8800", "volume": "28232197"},
        {"timestamp": "2019-06-06", "open": "102.4800", "high": "102.6000", "low": "101.9000", "close": "102.4900", "volume": "21122917"},
        {"timestamp": "2019-06-05", "open": "102.0000", "high": "102.3300", "low": "101.5300", "close": "102.1900", "volume": "23514402"},
        {"timestamp": "2019-06-04", "open": "101.2600", "high": "101.8600", "low": "100.8510", "close": "101.6700", "volume": "27281623"},
        {"timestamp": "2019-06-01", "open": '99.2798',  "high": "100.8600", "low": "99.1700",  "close": "100.7900", "volume": "28655624"}
    ]

    example_rows_wrong = [
        {"timestamp": "2019-06-01", "open": "101.0924", "high": "101.9500", "low": "100.5400", "close": "101.6300", "volume": "22165128"},
        {"timestamp": "2019-06-07", "open": "102.6500", "high": "102.6900", "low": "100.3800", "close": "100.8800", "volume": "28232197"},
        {"timestamp": "2019-06-06", "open": "102.4800", "high": "102.6000", "low": "101.9000", "close": "102.4900", "volume": "21122917"},
        {"timestamp": "2019-06-05", "open": "102.0000", "high": "102.3300", "low": "101.5300", "close": "102.1900", "volume": "23514402"},
        {"timestamp": "2019-06-04", "open": "101.2600", "high": "101.8600", "low": "100.8510", "close": "101.6700", "volume": "27281623"},
        {"timestamp": "2019-06-01", "open": '99.2798',  "high": "100.8600", "low": "99.1700",  "close": "100.7900", "volume": "28655624"}
    ]

    csv_filepath = os.path.join(os.path.dirname(__file__), "example_reports", "temp_prices.csv")

    if os.path.isfile(csv_filepath):
        os.remove(csv_filepath)

    assert os.path.isfile(csv_filepath) == False # just making sure the test was setup properly

    # INVOCATION

    result = write_to_csv(example_rows, csv_filepath)

    # EXPECTATIONS

    assert result == True
    assert os.path.isfile(csv_filepath) == True

    with open(csv_filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        assert [row for row in reader] == example_rows
    