"""
Data quality checks for banking datasets.
"""

import pandas as pd

def check_nulls(df: pd.DataFrame, columns: list) -> dict:
    results = {}
    for col in columns:
        null_count = df[col].isnull().sum()
        results[col] = {
            "null_count": int(null_count),
            "pass": null_count == 0
        }
    return results

def check_transaction_amounts(df: pd.DataFrame) -> dict:
    invalid = df[df["amount"].isnull() | (df["amount"] == 0)]
    return {
        "invalid_amount_count": len(invalid),
        "pass": len(invalid) == 0
    }

def check_status_values(df: pd.DataFrame, column: str, allowed: list) -> dict:
    invalid = ~df[column].isin(allowed)
    return {
        "invalid_count": int(invalid.sum()),
        "pass": invalid.sum() == 0
    }

def run_quality_checks():
    tx = pd.read_csv("data/processed/transactions_target.csv")
    results = {
        "null_checks": check_nulls(tx, ["transaction_id", "account_id", "amount"]),
        "amount_checks": check_transaction_amounts(tx),
        "status_checks": check_status_values(tx, "status", ["COMPLETED", "PENDING", "FAILED"])
    }
    return results

if __name__ == "__main__":
    print(run_quality_checks())
