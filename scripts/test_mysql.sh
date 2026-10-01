#!/bin/sh
set -eu
container="savanna-mysql-test-$$"
cleanup() { docker rm -f "$container" >/dev/null 2>&1 || true; }
trap cleanup EXIT INT TERM
docker run -d --name "$container" --network none -e MYSQL_ALLOW_EMPTY_PASSWORD=yes mysql:8.4 >/dev/null
attempt=0
until docker logs "$container" 2>&1 | rg -q 'MySQL init process done'; do
 attempt=$((attempt+1)); [ "$attempt" -lt 120 ] || exit 1
 sleep 1
done
attempt=0
until docker exec "$container" mysql -uroot -e 'SELECT 1' >/dev/null 2>&1; do
 attempt=$((attempt+1)); [ "$attempt" -lt 90 ] || exit 1
 sleep 1
done
docker exec "$container" mysql -uroot -e 'SELECT VERSION() AS mysql_version;'
for script in sql/01_core.sql sql/02_warehouse.sql sql/03_scd2.sql sql/04_rbac.sql sql/05_verify.sql; do
 docker exec -i "$container" mysql -uroot --show-warnings < "$script"
done
# Positive access must succeed before negative tests are meaningful.
docker exec "$container" mysql -udemo_analyst -e 'SELECT CURRENT_ROLE(); SELECT * FROM analytics.monthly_sales;'
docker exec "$container" mysql -udemo_steward -e "UPDATE core.customer SET district='Gulu' WHERE customer_id='DEMO1';"
expect_denied() {
 user="$1"; query="$2"
 set +e
 result=$(docker exec "$container" mysql "-u$user" -e "$query" 2>&1)
 code=$?
 set -e
 if [ "$code" -eq 0 ]; then echo 'FAIL: forbidden query succeeded'; exit 1; fi
 case "$result" in
  *'ERROR 1142'*|*'ERROR 1143'*) echo "$result"; echo "PASS: $user forbidden operation denied";;
  *) echo "$result"; echo 'FAIL: query failed for an unexpected reason'; exit 1;;
 esac
}
expect_denied demo_analyst 'SELECT * FROM core.customer;'
expect_denied demo_analyst 'SELECT * FROM hr.employee;'
expect_denied demo_analyst 'DELETE FROM warehouse.fact_sales;'
expect_denied demo_steward 'UPDATE core.customer SET consent_marketing=true;'
expect_denied demo_etl "UPDATE warehouse.dim_product SET valid_to=NULL;"
docker exec "$container" mysql -udemo_etl -e "CALL warehouse.apply_product('P2','Tea','Grocery','kg','2026-01-01');"
# Invalid temporal update must fail with the designed exception.
set +e
late=$(docker exec "$container" mysql -udemo_etl -e "CALL warehouse.apply_product('P1','Rice','Changed','kg','2025-01-01');" 2>&1)
code=$?
set -e
case "$code:$late" in
  *'ERROR 1644 (45000)'*) echo "$late"; echo 'PASS: late history rejected';;
  *) echo "$late"; echo 'FAIL: expected controlled history rejection'; exit 1;;
esac
# Stage CSV-derived SQL and load in one session; a temporary table cannot cross sessions.
{ cat evidence/synthetic/sales_stage.sql sql/07_load_sales.sql sql/08_demo_load.sql; } | docker exec -i "$container" mysql -uroot --show-warnings
echo 'PASS: all MySQL integration, ETL and privilege tests' 
