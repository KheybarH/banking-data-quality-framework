"""
SQL-based reconciliation runner.
Executes key reconciliation checks against PostgreSQL and prints results.
"""

from sqlalchemy import create_engine, text
import os
import json
from datetime import datetime

DB_URL = os.getenv("DATABASE_URL", "postgresql://dq_user:dq_password@localhost:5432/banking_dq")

QUERIES = {
    "row_count_transactions": """
        SELECT 
            (SELECT COUNT(*) FROM source.transactions) AS source_count,
            (SELECT COUNT(*) FROM target.transactions) AS target_count,
            (SELECT COUNT(*) FROM source.transactions) = (SELECT COUNT(*) FROM target.transactions) AS match
    """,
    "amount_sum_transactions": """
        SELECT 
            ROUND(COALESCE(SUM(amount), 0), 2) AS source_sum
        FROM source.transactions
    """,
    "amount_sum_target": """
        SELECT ROUND(COALESCE(SUM(amount), 0), 2) AS target_sum FROM target.transactions
    """,
    "missing_keys": """
        SELECT COUNT(*) AS missing_in_target
        FROM source.transactions s
        LEFT JOIN target.transactions t ON s.transaction_id = t.transaction_id
        WHERE t.transaction_id IS NULL
    """,
    "extra_keys": """
        SELECT COUNT(*) AS extra_in_target
        FROM target.transactions t
        LEFT JOIN source.transactions s ON t.transaction_id = s.transaction_id
        WHERE s.transaction_id IS NULL
    """,
    "orphan_transactions": """
        SELECT COUNT(*) AS orphan_count
        FROM source.transactions t
        LEFT JOIN source.accounts a ON t.account_id = a.account_id
        WHERE a.account_id IS NULL
    """
}

def run_reconciliation():
    engine = create_engine(DB_URL)
    results = {"timestamp": datetime.now().isoformat(), "checks": {}}

    with engine.connect() as conn:
        for name, query in QUERIES.items():
            row = conn.execute(text(query)).fetchone()
            results["checks"][name] = dict(row._mapping) if row else {}

    # Simple pass/fail summary
    rc = results["checks"].get("row_count_transactions", {})
    results["summary"] = {
        "row_count_match": rc.get("match", False),
        "missing_keys": results["checks"].get("missing_keys", {}).get("missing_in_target", 0),
        "extra_keys": results["checks"].get("extra_keys", {}).get("extra_in_target", 0),
        "orphan_transactions": results["checks"].get("orphan_transactions", {}).get("orphan_count", 0)
    }

    print(json.dumps(results, indent=2, default=str))
    return results

if __name__ == "__main__":
    run_reconciliation()
