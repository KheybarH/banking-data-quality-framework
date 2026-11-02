"""
Load CSV data into PostgreSQL source and target schemas.
"""

import pandas as pd
from sqlalchemy import create_engine
import os

DB_URL = os.getenv("DATABASE_URL", "postgresql://dq_user:dq_password@localhost:5432/banking_dq")

def load_table(csv_path, schema, table):
    df = pd.read_csv(csv_path)
    engine = create_engine(DB_URL)
    df.to_sql(table, engine, schema=schema, if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into {schema}.{table}")

def main():
    print("Loading data into PostgreSQL...")
    load_table("data/raw/customers_source.csv", "source", "customers")
    load_table("data/raw/accounts_source.csv", "source", "accounts")
    load_table("data/raw/transactions_source.csv", "source", "transactions")

    load_table("data/processed/customers_target.csv", "target", "customers")
    load_table("data/processed/accounts_target.csv", "target", "accounts")
    load_table("data/processed/transactions_target.csv", "target", "transactions")
    print("Load complete.")

if __name__ == "__main__":
    main()
