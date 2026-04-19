USE product_analytics;

SELECT
    customer_id,
    country,
    COUNT(DISTINCT invoice_no)      AS total_orders,
    ROUND(SUM(revenue), 2)          AS total_revenue,
    MIN(invoice_date)               AS first_purchase,
    MAX(invoice_date)               AS last_purchase,
    DATEDIFF('2011-12-09',
             MAX(invoice_date))     AS days_inactive,

    CASE
        WHEN DATEDIFF('2011-12-09', MAX(invoice_date)) > 90
            THEN 'High Risk'
        WHEN DATEDIFF('2011-12-09', MAX(invoice_date)) > 45
            THEN 'Medium Risk'
        WHEN DATEDIFF('2011-12-09', MAX(invoice_date)) > 20
            THEN 'Low Risk'
        ELSE 'Active'
    END AS churn_risk,

    CASE
        WHEN SUM(revenue) > 1000 THEN 'High Value'
        WHEN SUM(revenue) > 300  THEN 'Mid Value'
        ELSE 'Low Value'
    END AS value_segment

FROM transactions
GROUP BY customer_id, country
ORDER BY total_revenue DESC;