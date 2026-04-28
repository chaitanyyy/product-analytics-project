USE product_analytics;

WITH first_purchase AS (
    SELECT
        customer_id,
        DATE_FORMAT(MIN(invoice_date), '%Y-%m-01') AS cohort_month
    FROM transactions
    GROUP BY customer_id
),
monthly_activity AS (
    SELECT DISTINCT
        customer_id,
        DATE_FORMAT(invoice_date, '%Y-%m-01') AS activity_month
    FROM transactions
),
cohort_data AS (
    SELECT
        f.customer_id,
        f.cohort_month,
        m.activity_month,
        PERIOD_DIFF(
            DATE_FORMAT(m.activity_month, '%Y%m'),
            DATE_FORMAT(f.cohort_month,   '%Y%m')
        ) AS month_number
    FROM first_purchase f
    JOIN monthly_activity m ON f.customer_id = m.customer_id
),
cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT customer_id) AS total_users
    FROM first_purchase
    GROUP BY cohort_month
)
SELECT
    c.cohort_month,
    cs.total_users        AS cohort_size,
    c.month_number,
    COUNT(DISTINCT c.customer_id) AS retained_users,
    ROUND(
        100.0 * COUNT(DISTINCT c.customer_id) / cs.total_users, 1
    ) AS retention_pct
FROM cohort_data c
JOIN cohort_size cs ON c.cohort_month = cs.cohort_month
GROUP BY c.cohort_month, cs.total_users, c.month_number
ORDER BY c.cohort_month, c.month_number;