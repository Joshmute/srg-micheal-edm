"""Reproducible synthetic assignment inputs. No instructor or real customer data."""
from pathlib import Path
import csv,json,random,calendar,hashlib
from datetime import date,timedelta,datetime,timezone
R=random.Random(27300); OUT=Path('data/simulation');OUT.mkdir(exist_ok=True)
def write(name,rows):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
D=['Kampala','Jinja','Mbarara','Gulu'];C=['Grocery','Beverages','Household'];truth=[];dirty=[]
for i in range(4100):
 r=dict(customer_id=f'KMB-C{i:05}',name=f'Fictional Member {i:05}',phone=f'+2567{i+50000:08}',email=f'member.kmb{i}@example.invalid',district=D[i%4],dob=f'{1970+i%35}-05-15',gender=['male','female','not_stated'][i%3],updated_at='2026-06-01' if i%5 else '2025-10-01')
 truth.append(r);d=dict(r)
 if i%14==0:d['phone']=''
 elif i%16==0:d['phone']='bad-phone'
 elif i%4==0:d['phone']='0'+r['phone'][4:]
 elif i%4==1:d['phone']=r['phone'][1:]
 elif i%4==2:d['phone']='00'+r['phone'][1:]
 if i%14==0:d['email']=''
 elif i%21==0:d['email']='bad-email'
 if i%25==0:d['district']='Invalid District'
 elif i%3==0:d['district']=r['district'].lower()
 if i%29==0:d['name']=''
 elif i%4==0:d['name']='  '+r['name']+'  '
 if i%7==0:d['updated_at']='01/06/2026' if i%5 else '01/10/2025'
 elif i%3==0:d['updated_at']=r['updated_at'].replace('-','/')
 d['gender']={'male':'M','female':'F','not_stated':'prefer not to say'}[r['gender']]
 dirty.append(d)
# 900 exact repeated source records: 18% excess rows by generator identity.
dirty += [dict(dirty[i]) for i in range(900)]
write('SRG_Customers.csv',dirty);write('customer_truth.csv',truth)
# Simulated verification source supports enrichment for specific missing/invalid attributes.
write('verified_contact_updates.csv',[{**r,'verified_at':'2026-06-28','provenance':'SIMULATED customer confirmation'} for i,r in enumerate(truth) if i%14==0 or i%16==0 or i%21==0 or i%25==0 or i%29==0])
products=[];pdirty=[]
for i in range(1140):
 r=dict(sku=f'KMB-P{i:04}',name=f'Sample Item {i:04}',unit=['kg','l','each'][i%3],category=C[i%3],updated_at='2026-06-01');products.append(r);d=dict(r)
 d['unit']=['KGS','litres','pcs'][i%3]
 if i%7==0:d['category']={'Grocery':'grocry','Beverages':'bevrages','Household':'Household'}[r['category']]
 if i%9==0:d['sku']=r['sku'].lower()
 pdirty.append(d)
