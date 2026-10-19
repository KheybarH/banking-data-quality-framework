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

def check_schema_drift(source_df: pd.DataFrame, target_df: pd.DataFrame) -> dict:
    src_cols = set(source_df.columns)
    tgt_cols = set(target_df.columns)
    missing = src_cols - tgt_cols
    extra = tgt_cols - src_cols
    return {
        "missing_columns": list(missing),
        "extra_columns": list(extra),
        "pass": len(missing) == 0 and len(extra) == 0
    }

def run_quality_checks():
    source = pd.read_csv("data/raw/transactions_source.csv")
    target = pd.read_csv("data/processed/transactions_target.csv")
    
    results = {
        "null_checks": check_nulls(target, ["transaction_id", "account_id", "amount"]),
        "amount_checks": check_transaction_amounts(target),
        "status_checks": check_status_values(target, "status", ["COMPLETED", "PENDING", "FAILED"]),
        "schema_drift": check_schema_drift(source, target)
    }
    return results

if __name__ == "__main__":
    import json
    print(json.dumps(run_quality_checks(), indent=2))