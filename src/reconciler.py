"""
Core reconciliation logic between source and target datasets.
"""

import pandas as pd
from pathlib import Path

class DataReconciler:
    def __init__(self, source_path: str, target_path: str, key_column: str):
        self.source = pd.read_csv(source_path)
        self.target = pd.read_csv(target_path)
        self.key_column = key_column
        self.results = {}

    def check_row_count(self):
        src_count = len(self.source)
        tgt_count = len(self.target)
        match = src_count == tgt_count
        self.results["row_count"] = {
            "source": src_count,
            "target": tgt_count,
            "match": match,
            "difference": src_count - tgt_count
        }
        return match

    def check_key_uniqueness(self):
        src_unique = self.source[self.key_column].is_unique
        tgt_unique = self.target[self.key_column].is_unique
        self.results["key_uniqueness"] = {
            "source_unique": src_unique,
            "target_unique": tgt_unique,
            "pass": src_unique and tgt_unique
        }
        return src_unique and tgt_unique

    def check_missing_keys(self):
        src_keys = set(self.source[self.key_column])
        tgt_keys = set(self.target[self.key_column])
        missing_in_target = src_keys - tgt_keys
        extra_in_target = tgt_keys - src_keys
        self.results["missing_keys"] = {
            "missing_in_target": len(missing_in_target),
            "extra_in_target": len(extra_in_target),
            "pass": len(missing_in_target) == 0 and len(extra_in_target) == 0
        }
        return self.results["missing_keys"]["pass"]

    def run_all(self):
        self.check_row_count()
        self.check_key_uniqueness()
        self.check_missing_keys()
        return self.results

def reconcile_transactions():
    reconciler = DataReconciler(
        source_path="data/raw/transactions_source.csv",
        target_path="data/processed/transactions_target.csv",
        key_column="transaction_id"
    )
    results = reconciler.run_all()
    print("Reconciliation Results:")
    for check, result in results.items():
        print(f"  {check}: {result}")
    return results

if __name__ == "__main__":
    reconcile_transactions()
