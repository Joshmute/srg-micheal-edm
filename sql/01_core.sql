-- Target: MySQL 8.4 LTS. Run once in a fresh isolated database instance.
CREATE DATABASE core;
CREATE DATABASE warehouse;
CREATE DATABASE analytics;
CREATE DATABASE hr;
CREATE TABLE core.customer(
 customer_id varchar(64) PRIMARY KEY,name varchar(200) NOT NULL,phone varchar(16),email varchar(254),
 district varchar(100),consent_marketing boolean NOT NULL DEFAULT false,
 CHECK(phone IS NULL OR REGEXP_LIKE(phone,'^[+]256[37][0-9]{8}$'))
) ENGINE=InnoDB;
CREATE TABLE core.customer_xref(
 source varchar(32),source_id varchar(64),customer_id varchar(64) NOT NULL,
 verified_at datetime(6),PRIMARY KEY(source,source_id),
 FOREIGN KEY(customer_id) REFERENCES core.customer(customer_id));
CREATE TABLE core.product(
 product_id varchar(64) PRIMARY KEY,name varchar(200) NOT NULL,category varchar(100) NOT NULL,
 subcategory varchar(100),unit varchar(10) NOT NULL CHECK(unit IN ('kg','g','l','ml','each')));
CREATE TABLE core.supplier(supplier_id varchar(64) PRIMARY KEY,name varchar(200) NOT NULL);
CREATE TABLE core.product_supplier(
 product_id varchar(64),supplier_id varchar(64),supplier_sku varchar(64) NOT NULL,
 PRIMARY KEY(product_id,supplier_id),UNIQUE(supplier_id,supplier_sku),
 FOREIGN KEY(product_id) REFERENCES core.product(product_id),FOREIGN KEY(supplier_id) REFERENCES core.supplier(supplier_id));
CREATE TABLE core.store(store_id varchar(64) PRIMARY KEY,name varchar(200) NOT NULL,district varchar(100) NOT NULL);
CREATE TABLE core.orders(
 order_id varchar(64) PRIMARY KEY,source varchar(32) NOT NULL,source_order_id varchar(64) NOT NULL,
 customer_id varchar(64),store_id varchar(64) NOT NULL,ordered_at datetime(6) NOT NULL,
 currency char(3) NOT NULL CHECK(currency IN ('UGX','KES','RWF')),UNIQUE(source,source_order_id),
 FOREIGN KEY(customer_id) REFERENCES core.customer(customer_id),FOREIGN KEY(store_id) REFERENCES core.store(store_id));
CREATE TABLE core.order_line(
 order_id varchar(64),line_no int CHECK(line_no>0),product_id varchar(64) NOT NULL,
 quantity decimal(14,3) NOT NULL CHECK(quantity<>0),unit_price decimal(18,2) NOT NULL CHECK(unit_price>=0),
 return_of_order_id varchar(64),return_of_line_no int,PRIMARY KEY(order_id,line_no),
 FOREIGN KEY(order_id) REFERENCES core.orders(order_id),FOREIGN KEY(product_id) REFERENCES core.product(product_id),
 FOREIGN KEY(return_of_order_id,return_of_line_no) REFERENCES core.order_line(order_id,line_no),
 CHECK((return_of_order_id IS NULL)=(return_of_line_no IS NULL)));
CREATE TABLE core.payment(
 payment_id varchar(64) PRIMARY KEY,order_id varchar(64) NOT NULL,provider varchar(32) NOT NULL,
 provider_ref varchar(128),amount decimal(18,2) NOT NULL,
 status varchar(16) NOT NULL CHECK(status IN ('pending','settled','failed','refunded')),
 FOREIGN KEY(order_id) REFERENCES core.orders(order_id),UNIQUE(provider,provider_ref),
 CHECK(provider='cash' OR status<>'settled' OR provider_ref IS NOT NULL));
-- MySQL permits multiple NULLs in this unique key, supporting cash without a reference.
CREATE TABLE core.loyalty_account(
 account_id varchar(64) PRIMARY KEY,customer_id varchar(64) NOT NULL UNIQUE,
 points_balance decimal(14,2) NOT NULL DEFAULT 0,FOREIGN KEY(customer_id) REFERENCES core.customer(customer_id));
CREATE TABLE core.loyalty_ledger(
 entry_id varchar(64) PRIMARY KEY,account_id varchar(64) NOT NULL,order_id varchar(64),
 points_delta decimal(14,2) NOT NULL,occurred_at datetime(6) NOT NULL,source_event_id varchar(128) NOT NULL UNIQUE,
 FOREIGN KEY(account_id) REFERENCES core.loyalty_account(account_id),FOREIGN KEY(order_id) REFERENCES core.orders(order_id));
CREATE TABLE hr.employee(employee_id varchar(64) PRIMARY KEY,name varchar(200),salary decimal(18,2),bank_account varchar(64));
