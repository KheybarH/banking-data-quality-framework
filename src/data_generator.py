"""
Synthetic banking data generator.
Generates realistic source data and a slightly "dirty" target version for reconciliation demo.
"""

import pandas as pd
from faker import Faker
import random
import os
from datetime import datetime

fake = Faker()
Faker.seed(42)
random.seed(42)

def generate_customers(n=2000):
    return pd.DataFrame([{
        "customer_id": f"CUST{i+1:06d}",
        "full_name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "city": fake.city(),
        "registration_date": fake.date_between(start_date="-5y", end_date="today"),
        "status": random.choice(["ACTIVE", "ACTIVE", "ACTIVE", "INACTIVE"])
    } for i in range(n)])

def generate_accounts(customers_df, n_accounts=3000):
    customer_ids = customers_df["customer_id"].tolist()
    return pd.DataFrame([{
        "account_id": f"ACC{i+1:07d}",
        "customer_id": random.choice(customer_ids),
        "account_type": random.choice(["CHECKING", "SAVINGS", "CREDIT"]),
        "balance": round(random.uniform(0, 100000), 2),
        "currency": "USD",
        "opened_date": fake.date_between(start_date="-4y", end_date="today"),
        "status": random.choice(["OPEN", "OPEN", "OPEN", "CLOSED"])
    } for i in range(n_accounts)])

def generate_transactions(accounts_df, n_tx=20000):
    account_ids = accounts_df["account_id"].tolist()
    txs = []
    for i in range(n_tx):
        amount = round(random.uniform(-5000, 10000), 2)
        txs.append({
            "transaction_id": f"TXN{i+1:08d}",
            "account_id": random.choice(account_ids),
            "amount": amount,
            "transaction_type": "CREDIT" if amount > 0 else "DEBIT",
            "transaction_date": fake.date_time_between(start_date="-1y", end_date="now"),
            "description": fake.sentence(nb_words=5),
            "status": random.choice(["COMPLETED", "COMPLETED", "COMPLETED", "PENDING", "FAILED"])
        })
    return pd.DataFrame(txs)

def introduce_issues(df, table_name):
    """Introduce controlled data quality issues in target data."""
    dirty = df.copy()
    if table_name == "transactions":
        # Drop some rows
        dirty = dirty.sample(frac=0.98, random_state=42)
        # Change a few amounts
        dirty.loc[dirty.index[:10], "amount"] = dirty.loc[dirty.index[:10], "amount"] * 1.1
        # Add a couple of orphan transactions (invalid account)
        dirty.loc[dirty.index[:2], "account_id"] = "ACC_INVALID"
    return dirty

def main():
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    print("Generating synthetic banking data...")
    customers = generate_customers()
    accounts = generate_accounts(customers)
    transactions = generate_transactions(accounts)

    # Source (clean)
    customers.to_csv("data/raw/customers_source.csv", index=False)
    accounts.to_csv("data/raw/accounts_source.csv", index=False)
    transactions.to_csv("data/raw/transactions_source.csv", index=False)

    # Target (with intentional issues)
    customers_t = introduce_issues(customers, "customers")
    accounts_t = introduce_issues(accounts, "accounts")
    transactions_t = introduce_issues(transactions, "transactions")

    customers_t.to_csv("data/processed/customers_target.csv", index=False)
    accounts_t.to_csv("data/processed/accounts_target.csv", index=False)
    transactions_t.to_csv("data/processed/transactions_target.csv", index=False)

    print(f"Generated: {len(customers)} customers, {len(accounts)} accounts, {len(transactions)} transactions")
    print("Source → data/raw/ | Target → data/processed/")

if __name__ == "__main__":
    main()
