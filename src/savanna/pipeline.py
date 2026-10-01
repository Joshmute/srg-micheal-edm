"""Run with PYTHONPATH=src python -m savanna.pipeline --help."""
import argparse, csv, hashlib, json, os
from datetime import date
from pathlib import Path
from .quality import profile, clean_customers, clean_products


def read_csv(path, required):
    with path.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        missing=set(required)-set(reader.fieldnames or [])
        if missing: raise ValueError(f'{path.name}: missing canonical headers {sorted(missing)}; map source columns explicitly first')
        return list(reader)


def write_csv(path, rows, fields=None):
    fields=fields or (list(rows[0]) if rows else ['row','field','reason'])
    with path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)


def run(source, output, reference, as_of, day_first=False):
    output.mkdir(parents=True,exist_ok=True,mode=0o700)
    os.chmod(output,0o700)
    districts={r['district'].casefold():r['district'] for r in read_csv(reference/'districts.csv',['district'])}
    categories={r['alias'].casefold():r['canonical'] for r in read_csv(reference/'category_aliases.csv',['alias','canonical'])}
    c=read_csv(source/'SRG_Customers.csv',['customer_id','name','phone','email','district'])
    p=read_csv(source/'SRG_Products.csv',['sku','name','unit','category'])
    cc,ci,cm=clean_customers(c,districts,day_first)
    pp,pi=clean_products(p,categories)
    metrics={}
    for domain, before, after in [('customers',c,cc),('products',p,pp)]:
        metrics[domain]={'before':profile(before,domain,districts,as_of,day_first),'after':profile(after,domain,districts,as_of,day_first)}
        write_csv(output/f'{domain}_clean.csv',after,sorted({k for r in after for k in r}) if after else None)
    write_csv(output/'customer_issues.csv',ci)
    write_csv(output/'product_issues.csv',pi)
    write_csv(output/'match_review.csv',cm,['row_a','row_b','score','action'])
    metrics['provenance']={'as_of':str(as_of),'synthetic':source.name=='synthetic',
        'sources':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(source.glob('*.csv'))},
        'notes':'Candidate duplicates are not verified duplicate persons. Accuracy needs ground truth. Rows with defects remain visible; quarantined sales are counted separately.'}
    (output/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
    flat=[]
    for domain in ('customers','products'):
        for metric,value in metrics[domain]['before'].items():
            if not isinstance(value,(dict,list)):
                flat.append({'domain':domain,'metric':metric,'before':value,'after':metrics[domain]['after'].get(metric)})
    write_csv(output/'before_after.csv',flat)
    return metrics


def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--reference',type=Path,default=Path('data/reference'));p.add_argument('--as-of',type=date.fromisoformat,required=True)
    p.add_argument('--day-first',action='store_true',help='Only use after source owner confirms DD/MM/YYYY.')
    args=p.parse_args()
    if args.input.resolve()==args.output.resolve(): p.error('Input and output must differ')
    print(json.dumps(run(args.input,args.output,args.reference,args.as_of,args.day_first),indent=2))
if __name__=='__main__':main()
