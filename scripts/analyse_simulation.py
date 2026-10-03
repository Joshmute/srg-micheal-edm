"""Execute the capstone on explicitly synthetic, reproducible inputs."""
from pathlib import Path
from datetime import date,datetime
from collections import defaultdict,Counter
from decimal import Decimal
import sys,csv,json,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from savanna.pipeline import read_csv,write_csv
from savanna.quality import profile,clean_customers,clean_products,phone,email,text,percent,parse_date
from savanna.etl import load_sales
from savanna.masking import mask
from savanna.sales_cli import FIELDS,sql_string
S=Path('data/simulation');O=Path('evidence/simulation');O.mkdir(exist_ok=True)
read=lambda name:read_csv(S/name,[])
districts={s.casefold():s for s in ['Kampala','Jinja','Mbarara','Gulu']};categories={'grocry':'Grocery','grocery':'Grocery','bevrages':'Beverages','beverages':'Beverages','household':'Household'}
customers=read('SRG_Customers.csv');products=read('SRG_Products.csv');cc,issues,candidates=clean_customers(customers,districts,True);pp,pissues=clean_products(products,categories)
updates={r['customer_id']:r for r in read('verified_contact_updates.csv')};enrich=[]
for r in cc:
 if r['customer_id'] in updates:
  for field in ('name','phone','email','district'):
   if not r[field]:
    r[field]=updates[r['customer_id']][field];enrich.append({'customer_id':r['customer_id'],'field':field,'source':'SIMULATED verified_contact_updates.csv'})
# Ground truth is used for evaluation only, not blanket overwrite.
ct={r['customer_id']:r for r in read('customer_truth.csv')};pt={r['sku']:r for r in read('product_truth.csv')}
def accuracy(rows,domain):
 fields=('name','phone','email','district') if domain=='customers' else ('name','unit','category')
 truth=ct if domain=='customers' else pt;key='customer_id' if domain=='customers' else 'sku'
 good=total=0
 for r in rows:
  k=r[key] if domain=='customers' else r[key].upper()
  for f in fields:
   total+=1;value=text(r.get(f))
   if f=='phone':value=phone(value)
   elif f=='email':value=email(value)
   elif f in ('district','category'):value=value.casefold()
   elif f=='unit':value={'kgs':'kg','kilograms':'kg','litres':'l','pcs':'each'}.get(value.lower(),value)
   expected=truth[k][f].casefold() if f in ('district','category') else truth[k][f]
   good+=value==expected
 return {'accuracy_pct':percent(good,total),'accuracy_checked_values':total,'accuracy_correct_values':good,'accuracy_note':'Agreement with generator truth on all specified values; not independently verified real-world accuracy.'}
metrics={}
for domain,before,after in [('customers',customers,cc),('products',products,pp)]:
 metrics[domain]={stage:{**profile(rows,domain,districts,date(2026,6,30),True),**accuracy(rows,domain)} for stage,rows in [('before',before),('after',after)]}
write_csv(O/'customers_clean.csv',cc);write_csv(O/'products_clean.csv',pp);write_csv(O/'enrichment_audit.csv',enrich);write_csv(O/'customer_issues.csv',issues);write_csv(O/'product_issues.csv',pissues);write_csv(O/'match_review.csv',candidates,['row_a','row_b','score','action'])
key=b'SYNTHETIC-ONLY-MASKING-KEY-NOT-FOR-PRODUCTION'
write_csv(O/'customers_masked.csv',[mask(r,key) for r in cc])
rows=[]
for r in read('SRG_Sales.csv'):
 day=parse_date(r['order_date'],day_first=r['source']=='pos')
 if not day:raise ValueError('Source date contract failed')
 rows.append({**r,'order_date':day,'sku':r['sku'].upper()})
stage={};result=load_sales(rows,stage,{r['sku'] for r in pp},{r['customer_id'] for r in cc})
assert result['loaded']==60000 and not result['quarantined'],result
replay=load_sales(rows,stage,{r['sku'] for r in pp},{r['customer_id'] for r in cc});assert replay['replayed']==60000
validated=[dict(zip(FIELDS,v)) for v in stage.values()];write_csv(O/'sales_validated.csv',validated)
# Publish only simulation fields; no raw phone/email/HR attributes.
stores={r['store_id']:r for r in read('SRG_Stores.csv')};pr={r['sku']:r for r in pp};crm={r['customer_id']:r for r in read('SRG_CRM.csv')}
board=[];monthly=defaultdict(lambda:{'net':Decimal(0),'buyers':set(),'rows':0});total=defaultdict(Decimal);missing=defaultdict(lambda:{'count':0,'value':Decimal(0)})
for r in validated:
 customer=r['customer_id'];positive=Decimal(r['quantity'])>0;month=r['order_date'][:7];source=r['source'];product=pr[r['sku']];store=stores[r['store_id']];net=Decimal(r['net_amount']);currency=r['currency'];total[currency]+=net
 m=monthly[(month,currency)];m['net']+=net;m['rows']+=1
 if customer and positive:m['buyers'].add(customer)
 if source!='pos' and not r['payment_ref_present']:
  missing[currency]['count']+=1;missing[currency]['value']+=net
 board.append({'Month':month+'-01','Order Date':r['order_date'],'District':store['district'],'Store':store['name'],'Store ID':r['store_id'],'Category':product['category'],'Product':product['name'],'Channel':source,'Currency':currency,'Net Sales':str(net),'Net Units':r['quantity'],'Order ID':r['order_id'],'Customer ID':customer or '', 'Active Buyer':customer if positive and customer else '', 'Segment':crm[customer]['segment'] if customer else 'Anonymous','Unmatched Payment Value':str(net) if source!='pos' and not r['payment_ref_present'] else '0','Simulation':'SYNTHETIC - not actual SRG observations'})
