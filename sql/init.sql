-- Banking Data Quality Framework - Database Initialization
-- Source and Target schemas for reconciliation demo

CREATE SCHEMA IF NOT EXISTS source;
CREATE SCHEMA IF NOT EXISTS target;
CREATE SCHEMA IF NOT EXISTS dq;

-- Customers
CREATE TABLE IF NOT EXISTS source.customers (
    customer_id     VARCHAR(20) PRIMARY KEY,
    full_name       VARCHAR(200),
    email           VARCHAR(200),
    phone           VARCHAR(50),
    city            VARCHAR(100),
    registration_date DATE,
    status          VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS target.customers (
    LIKE source.customers INCLUDING ALL
);

-- Accounts
CREATE TABLE IF NOT EXISTS source.accounts (
    account_id      VARCHAR(20) PRIMARY KEY,
    customer_id     VARCHAR(20),
    account_type    VARCHAR(20),
    balance         NUMERIC(15,2),
    currency        VARCHAR(3),
    opened_date     DATE,
    status          VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS target.accounts (
    LIKE source.accounts INCLUDING ALL
);

-- Transactions
CREATE TABLE IF NOT EXISTS source.transactions (
    transaction_id      VARCHAR(20) PRIMARY KEY,
    account_id          VARCHAR(20),
    amount              NUMERIC(15,2),
    transaction_type    VARCHAR(10),
    transaction_date    TIMESTAMP,
    description         VARCHAR(500),
    status              VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS target.transactions (
    LIKE source.transactions INCLUDING ALL
);

-- DQ results table (for trends later)
CREATE TABLE IF NOT EXISTS dq.results (
    run_id          UUID DEFAULT gen_random_uuid(),
    check_name      VARCHAR(100),
    severity        VARCHAR(20),
    passed          BOOLEAN,
    details         JSONB,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for reconciliation performance
CREATE INDEX IF NOT EXISTS idx_src_tx_account ON source.transactions(account_id);
CREATE INDEX IF NOT EXISTS idx_tgt_tx_account ON target.transactions(account_id);
CREATE INDEX IF NOT EXISTS idx_src_acc_customer ON source.accounts(customer_id);
CREATE INDEX IF NOT EXISTS idx_tgt_acc_customer ON target.accounts(customer_id);