pdirty += [dict(pdirty[i]) for i in range(60)]
write('SRG_Products.csv',pdirty);write('product_truth.csv',products)
stores=[dict(store_id=f'KMB-S{i+1:02}',name=f'{D[i%4]} Branch {i+1:02}',district=D[i%4]) for i in range(23)]
write('SRG_Stores.csv',stores)
write('SRG_Suppliers.csv',[dict(supplier_id=f'KMB-SUP{i:03}',name=f'Fictional Vendor {i:03}',email=f'vendor.kmb{i}@example.invalid',country='Uganda') for i in range(80)])
write('SRG_Loyalty.csv',[dict(account_id=f'KMB-L{i:05}',customer_id=r['customer_id'],opening_points=0,marketing_consent=i%4!=0,consent_source='SIMULATED enrolment',consent_at='2026-01-01') for i,r in enumerate(truth)])
write('SRG_CRM.csv',[dict(customer_id=r['customer_id'],segment=['Occasional','Routine','Frequent'][i%3],marketing_consent=i%4!=0,preference_updated_at='2026-06-01') for i,r in enumerate(truth)])
write('SRG_HR.csv',[dict(employee_id=f'KMB-E{i:03}',name=f'Fictional Staff {i:03}',salary_ugx=650000+i*30000,bank_account=f'NOT-REAL-BANK-{i:03}',national_id=f'NOT-REAL-NIN-{i:03}',health_note='SIMULATED confidential field',next_of_kin_phone=f'NOT-REAL-CONTACT-{i:03}') for i in range(46)])
sales=[];payments=[];canonical=[];counts=[11000,10500,8500,9000,12500,8500];index=0
for month,count in zip(range(1,7),counts):
 for k in range(count):
  index+=1;source=['pos','ecommerce','loyalty_app'][index%3];customer=truth[R.randrange(4100 if month<4 else 3500)];product=products[R.randrange(1140)];store=stores[R.randrange(23)]
  day=date(2026,month,1)+timedelta(days=R.randrange(calendar.monthrange(2026,month)[1]))
  qty=-R.randint(1,3) if R.random()<0.065 else R.randint(1,5);price=(800+int(product['sku'][-4:])%60*300);currency='UGX' if index%40 else ('KES' if index%80 else 'RWF')
  if currency=='KES':price=max(50,price//30)
  if currency=='RWF':price=price//3
  provider=['cash','MTN','Airtel'][index%3];ref='' if provider=='cash' or index%83==0 else f'KMB-REF-{index:06}'
  native_date=day.strftime('%d/%m/%Y') if source=='pos' else day.isoformat() if source=='ecommerce' else day.strftime('%d-%b-%Y')
  notation=f'{currency} {price:,}' if source=='pos' else str(price) if source=='ecommerce' else f'{price:,.2f}'
  row=dict(source=source,order_id=f'KMB-O{index:06}',line_no=1,order_date=native_date,customer_id='' if index%37==0 else customer['customer_id'],sku=product['sku'].lower() if source=='pos' else product['sku'],store_id=store['store_id'],quantity=qty,unit_price=notation,currency=currency,payment_ref=ref)
  sales.append(row);canonical.append({**row,'order_date':day.isoformat(),'sku':product['sku'],'unit_price':price})
  if provider!='cash':payments.append(dict(provider=provider,provider_ref=ref or f'KMB-UNLINKED-{index}',order_id=row['order_id'],store_id=store['store_id'],occurred_at=day.isoformat(),amount=qty*price,currency=currency,status='refunded' if qty<0 else 'settled'))
write('SRG_Sales.csv',sales);write('sales_truth.csv',canonical);write('SRG_MobileMoney.csv',payments)
inventory=[]
for store in stores:
 for product in products[:120]:
  book=R.randint(0,120);physical=max(0,book+R.choice([0,0,0,-1,-2,2,-5]))
  inventory.append(dict(snapshot_at='2026-06-30T20:00:00Z',store_id=store['store_id'],sku=product['sku'],on_hand=book,physical_count=physical,unit=product['unit'],source='SIMULATED Odoo'))
write('SRG_Inventory.csv',inventory)
events=[dict(event_id=f'KMB-F{i:05}',store_id=stores[i%23]['store_id'],device_id=f'KMB-D{i%23:02}',event_time_utc=f'2026-06-29T{8+i//60%10:02}:{i%60:02}:00Z',count_delta=1,sequence=i,schema_version=1) for i in range(720)]
events+=events[:8];(OUT/'footfall_stream_sample.json').write_text(json.dumps(events,indent=2))
(OUT/'etl_error_log.txt').write_text('SIMULATED FAILURE FIXTURE - not an instructor log\n2026-06-29T00:01:02Z ERROR batch=KMB-042 source=pos row=3 date=03/04/2026 conversion failed: ISO date expected\n2026-06-29T00:01:03Z ERROR batch=KMB-042 row=4 sku=kmb-p0001 lookup failed: case-sensitive dictionary\n2026-06-29T00:01:04Z ERROR retry=1 batch=KMB-042 duplicate business key source/order/line; previous rows were committed\n')
manifest={'classification':'SYNTHETIC ASSIGNMENT SIMULATION - not actual SRG observations','seed':27300,'counts':{'customer_rows':len(dirty),'distinct_customer_ids':4100,'product_rows':len(pdirty),'distinct_skus':1140,'sales_rows':len(sales)},'period':'2026-01-01 to 2026-06-30','generated_by':'scripts/generate_simulation.py','files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.suffix in ('.csv','.json','.txt') and p.name!='manifest.json'}}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest['counts']))