write_csv(Path('dashboard/micheal_simulated_sales.csv'),board)
write_csv(Path('dashboard/micheal_ugx_dashboard.csv'),[r for r in board if r['Currency']=='UGX'])
monthrows=[{'month':mo,'currency':cu,'net_sales':str(v['net']),'active_customers':len(v['buyers']),'rows':v['rows']} for (mo,cu),v in sorted(monthly.items())];write_csv(O/'monthly_kpis.csv',monthrows)
# Cohort metric requires a full 90-day lookback; use fixed date, never current runtime date.
purchase_dates=defaultdict(list)
for r in validated:
 if r['customer_id'] and Decimal(r['quantity'])>0:purchase_dates[r['customer_id']].append(date.fromisoformat(r['order_date']))
asof=date(2026,7,1);eligible=[k for k,v in purchase_dates.items() if min(v)<date(2026,4,2)];inactive=[k for k in eligible if (asof-max(purchase_dates[k])).days>=90]
events=json.loads((S/'footfall_stream_sample.json').read_text());unique={e['event_id']:e for e in events}
hr=read('SRG_HR.csv');hr_inventory=[{'field':field,'classification':'Restricted','reason':reason} for field,reason in [('name','Direct identifier'),('salary_ugx','Personal financial information'),('bank_account','Banking information'),('national_id','Government identifier'),('health_note','Health information'),('next_of_kin_phone','Third-party contact')]];write_csv(O/'hr_classification.csv',hr_inventory)
summary={'simulation':True,'seed':27300,'sales':result,'replay':replay,'net_sales_by_currency':{k:str(v) for k,v in total.items()},'monthly':monthrows,'unmatched_electronic':{k:{'count':v['count'],'net_value':str(v['value'])} for k,v in missing.items()},'inactivity':{'as_of':str(asof),'eligible_members':len(eligible),'inactive_90_days':len(inactive),'inactive_pct':percent(len(inactive),len(eligible))},'footfall':{'input_events':len(events),'unique_events':len(unique),'duplicate_events':len(events)-len(unique)},'enriched_attributes':len(enrich),'returned_lines':sum(Decimal(r['quantity'])<0 for r in validated),'rows':{'customer_input':5000,'customer_output':len(cc),'product_input':1200,'product_output':len(pp)},'metrics':metrics}
(O/'results.json').write_text(json.dumps(summary,indent=2)+'\n')
flat=[{'domain':d,'metric':m,'before':metrics[d]['before'].get(m),'after':metrics[d]['after'].get(m)} for d in metrics for m in metrics[d]['before'] if not isinstance(metrics[d]['before'][m],dict)];write_csv(O/'before_after.csv',flat)
# Build one runnable MySQL script using safely encoded literals and batched inserts.
def insert(table,columns,rows):
 output=[]
 for i in range(0,len(rows),500):output.append(f'INSERT INTO {table} ({columns}) VALUES\n'+',\n'.join('('+','.join(sql_string(v) for v in r)+')' for r in rows[i:i+500])+';')
 return '\n'.join(output)+'\n'
sql=[]
sql.append(insert('warehouse.dim_customer','customer_token,segment',[(hashlib.sha256(('KMB-'+r['customer_id']).encode()).hexdigest(),crm[r['customer_id']]['segment']) for r in cc]))
sql.append(insert('warehouse.customer_source_map','source_customer_id,customer_key',[(r['customer_id'],i+1) for i,r in enumerate(cc)]))
sql.append(insert('warehouse.dim_product','product_id,name,category,unit,valid_from',[(r['sku'],r['name'],r['category'],r['unit'],'2026-01-01') for r in pp]))
sql.append(insert('warehouse.dim_store','store_id,district,valid_from',[(r['store_id'],r['district'],'2026-01-01') for r in stores.values()]))
sql.append('CREATE TEMPORARY TABLE warehouse.stage_sales(source varchar(32),order_id varchar(64),line_no int,order_date date,customer_id varchar(64),sku varchar(64),store_id varchar(64),quantity decimal(14,3),unit_price decimal(18,2),currency char(3),net_amount decimal(18,2),payment_ref_present boolean,PRIMARY KEY(source,order_id,line_no));')
sql.append(insert('warehouse.stage_sales',','.join(FIELDS),list(stage.values())))
sql+=['CALL warehouse.load_staged_sales();','CALL warehouse.load_staged_sales();',"SELECT COUNT(*) AS loaded_facts FROM warehouse.fact_sales;",'SELECT currency,SUM(net_amount) AS net_sales,COUNT(*) AS rows_loaded FROM warehouse.fact_sales GROUP BY currency;']
(O/'load_simulation.sql').write_text('\n'.join(sql))
print(json.dumps({k:v for k,v in summary.items() if k not in ('metrics','monthly')},indent=2))
