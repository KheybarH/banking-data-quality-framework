"""
Basic tests for the data quality framework.
"""

import pytest
import pandas as pd
from src.quality_checks import check_nulls, check_transaction_amounts

def test_check_nulls_pass():
    df = pd.DataFrame({"id": [1, 2, 3], "amount": [10, 20, 30]})
    result = check_nulls(df, ["id", "amount"])
    assert result["id"]["pass"] is True
    assert result["amount"]["pass"] is True

def test_check_nulls_fail():
    df = pd.DataFrame({"id": [1, 2, None], "amount": [10, None, 30]})
    result = check_nulls(df, ["id", "amount"])
    assert result["id"]["pass"] is False
    assert result["amount"]["pass"] is False

def test_transaction_amounts():
    df = pd.DataFrame({"amount": [100, -50, 0, None]})
    result = check_transaction_amounts(df)
    assert result["pass"] is False
    assert result["invalid_amount_count"] > 0
