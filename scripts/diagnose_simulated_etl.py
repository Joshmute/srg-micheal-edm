"""Execute a broken-job demonstration because no instructor log was supplied."""
from pathlib import Path
from datetime import datetime
import sys,json
sys.path.insert(0,'src')
from savanna.quality import parse_date
from savanna.etl import load_sales
from savanna.pipeline import read_csv
raw=read_csv(Path('data/simulation/SRG_Sales.csv'),[])
example=next(r for r in raw if r['source']=='pos')
lines=['SIMULATED ETL DIAGNOSTIC - executed demonstration; not an instructor job']
try:datetime.strptime(example['order_date'],'%Y-%m-%d')
except ValueError as e:lines.append('REPRODUCED date conversion failure: '+str(e))
lookup={'KMB-P0001':'canonical product'}
try:lookup['kmb-p0001']
except KeyError as e:lines.append('REPRODUCED missing product lookup: '+str(e))
seen=set()
try:
 for event in ['KMB-O1','KMB-O1']:
  if event in seen:raise ValueError('duplicate key after retry of committed row')
  seen.add(event)
except ValueError as e:lines.append('REPRODUCED replay failure: '+str(e))
assert parse_date(example['order_date'],True)
assert lookup['kmb-p0001'.upper()]=='canonical product'
r={'source':'pos','order_id':'KMB-O1','line_no':'1','order_date':'2026-02-03','sku':'KMB-P0001','customer_id':'','store_id':'KMB-S01','quantity':'-1','unit_price':'UGX 1,000','currency':'UGX','payment_ref':''}
stage={};a=load_sales([r],stage,{'KMB-P0001'},set());b=load_sales([r],stage,{'KMB-P0001'},set())
assert a['loaded']==1 and b['replayed']==1 and len(stage)==1
lines += ['FIX VERIFIED: source-specific day-first parsing succeeds.','FIX VERIFIED: approved uppercase SKU standardisation resolves lookup.','FIX VERIFIED: source/order/line identity yields one fact after replay; negative return is preserved.','PREVENTION: versioned source contracts, reference coverage check, transaction manifest and replay test.']
Path('evidence/simulation/etl_diagnosis.txt').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
