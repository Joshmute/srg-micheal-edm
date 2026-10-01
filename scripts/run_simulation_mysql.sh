#!/bin/sh
set -eu
container="savanna-full-simulation-$$"
cleanup() { docker rm -f "$container" >/dev/null 2>&1 || true; }
trap cleanup EXIT INT TERM
docker run -d --name "$container" --network none -e MYSQL_ALLOW_EMPTY_PASSWORD=yes mysql:8.4 >/dev/null
attempt=0
until docker logs "$container" 2>&1 | rg -q 'MySQL init process done'; do
 attempt=$((attempt+1)); [ "$attempt" -lt 120 ] || exit 1; sleep 1
done
attempt=0
until docker exec "$container" mysql -uroot -e 'SELECT 1' >/dev/null 2>&1; do
 attempt=$((attempt+1)); [ "$attempt" -lt 90 ] || exit 1; sleep 1
done
for script in sql/01_core.sql sql/02_warehouse.sql sql/03_scd2.sql sql/04_rbac.sql sql/07_load_sales.sql; do
 docker exec -i "$container" mysql -uroot < "$script"
done
docker exec -i "$container" mysql -uroot < evidence/simulation/load_simulation.sql
docker exec "$container" mysql -uroot --batch -e 'SELECT currency,SUM(net_amount) AS net_sales,COUNT(*) AS loaded_rows FROM warehouse.fact_sales GROUP BY currency;' > evidence/simulation/mysql_totals.tsv
python3 - <<'PY'
import csv,json
from decimal import Decimal
r=json.load(open('evidence/simulation/results.json'));actual=list(csv.DictReader(open('evidence/simulation/mysql_totals.tsv'),delimiter='\t'))
assert sum(int(x['loaded_rows']) for x in actual)==60000
for x in actual:assert Decimal(x['net_sales'])==Decimal(r['net_sales_by_currency'][x['currency']])
print('PASS: 60,000 facts remain after two loads; every currency total matches independent Python Decimal aggregation.')
PY
docker exec "$container" mysql -uroot --batch -e "SELECT DATE_FORMAT(date_key,'%Y-%m-01') AS Month,s.district AS District,p.category AS Category,f.source AS Channel,f.currency AS Currency,SUM(f.net_amount) AS NetSales,SUM(f.quantity) AS NetUnits,COUNT(DISTINCT CASE WHEN f.quantity>0 THEN f.customer_key END) AS ActiveCustomers FROM warehouse.fact_sales f JOIN warehouse.dim_store s USING(store_key) JOIN warehouse.dim_product p USING(product_key) GROUP BY 1,2,3,4,5;" > evidence/simulation/mysql_board_aggregates.tsv
