-- Synthetic data only. Tests execute in a disposable, network-isolated container.
INSERT INTO core.customer VALUES('DEMO1','Synthetic Person','+256772000001','example@example.invalid','Jinja',false);
INSERT INTO hr.employee VALUES('DEMO1','Synthetic Employee',1000,'DEMO-ONLY');
CALL warehouse.apply_product('P1','Rice','Grocery','kg','2026-01-01');
CALL warehouse.apply_product('P1','Rice','Staples','kg','2026-02-01');
CALL warehouse.apply_product('P1','Rice','Staples','kg','2026-02-01');
CALL warehouse.apply_store('S1','Jinja','2026-01-01');
CALL warehouse.apply_store('S1','Kampala','2026-03-01');
DELIMITER //
CREATE PROCEDURE warehouse.assert_demo()
BEGIN
 IF (SELECT COUNT(*) FROM warehouse.dim_product WHERE product_id='P1')<>2 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='SCD2 replay failed'; END IF;
 IF (SELECT COUNT(*) FROM warehouse.dim_store WHERE store_id='S1')<>2 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Store history failed'; END IF;
 IF (SELECT COUNT(*) FROM warehouse.dim_product WHERE product_id='P1' AND '2026-01-15'>=valid_from AND ('2026-01-15'<valid_to OR valid_to IS NULL))<>1 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Historical lookup failed'; END IF;
 SELECT 'PASS: MySQL product/store SCD2 replay and historical lookup' AS result;
END//
DELIMITER ;
CALL warehouse.assert_demo();
DROP PROCEDURE warehouse.assert_demo;
CREATE USER 'demo_analyst'@'localhost';
CREATE USER 'demo_steward'@'localhost';
CREATE USER 'demo_etl'@'localhost';
GRANT 'srg_analyst' TO 'demo_analyst'@'localhost';
GRANT 'srg_steward' TO 'demo_steward'@'localhost';
GRANT 'srg_etl' TO 'demo_etl'@'localhost';
SET DEFAULT ROLE 'srg_analyst' TO 'demo_analyst'@'localhost';
SET DEFAULT ROLE 'srg_steward' TO 'demo_steward'@'localhost';
SET DEFAULT ROLE 'srg_etl' TO 'demo_etl'@'localhost';
-- These passwordless local-only demo accounts are never suitable for deployment.
