"""Validate canonical sales CSV and emit a MySQL staging import, never raw SQL literals."""
import argparse,json
from pathlib import Path
from collections import Counter
from .pipeline import read_csv,write_csv
from .etl import load_sales

FIELDS=['source','order_id','line_no','order_date','customer_id','sku','store_id','quantity','unit_price','currency','net_amount','payment_ref_present']

def sql_string(value):
    if value is None:return 'NULL'
    # Hex UTF-8 avoids quote/backslash/sql_mode ambiguities from untrusted source fields.
    return "CONVERT(X'"+str(value).encode('utf-8').hex()+"' USING utf8mb4)"

def main():
    p=argparse.ArgumentParser();p.add_argument('--sales',type=Path,required=True);p.add_argument('--products',type=Path,required=True);p.add_argument('--customers',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--day-first',action='store_true');a=p.parse_args()
    products=read_csv(a.products,['sku']);counts=Counter(r['sku'] for r in products)
    if any(n>1 for n in counts.values()):p.error('Resolve conflicting product SKUs before sales loading')
    customers=read_csv(a.customers,['customer_id'])
    rows=read_csv(a.sales,['source','order_id','line_no','order_date','sku','store_id','quantity','unit_price','currency'])
    stage={};result=load_sales(rows,stage,set(counts),{r['customer_id'] for r in customers},a.day_first)
    a.output.mkdir(parents=True,exist_ok=True,mode=0o700)
    write_csv(a.output/'sales_validated.csv',[dict(zip(FIELDS,v)) for v in stage.values()],FIELDS)
    (a.output/'sales_result.json').write_text(json.dumps(result,indent=2)+'\n')
    # Temporary table is per session. Re-run the file in one mysql session to recreate safely.
    statements=['DROP TEMPORARY TABLE IF EXISTS warehouse.stage_sales;',
      '''CREATE TEMPORARY TABLE warehouse.stage_sales(
source varchar(32),order_id varchar(64),line_no int,order_date date,customer_id varchar(64),
sku varchar(64),store_id varchar(64),quantity decimal(14,3),unit_price decimal(18,2),
currency char(3),net_amount decimal(18,2),payment_ref_present boolean,PRIMARY KEY(source,order_id,line_no));''']
    for values in stage.values():statements.append('INSERT INTO warehouse.stage_sales VALUES('+','.join(sql_string(v) for v in values)+');')
    (a.output/'sales_stage.sql').write_text('\n'.join(statements)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
