CALL warehouse.apply_product('DEMO-RICE','Rice','Grocery','kg','2026-01-01');
CALL warehouse.apply_product('DEMO-TEA','Tea','Grocery','kg','2026-01-01');
CALL warehouse.apply_product('DEMO-SODA','Soda','Beverages','l','2026-01-01');
CALL warehouse.apply_store('DEMO-JINJA','Jinja','2026-01-01');
CALL warehouse.apply_store('DEMO-WEB','Kampala','2026-01-01');
CALL warehouse.apply_store('DEMO-GULU','Gulu','2026-01-01');
INSERT INTO warehouse.dim_customer(customer_token,segment) VALUES(SHA2('DEMO1-NOT-A-REAL-TOKEN',256),'Demo'),(SHA2('DEMO2-NOT-A-REAL-TOKEN',256),'Demo');
INSERT INTO warehouse.customer_source_map
SELECT 'DEMO1',customer_key FROM warehouse.dim_customer WHERE customer_token=SHA2('DEMO1-NOT-A-REAL-TOKEN',256);
INSERT INTO warehouse.customer_source_map
SELECT 'DEMO2',customer_key FROM warehouse.dim_customer WHERE customer_token=SHA2('DEMO2-NOT-A-REAL-TOKEN',256);
CALL warehouse.load_staged_sales();
CALL warehouse.load_staged_sales();
DELIMITER //
CREATE PROCEDURE warehouse.assert_sales_demo()
BEGIN
 IF (SELECT COUNT(*) FROM warehouse.fact_sales)<>4 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Wrong fact count or duplicate replay'; END IF;
 IF (SELECT SUM(net_amount) FROM warehouse.fact_sales)<>11500 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Sales total failed'; END IF;
 SELECT 'PASS: MySQL staged ETL, replay, returns, 4 facts and UGX 11500 synthetic total' AS result;
END//
DELIMITER ;
CALL warehouse.assert_sales_demo();
SELECT * FROM analytics.monthly_sales;
DROP PROCEDURE warehouse.assert_sales_demo;
