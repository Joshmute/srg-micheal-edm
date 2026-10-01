"""Canonical sales transformation with explicit quarantine and replay safety."""
import csv, json, re
from decimal import Decimal, InvalidOperation
from pathlib import Path
from .quality import parse_date, text


def amount(value,currency):
    v=text(value).upper()
    for marker in ('UGX','KES','RWF'):
        if marker in v and marker!=currency: raise ValueError('currency label conflicts with currency field')
    v=re.sub(r'^(UGX|KES|RWF)\s*','',v).replace(',','')
    if not re.fullmatch(r'\d+(\.\d{1,2})?',v): raise ValueError('ambiguous or invalid nonnegative unit price')
    return Decimal(v)


def load_sales(rows,db,products,customers,day_first=False):
    """Validate into an in-memory staging map before MySQL bulk loading.
    The map is keyed by source/order/line and is not a DBMS.
    Amounts remain in original currency; never sum different currencies.
    """
    errors=[]; loaded=replayed=0
    for i,r in enumerate(rows,2):
        try:
            source=text(r['source']);order=text(r['order_id']);sku=text(r['sku']).upper()
            if source not in ('pos','ecommerce','loyalty_app') or not order: raise ValueError('unknown source or missing order')
            if sku not in products: raise ValueError('unresolved product')
            line=int(r['line_no'])
            if line<1: raise ValueError('line number must be positive')
            day=parse_date(r['order_date'],day_first)
            if not day: raise ValueError('invalid or ambiguous date')
            qty=Decimal(r['quantity']);cur=text(r['currency']).upper()
            if not qty.is_finite() or qty==0 or cur not in ('UGX','KES','RWF'): raise ValueError('invalid quantity/currency')
            price=amount(r['unit_price'],cur);cust=text(r.get('customer_id'))
            if cust and cust not in customers: raise ValueError('unresolved customer')
            if not text(r.get('store_id')): raise ValueError('missing store')
            values=(source,order,line,day,cust or None,sku,text(r['store_id']),str(qty),str(price),cur,str(qty*price),int(bool(text(r.get('payment_ref')))))
            existing=db.get(values[:3])
            if existing:
                if tuple(existing)!=values: raise ValueError('conflicting replay; requires source correction version')
                replayed+=1; continue
            db[values[:3]]=values;loaded+=1
        except (ValueError,KeyError,InvalidOperation) as exc:
            errors.append({'row':i,'reason':str(exc)})
    return {'input_rows':len(rows),'loaded':loaded,'replayed':replayed,'quarantined':len(errors),'errors':errors}
