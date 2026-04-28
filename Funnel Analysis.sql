USE product_analytics;

-- FUNNEL ANALYSIS
WITH customer_stats AS (
    SELECT
        customer_id,
        COUNT(DISTINCT invoice_no) AS total_orders,
        SUM(revenue)               AS total_revenue
    FROM transactions
    GROUP BY customer_id
)
SELECT 'Total Customers'         AS funnel_stage, COUNT(*)                                            AS customers, 1 AS step FROM customer_stats
UNION ALL
SELECT 'Purchased Once',          SUM(CASE WHEN total_orders >= 1 THEN 1 ELSE 0 END), 2 FROM customer_stats
UNION ALL
SELECT 'Purchased 2+ Times',      SUM(CASE WHEN total_orders >= 2 THEN 1 ELSE 0 END), 3 FROM customer_stats
UNION ALL
SELECT 'Purchased 5+ Times',      SUM(CASE WHEN total_orders >= 5 THEN 1 ELSE 0 END), 4 FROM customer_stats
UNION ALL
SELECT 'High Value (Revenue>500)',SUM(CASE WHEN total_revenue > 500 THEN 1 ELSE 0 END),5 FROM customer_stats
ORDER BY step;