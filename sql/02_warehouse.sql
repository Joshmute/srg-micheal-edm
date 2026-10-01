-- UTC DATETIME values in storage; derive Ugandan business DATE in the source adapter.
CREATE TABLE warehouse.dim_date(date_key date PRIMARY KEY,month_start date NOT NULL,year int NOT NULL);
CREATE TABLE warehouse.dim_customer(
 customer_key bigint AUTO_INCREMENT PRIMARY KEY,customer_token char(64) NOT NULL UNIQUE,segment varchar(64) NOT NULL);
CREATE TABLE warehouse.dim_product(
 product_key bigint AUTO_INCREMENT PRIMARY KEY,product_id varchar(64) NOT NULL,
 name varchar(200) NOT NULL,category varchar(100) NOT NULL,unit varchar(10) NOT NULL,
 valid_from datetime(6) NOT NULL,valid_to datetime(6),
 current_id varchar(64) GENERATED ALWAYS AS (CASE WHEN valid_to IS NULL THEN product_id ELSE NULL END) STORED,
 UNIQUE(current_id),UNIQUE(product_id,valid_from),CHECK(valid_to IS NULL OR valid_to>valid_from));
CREATE TABLE warehouse.dim_store(
 store_key bigint AUTO_INCREMENT PRIMARY KEY,store_id varchar(64) NOT NULL,district varchar(100) NOT NULL,
 valid_from datetime(6) NOT NULL,valid_to datetime(6),
 current_id varchar(64) GENERATED ALWAYS AS (CASE WHEN valid_to IS NULL THEN store_id ELSE NULL END) STORED,
 UNIQUE(current_id),UNIQUE(store_id,valid_from),CHECK(valid_to IS NULL OR valid_to>valid_from));
-- MySQL has no PostgreSQL-style exclusion constraint. Controlled procedures serialize all history writes.
CREATE TABLE warehouse.dimension_lock(domain_name varchar(16),natural_id varchar(64),PRIMARY KEY(domain_name,natural_id));
CREATE TABLE warehouse.fact_sales(
 source varchar(32),source_order_id varchar(64),line_no int,
 date_key date NOT NULL,customer_key bigint,product_key bigint NOT NULL,store_key bigint NOT NULL,
 quantity decimal(14,3) NOT NULL,net_amount decimal(18,2) NOT NULL,currency char(3) NOT NULL,
 PRIMARY KEY(source,source_order_id,line_no),
 FOREIGN KEY(date_key) REFERENCES warehouse.dim_date(date_key),
 FOREIGN KEY(customer_key) REFERENCES warehouse.dim_customer(customer_key),
 FOREIGN KEY(product_key) REFERENCES warehouse.dim_product(product_key),
 FOREIGN KEY(store_key) REFERENCES warehouse.dim_store(store_key));
CREATE TABLE warehouse.fact_payment(
 source varchar(32),provider_ref varchar(128),store_key bigint,occurred_at datetime(6),
 amount decimal(18,2),currency char(3),status varchar(16),PRIMARY KEY(source,provider_ref),
 FOREIGN KEY(store_key) REFERENCES warehouse.dim_store(store_key));
CREATE TABLE warehouse.fact_inventory_snapshot(
 snapshot_at datetime(6),store_key bigint,product_key bigint,on_hand decimal(14,3),
 PRIMARY KEY(snapshot_at,store_key,product_key),
 FOREIGN KEY(store_key) REFERENCES warehouse.dim_store(store_key),FOREIGN KEY(product_key) REFERENCES warehouse.dim_product(product_key));
CREATE SQL SECURITY DEFINER VIEW analytics.monthly_sales AS
 SELECT CAST(DATE_FORMAT(f.date_key,'%Y-%m-01') AS DATE) AS month_start,s.district,p.category,f.currency,
 SUM(f.net_amount) AS net_sales,SUM(f.quantity) AS net_units,
 COUNT(DISTINCT CASE WHEN f.quantity>0 THEN f.customer_key END) AS active_customers
 FROM warehouse.fact_sales f JOIN warehouse.dim_store s ON f.store_key=s.store_key
 JOIN warehouse.dim_product p ON f.product_key=p.product_key GROUP BY 1,2,3,4;
-- Counts are non-additive: recompute distinct customers across categories, never sum these counts.
