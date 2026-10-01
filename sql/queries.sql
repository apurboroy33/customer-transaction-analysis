-- ============================================
-- 1. TOTAL REVENUE
-- ============================================

SELECT
    SUM(amount) AS total_revenue
FROM transactions;

-- ============================================
-- 2. TOTAL TRANSACTIONS
-- ============================================

SELECT
    COUNT(*) AS total_transactions
FROM transactions;

-- ============================================
-- 3. AVERAGE TRANSACTION VALUE
-- ============================================

SELECT
    AVG(amount) AS average_transaction_value
FROM transactions;

-- ============================================
-- 4. MONTHLY REVENUE
-- ============================================

SELECT
    YEAR(transaction_date) AS year,
    MONTH(transaction_date) AS month,
    SUM(amount) AS revenue
FROM transactions
GROUP BY
    YEAR(transaction_date),
    MONTH(transaction_date)
ORDER BY
    year,
    month;

-- ============================================
-- 5. TOP 10 CUSTOMERS BY SPENDING
-- ============================================

SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount) AS total_spending
FROM customers c
JOIN transactions t
    ON c.customer_id = t.customer_id
GROUP BY
    c.customer_id,
    c.customer_name,
    c.city
ORDER BY
    total_spending DESC
LIMIT 10;

-- ============================================
-- 6. REVENUE BY CATEGORY
-- ============================================

SELECT
    p.category,
    SUM(t.amount) AS total_revenue,
    COUNT(t.transaction_id) AS total_transactions
FROM transactions t
JOIN products p
    ON t.product_id = p.product_id
GROUP BY
    p.category
ORDER BY
    total_revenue DESC;

-- ============================================
-- 7. TOP PRODUCTS BY QUANTITY SOLD
-- ============================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(t.quantity) AS units_sold
FROM transactions t
JOIN products p
    ON t.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY
    units_sold DESC
LIMIT 10;

-- ============================================
-- 8. PAYMENT METHOD ANALYSIS
-- ============================================

SELECT
    payment_method,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_revenue,
    AVG(amount) AS average_transaction_value
FROM transactions
GROUP BY
    payment_method
ORDER BY
    total_revenue DESC;

-- ============================================
-- 9. REVENUE BY CITY
-- ============================================

SELECT
    c.city,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount) AS total_revenue,
    AVG(t.amount) AS average_transaction_value
FROM customers c
JOIN transactions t
    ON c.customer_id = t.customer_id
GROUP BY
    c.city
ORDER BY
    total_revenue DESC;

-- ============================================
-- 10. CUSTOMER PURCHASE FREQUENCY
-- ============================================

SELECT
    customer_id,
    COUNT(transaction_id) AS purchase_frequency,
    SUM(amount) AS total_spending
FROM transactions
GROUP BY
    customer_id
ORDER BY
    purchase_frequency DESC;

-- ============================================
-- 11. REPEAT VS ONE-TIME CUSTOMERS
-- ============================================

SELECT
    CASE
        WHEN purchase_count = 1
            THEN 'One-Time Customer'
        ELSE 'Repeat Customer'
    END AS customer_type,

    COUNT(*) AS customer_count

FROM (
    SELECT
        customer_id,
        COUNT(*) AS purchase_count
    FROM transactions
    GROUP BY customer_id
) AS customer_purchases

GROUP BY
    customer_type;

-- ============================================
-- 11. REPEAT VS ONE-TIME CUSTOMERS
-- ============================================

SELECT
    CASE
        WHEN purchase_count = 1
            THEN 'One-Time Customer'
        ELSE 'Repeat Customer'
    END AS customer_type,

    COUNT(*) AS customer_count

FROM (
    SELECT
        customer_id,
        COUNT(*) AS purchase_count
    FROM transactions
    GROUP BY customer_id
) AS customer_purchases

GROUP BY
    customer_type;