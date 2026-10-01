-- Run after validated sales_stage.sql in the SAME session.
-- Requires preapproved dimension_customer_map and staged historical dimensions.
-- This map is restricted identity linkage, populated only from approved golden IDs/tokens.
CREATE TABLE IF NOT EXISTS warehouse.customer_source_map(
 source_customer_id varchar(64) PRIMARY KEY,customer_key bigint NOT NULL,
 FOREIGN KEY(customer_key) REFERENCES warehouse.dim_customer(customer_key));
DELIMITER //
CREATE PROCEDURE warehouse.load_staged_sales()
SQL SECURITY DEFINER
BEGIN
 DECLARE unresolved int DEFAULT 0; DECLARE conflicts int DEFAULT 0;
 DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; RESIGNAL; END;
 START TRANSACTION;
 SELECT COUNT(*) INTO unresolved FROM warehouse.stage_sales st
 LEFT JOIN warehouse.customer_source_map c ON st.customer_id=c.source_customer_id
 LEFT JOIN warehouse.dim_product p ON st.sku=p.product_id AND st.order_date>=p.valid_from AND (st.order_date<p.valid_to OR p.valid_to IS NULL)
 LEFT JOIN warehouse.dim_store s ON st.store_id=s.store_id AND st.order_date>=s.valid_from AND (st.order_date<s.valid_to OR s.valid_to IS NULL)
 WHERE p.product_key IS NULL OR s.store_key IS NULL OR (st.customer_id IS NOT NULL AND c.customer_key IS NULL);
 IF unresolved>0 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Unresolved staged dimension keys'; END IF;
 INSERT IGNORE INTO warehouse.dim_date(date_key,month_start,year)
 SELECT DISTINCT order_date,CAST(DATE_FORMAT(order_date,'%Y-%m-01') AS DATE),YEAR(order_date) FROM warehouse.stage_sales;
 -- Detect changed replay rather than silently overwriting a fact.
 SELECT COUNT(*) INTO conflicts FROM warehouse.stage_sales st
 JOIN warehouse.fact_sales f ON f.source=st.source AND f.source_order_id=st.order_id AND f.line_no=st.line_no
 JOIN warehouse.dim_product p ON st.sku=p.product_id AND st.order_date>=p.valid_from AND (st.order_date<p.valid_to OR p.valid_to IS NULL)
 JOIN warehouse.dim_store s ON st.store_id=s.store_id AND st.order_date>=s.valid_from AND (st.order_date<s.valid_to OR s.valid_to IS NULL)
 LEFT JOIN warehouse.customer_source_map c ON st.customer_id=c.source_customer_id
 WHERE NOT(f.date_key<=>st.order_date AND f.quantity<=>st.quantity AND f.net_amount<=>st.net_amount AND f.currency<=>st.currency
 AND f.product_key<=>p.product_key AND f.store_key<=>s.store_key AND f.customer_key<=>c.customer_key);
 IF conflicts>0 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Conflicting fact replay'; END IF;
 INSERT INTO warehouse.fact_sales(source,source_order_id,line_no,date_key,customer_key,product_key,store_key,quantity,net_amount,currency)
 SELECT st.source,st.order_id,st.line_no,st.order_date,c.customer_key,p.product_key,s.store_key,st.quantity,st.net_amount,st.currency
 FROM warehouse.stage_sales st
 JOIN warehouse.dim_product p ON st.sku=p.product_id AND st.order_date>=p.valid_from AND (st.order_date<p.valid_to OR p.valid_to IS NULL)
 JOIN warehouse.dim_store s ON st.store_id=s.store_id AND st.order_date>=s.valid_from AND (st.order_date<s.valid_to OR s.valid_to IS NULL)
 LEFT JOIN warehouse.customer_source_map c ON st.customer_id=c.source_customer_id
 LEFT JOIN warehouse.fact_sales f ON f.source=st.source AND f.source_order_id=st.order_id AND f.line_no=st.line_no
 WHERE f.source IS NULL;
 COMMIT;
END//
DELIMITER ;
-- Installation-only: CALL warehouse.load_staged_sales() after staging in a live session.
-- Date-grain extract assumes dimension changes effective at midnight. Intraday sources must carry event timestamp.
