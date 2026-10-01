-- Standalone transactional procedures: do not CALL inside a larger fact transaction.
-- Production: install under a dedicated locked migration/definer account, never an application administrator.
DELIMITER //
CREATE PROCEDURE warehouse.apply_product(IN p_id varchar(64),IN p_name varchar(200),IN p_category varchar(100),IN p_unit varchar(10),IN p_effective datetime(6))
SQL SECURITY DEFINER
BEGIN
 DECLARE v_key bigint DEFAULT NULL; DECLARE v_start datetime(6); DECLARE v_name varchar(200);
 DECLARE v_category varchar(100); DECLARE v_unit varchar(10); DECLARE v_lock varchar(64);
 DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_key=NULL;
 DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; RESIGNAL; END;
 IF p_id IS NULL OR p_effective IS NULL THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Missing dimension key/time'; END IF;
 START TRANSACTION;
 INSERT IGNORE INTO warehouse.dimension_lock VALUES('product',p_id);
 SELECT natural_id INTO v_lock FROM warehouse.dimension_lock WHERE domain_name='product' AND natural_id=p_id FOR UPDATE;
 SELECT product_key,valid_from,name,category,unit INTO v_key,v_start,v_name,v_category,v_unit
 FROM warehouse.dim_product WHERE current_id=p_id FOR UPDATE;
 IF v_key IS NOT NULL AND p_effective<v_start THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Late history requires controlled rebuild'; END IF;
 IF v_key IS NULL OR NOT(v_name<=>p_name AND v_category<=>p_category AND v_unit<=>p_unit) THEN
  IF v_key IS NOT NULL AND p_effective=v_start THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Conflicting same-time version'; END IF;
  IF v_key IS NOT NULL THEN UPDATE warehouse.dim_product SET valid_to=p_effective WHERE product_key=v_key; END IF;
  INSERT INTO warehouse.dim_product(product_id,name,category,unit,valid_from) VALUES(p_id,p_name,p_category,p_unit,p_effective);
 END IF;
 COMMIT;
END//
CREATE PROCEDURE warehouse.apply_store(IN p_id varchar(64),IN p_district varchar(100),IN p_effective datetime(6))
SQL SECURITY DEFINER
BEGIN
 DECLARE v_key bigint DEFAULT NULL; DECLARE v_start datetime(6); DECLARE v_district varchar(100); DECLARE v_lock varchar(64);
 DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_key=NULL;
 DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; RESIGNAL; END;
 IF p_id IS NULL OR p_effective IS NULL THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Missing dimension key/time'; END IF;
 START TRANSACTION;
 INSERT IGNORE INTO warehouse.dimension_lock VALUES('store',p_id);
 SELECT natural_id INTO v_lock FROM warehouse.dimension_lock WHERE domain_name='store' AND natural_id=p_id FOR UPDATE;
 SELECT store_key,valid_from,district INTO v_key,v_start,v_district FROM warehouse.dim_store WHERE current_id=p_id FOR UPDATE;
 IF v_key IS NOT NULL AND p_effective<v_start THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Late history requires controlled rebuild'; END IF;
 IF v_key IS NULL OR NOT(v_district<=>p_district) THEN
  IF v_key IS NOT NULL AND p_effective=v_start THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Conflicting same-time version'; END IF;
  IF v_key IS NOT NULL THEN UPDATE warehouse.dim_store SET valid_to=p_effective WHERE store_key=v_key; END IF;
  INSERT INTO warehouse.dim_store(store_id,district,valid_from) VALUES(p_id,p_district,p_effective);
 END IF;
 COMMIT;
END//
DELIMITER ;
