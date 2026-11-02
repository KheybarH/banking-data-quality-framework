import pytest
from src.data_generator import generate_customers, generate_accounts

def test_generate_customers():
    df = generate_customers(10)
    assert len(df) == 10
    assert "customer_id" in df.columns
    assert df["customer_id"].is_unique

def test_generate_accounts():
    customers = generate_customers(5)
    accounts = generate_accounts(customers, 10)
    assert len(accounts) == 10
    assert accounts["customer_id"].isin(customers["customer_id"]).all()
