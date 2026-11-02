"""
YAML-driven data quality engine.
Reads rules from config/rules.yaml and executes them against PostgreSQL.
"""

import yaml
from sqlalchemy import create_engine, text
import os
from datetime import datetime

DB_URL = os.getenv("DATABASE_URL", "postgresql://dq_user:dq_password@localhost:5432/banking_dq")

def load_rules(path="config/rules.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["rules"]

def run_rule(conn, rule):
    name = rule["name"]
    rtype = rule["type"]
    result = {"name": name, "severity": rule.get("severity", "info"), "passed": True, "details": {}}

    if rtype == "row_count":
        q = text(f"""
            SELECT 
                (SELECT COUNT(*) FROM source.{rule['table']}) AS src,
                (SELECT COUNT(*) FROM target.{rule['table']}) AS tgt
        """)
        row = conn.execute(q).fetchone()
        result["details"] = {"source": row.src, "target": row.tgt}
        result["passed"] = row.src == row.tgt

    elif rtype == "amount_sum":
        q = text("""
            SELECT 
                ROUND(COALESCE(SUM(amount),0),2) AS src_sum
            FROM source.transactions
        """)
        src = conn.execute(q).scalar()
        q2 = text("SELECT ROUND(COALESCE(SUM(amount),0),2) FROM target.transactions")
        tgt = conn.execute(q2).scalar()
        result["details"] = {"source_sum": float(src), "target_sum": float(tgt)}
        result["passed"] = abs(float(src) - float(tgt)) <= rule.get("threshold", 0)

    elif rtype == "missing_keys":
        q = text(f"""
            SELECT COUNT(*) FROM source.{rule['table']} s
            LEFT JOIN target.{rule['table']} t ON s.{rule['key']} = t.{rule['key']}
            WHERE t.{rule['key']} IS NULL
        """)
        cnt = conn.execute(q).scalar()
        result["details"] = {"missing": cnt}
        result["passed"] = cnt <= rule.get("threshold", 0)

    elif rtype == "uniqueness":
        q = text(f"""
            SELECT COUNT(*) FROM (
                SELECT {rule['column']} FROM source.{rule['table']}
                GROUP BY {rule['column']} HAVING COUNT(*) > 1
            ) d
        """)
        cnt = conn.execute(q).scalar()
        result["details"] = {"duplicates": cnt}
        result["passed"] = cnt == 0

    elif rtype == "referential_integrity":
        q = text(f"""
            SELECT COUNT(*) FROM source.{rule['child_table']} c
            LEFT JOIN source.{rule['parent_table']} p 
              ON c.{rule['child_key']} = p.{rule['parent_key']}
            WHERE p.{rule['parent_key']} IS NULL
        """)
        cnt = conn.execute(q).scalar()
        result["details"] = {"orphans": cnt}
        result["passed"] = cnt <= rule.get("threshold", 0)

    elif rtype == "freshness":
        q = text(f"""
            SELECT EXTRACT(DAY FROM (CURRENT_TIMESTAMP - MAX({rule['date_column']}))) 
            FROM source.{rule['table']}
        """)
        days = conn.execute(q).scalar() or 999
        result["details"] = {"days_since_last": float(days)}
        result["passed"] = float(days) <= rule.get("threshold", 7)

    else:
        result["details"] = {"note": "Check type not yet implemented"}
        result["passed"] = True

    return result

def run_all():
    rules = load_rules()
    engine = create_engine(DB_URL)
    results = []

    with engine.connect() as conn:
        for rule in rules:
            res = run_rule(conn, rule)
            results.append(res)
            status = "PASS" if res["passed"] else "FAIL"
            print(f"[{res['severity'].upper()}] {res['name']}: {status} | {res['details']}")

    # Summary
    critical_fails = sum(1 for r in results if not r["passed"] and r["severity"] == "critical")
    print(f"\n=== Summary: {critical_fails} critical failure(s) ===")
    return results

if __name__ == "__main__":
    run_all()
