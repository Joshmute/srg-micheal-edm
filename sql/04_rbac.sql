CREATE ROLE 'srg_analyst','srg_steward','srg_etl','srg_hr';
GRANT SELECT ON analytics.monthly_sales TO 'srg_analyst';
GRANT SELECT ON core.customer TO 'srg_steward';
GRANT SELECT ON core.customer_xref TO 'srg_steward';
GRANT SELECT ON core.product TO 'srg_steward';
GRANT UPDATE(name,phone,email,district) ON core.customer TO 'srg_steward';
GRANT SELECT ON core.* TO 'srg_etl';
GRANT SELECT ON warehouse.* TO 'srg_etl';
GRANT INSERT,UPDATE ON warehouse.fact_sales TO 'srg_etl';
GRANT INSERT,UPDATE ON warehouse.fact_payment TO 'srg_etl';
GRANT INSERT,UPDATE ON warehouse.fact_inventory_snapshot TO 'srg_etl';
GRANT INSERT,UPDATE ON warehouse.dim_date TO 'srg_etl';
GRANT INSERT,UPDATE ON warehouse.dim_customer TO 'srg_etl';
GRANT EXECUTE ON PROCEDURE warehouse.apply_product TO 'srg_etl';
GRANT EXECUTE ON PROCEDURE warehouse.apply_store TO 'srg_etl';
GRANT SELECT,INSERT,UPDATE ON hr.employee TO 'srg_hr';
-- Explicit revocation example: a withdrawn emergency read grant.
GRANT SELECT ON core.customer TO 'srg_analyst';
REVOKE SELECT ON core.customer FROM 'srg_analyst';
-- Fresh roles have no other permissions. MySQL does not use PostgreSQL's PUBLIC role.
-- Individual logins receive a role and SET DEFAULT ROLE. No role receives GRANT OPTION.
