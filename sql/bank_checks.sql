-- Additional bank-specific SQL checks

-- Duplicate detection
SELECT 
    transaction_id, 
    COUNT(*) AS cnt
FROM source.transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1;

-- Referential integrity: accounts without customers
SELECT COUNT(*) AS orphan_accounts
FROM source.accounts a
LEFT JOIN source.customers c ON a.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- Freshness check (days since last transaction)
SELECT 
    EXTRACT(DAY FROM (CURRENT_TIMESTAMP - MAX(transaction_date))) AS days_since_last
FROM source.transactions;

-- Simple balance style check (example)
SELECT 
    account_id,
    SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS total_credits,
    SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) AS total_debits
FROM source.transactions
GROUP BY account_id
LIMIT 10;
