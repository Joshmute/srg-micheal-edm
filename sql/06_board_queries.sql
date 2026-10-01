-- MySQL 8.4. Parameterise dates/currency in the BI layer.
SET @month_start='2026-09-01';
SET @next_month='2026-10-01';
SET @currency='UGX';
SELECT SUM(net_amount) AS net_sales,
 COUNT(DISTINCT CASE WHEN quantity>0 THEN customer_key END) AS active_customers,
 SUM(customer_key IS NULL) AS anonymous_lines
FROM warehouse.fact_sales
WHERE date_key>=@month_start AND date_key<@next_month AND currency=@currency;

SELECT s.store_id,p.category,f.currency,SUM(f.net_amount) AS net_sales
FROM warehouse.fact_sales f JOIN warehouse.dim_store s ON f.store_key=s.store_key
JOIN warehouse.dim_product p ON f.product_key=p.product_key
WHERE f.date_key>=@month_start AND f.date_key<@next_month AND f.currency=@currency
GROUP BY s.store_id,p.category,f.currency ORDER BY net_sales DESC;

-- Freshness must accompany inventory. Quantity cannot infer demand or stock-outs alone.
SELECT s.store_id,MAX(i.snapshot_at) AS latest_snapshot_utc
FROM warehouse.fact_inventory_snapshot i JOIN warehouse.dim_store s ON i.store_key=s.store_key
GROUP BY s.store_id;
