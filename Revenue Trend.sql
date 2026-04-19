USE product_analytics;

SELECT
    DATE_FORMAT(invoice_date, '%Y-%m') AS month,
    COUNT(DISTINCT customer_id)        AS active_customers,
    COUNT(DISTINCT invoice_no)         AS total_orders,
    ROUND(SUM(revenue), 2)             AS total_revenue,
    ROUND(AVG(revenue), 2)             AS avg_order_value
FROM transactions
GROUP BY DATE_FORMAT(invoice_date, '%Y-%m')
ORDER BY month;