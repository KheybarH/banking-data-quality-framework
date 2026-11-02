-- SQL-based Reconciliation Queries
-- Run these after data is loaded into source and target schemas

-- 1. Row count reconciliation
SELECT 
    'transactions_row_count' AS check_name,
    (SELECT COUNT(*) FROM source.transactions) AS source_count,
    (SELECT COUNT(*) FROM target.transactions) AS target_count,
    (SELECT COUNT(*) FROM source.transactions) = (SELECT COUNT(*) FROM target.transactions) AS match;

-- 2. Amount sum reconciliation (checksum)
SELECT 
    'transactions_amount_sum' AS check_name,
    ROUND(SUM(amount), 2) AS source_sum
FROM source.transactions
UNION ALL
SELECT 
    'transactions_amount_sum_target',
    ROUND(SUM(amount), 2)
FROM target.transactions;

-- 3. Missing / extra keys
SELECT 
    'missing_in_target' AS type,
    COUNT(*) AS cnt
FROM source.transactions s
LEFT JOIN target.transactions t ON s.transaction_id = t.transaction_id
WHERE t.transaction_id IS NULL

UNION ALL

SELECT 
    'extra_in_target',
    COUNT(*)
FROM target.transactions t
LEFT JOIN source.transactions s ON t.transaction_id = s.transaction_id
WHERE s.transaction_id IS NULL;

-- 4. Referential integrity: transactions pointing to non-existent accounts
SELECT COUNT(*) AS orphan_transactions
FROM source.transactions t
LEFT JOIN source.accounts a ON t.account_id = a.account_id
WHERE a.account_id IS NULL;
