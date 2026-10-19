"""
Synthetic banking data generator.
Creates realistic source and target datasets for reconciliation testing.
"""

import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import random
import os

fake = Faker()
Faker.seed(42)
random.seed(42)

def generate_customers(n=1000):
    customers = []
    for i in range(n):
        customers.append({
            "customer_id": f"CUST{i+1:06d}",
            "full_name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "city": fake.city(),
            "registration_date": fake.date_between(start_date="-5y", end_date="today"),
            "status": random.choice(["ACTIVE", "ACTIVE", "ACTIVE", "INACTIVE"])
        })
    return pd.DataFrame(customers)

def generate_accounts(customers_df, n_accounts=1500):
    accounts = []
    customer_ids = customers_df["customer_id"].tolist()
    for i in range(n_accounts):
        accounts.append({
            "account_id": f"ACC{i+1:07d}",
            "customer_id": random.choice(customer_ids),
            "account_type": random.choice(["CHECKING", "SAVINGS", "CREDIT"]),
            "balance": round(random.uniform(0, 50000), 2),
            "currency": "USD",
            "opened_date": fake.date_between(start_date="-4y", end_date="today"),
            "status": random.choice(["OPEN", "OPEN", "OPEN", "CLOSED"])
        })
    return pd.DataFrame(accounts)

def generate_transactions(accounts_df, n_tx=10000):
    transactions = []
    account_ids = accounts_df["account_id"].tolist()
    for i in range(n_tx):
        amount = round(random.uniform(-2000, 5000), 2)
        transactions.append({
            "transaction_id": f"TXN{i+1:08d}",
            "account_id": random.choice(account_ids),
            "amount": amount,
            "transaction_type": "CREDIT" if amount > 0 else "DEBIT",
            "transaction_date": fake.date_time_between(start_date="-1y", end_date="now"),
            "description": fake.sentence(nb_words=4),
            "status": random.choice(["COMPLETED", "COMPLETED", "COMPLETED", "PENDING", "FAILED"])
        })
    return pd.DataFrame(transactions)

def main():
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    print("Generating synthetic banking data...")
    customers = generate_customers(1000)
    accounts = generate_accounts(customers, 1500)
    transactions = generate_transactions(accounts, 10000)

    # Source (raw)
    customers.to_csv("data/raw/customers_source.csv", index=False)
    accounts.to_csv("data/raw/accounts_source.csv", index=False)
    transactions.to_csv("data/raw/transactions_source.csv", index=False)

    # Target (with some intentional differences for testing)
    customers_target = customers.copy()
    accounts_target = accounts.copy()
    transactions_target = transactions.copy()

    # Introduce some data quality issues in target
    transactions_target.loc[transactions_target.sample(50).index, "amount"] = None
    transactions_target = transactions_target.drop(transactions_target.sample(20).index)

    customers_target.to_csv("data/processed/customers_target.csv", index=False)
    accounts_target.to_csv("data/processed/accounts_target.csv", index=False)
    transactions_target.to_csv("data/processed/transactions_target.csv", index=False)

    print(f"Generated: {len(customers)} customers, {len(accounts)} accounts, {len(transactions)} transactions")
    print("Source and target files saved.")

if __name__ == "__main__":
    main()
