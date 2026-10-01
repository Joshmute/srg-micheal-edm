"""Conservative cleansing: preserve uncertainty instead of inventing values."""
import re
from collections import Counter
from datetime import datetime, date
from difflib import SequenceMatcher


def text(value):
    return ' '.join(str(value or '').strip().split())


def phone(value):
    raw = re.sub(r'[\s().-]', '', text(value))
    if raw.startswith('00'): raw = '+' + raw[2:]
    if re.fullmatch(r'0[37]\d{8}', raw): raw = '+256' + raw[1:]
    if re.fullmatch(r'256[37]\d{8}', raw): raw = '+' + raw
    # Uganda phone syntax only; this does not verify ownership or active service.
    return raw if re.fullmatch(r'\+256[37]\d{8}', raw) else ''


def phone_variant(value):
    v = text(value)
    if not v: return 'missing'
    if v.startswith('+256'): return 'international_plus'
    if v.startswith('00256'): return 'international_00'
    if v.startswith('256'): return 'international_bare'
    if v.startswith('0'): return 'national'
    return 'other'


def parse_date(value, day_first=False):
    v = text(value)
    if not v: return ''
    formats = ['%Y-%m-%d', '%Y/%m/%d', '%d-%b-%Y']
    if day_first: formats += ['%d/%m/%Y']
    for fmt in formats:
        try: return datetime.strptime(v, fmt).date().isoformat()
        except ValueError: pass
    return ''  # Ambiguous slash dates need an approved source contract.


def date_variant(value):
    v = text(value)
    if not v: return 'missing'
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', v): return 'iso'
    if re.fullmatch(r'\d{4}/\d{2}/\d{2}', v): return 'year_first_slash'
    if re.fullmatch(r'\d{1,2}/\d{1,2}/\d{4}', v): return 'ambiguous_slash'
    if re.fullmatch(r'\d{1,2}-[A-Za-z]{3}-\d{4}', v): return 'named_month'
    return 'other'


def email(value):
    v = text(value).lower()
    return v if re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', v) else ''


def match_score(a, b):
    """Heuristic 0-100, NOT a calibrated probability. Never enough to auto-merge."""
    name_a, name_b = text(a.get('name')).casefold(), text(b.get('name')).casefold()
    name = SequenceMatcher(None, name_a, name_b).ratio() if name_a and name_b else 0
    p, e, d = phone(a.get('phone')), email(a.get('email')), text(a.get('district')).casefold()
    return round(40 * bool(p and p == phone(b.get('phone'))) +
                 25 * bool(e and e == email(b.get('email'))) + 25 * name +
                 10 * bool(d and d == text(b.get('district')).casefold()), 2)


def person_key(row):
    # No phone-only merging: family phones and recycled SIMs make it unsafe.
    p, e, n = phone(row.get('phone')), email(row.get('email')), text(row.get('name')).casefold()
    return (n, p, e) if n and p and e else None


def percent(n, d):
    return round(100*n/d, 2) if d else None


def profile(rows, domain, districts, as_of, day_first=False):
    n = len(rows)
    result = {'rows': n, 'accuracy_pct': None,
              'accuracy_note': 'Not measured: requires independently verified sample.',
              'timeliness_note': 'Freshness uses updated_at <=90 days; missing/invalid timestamps are unassessable.'}
    dates = [(parse_date(r.get('updated_at'), day_first), r) for r in rows]
    valid_dates = [date.fromisoformat(d) for d,r in dates if d and date.fromisoformat(d) <= as_of]
    result['timeliness_assessable_rows'] = len(valid_dates)
    result['timeliness_pct'] = percent(sum(0 <= (as_of-d).days <= 90 for d in valid_dates), len(valid_dates))
    result['date_format_counts'] = dict(Counter(date_variant(r.get('updated_at')) for r in rows))
    if domain == 'customers':
        keys = [person_key(r) for r in rows]
        counts = Counter(k for k in keys if k)
        excess = sum(c-1 for c in counts.values())
        result.update({
            'candidate_duplicate_excess_rows': excess,
            'candidate_duplicate_pct': percent(excess,n),
            'uniqueness_pct': percent(n-excess,n),
            'identity_assessable_rows': sum(bool(k) for k in keys),
            'missing_contact_pct': percent(sum(not text(r.get('phone')) and not text(r.get('email')) for r in rows),n),
            'completeness_pct': percent(sum(bool(text(r.get('name'))) and bool(text(r.get('phone')) or text(r.get('email'))) for r in rows),n),
            'phone_format_counts': dict(Counter(phone_variant(r.get('phone')) for r in rows)),
            'validity_pct': percent(sum(bool(phone(r.get('phone'))) and text(r.get('district')).casefold() in districts for r in rows),n),
            'invalid_district_rows': sum(text(r.get('district')).casefold() not in districts for r in rows),
            'consistency_pct': percent(sum(bool(phone(r.get('phone'))) and text(r.get('phone')) == phone(r.get('phone')) for r in rows),n)
        })
    else:
        skus = [text(r.get('sku')).upper() for r in rows]
        excess = sum(c-1 for k,c in Counter(skus).items() if k)
        result.update({'duplicate_sku_excess_rows':excess, 'uniqueness_pct':percent(n-excess,n),
            'completeness_pct': percent(sum(all(text(r.get(k)) for k in ('sku','name','unit','category')) for r in rows),n),
            'consistency_pct': percent(sum(text(r.get('unit')) in ('kg','g','l','ml','each') for r in rows),n),
            'validity_pct': percent(sum(bool(re.fullmatch(r'[A-Z0-9][A-Z0-9_-]*',text(r.get('sku')))) and text(r.get('unit')) in ('kg','g','l','ml','each') for r in rows),n)})
    return result


def clean_customers(rows, districts, day_first=False):
    clean, issues, candidates = [], [], []
    seen = {}
    for i, row in enumerate(rows, 2):
        r = dict(row)
        r['name'] = text(r.get('name'))
        for field, fn in [('phone', phone), ('email', email)]:
            old = text(r.get(field)); r[field] = fn(old)
            if old and not r[field]: issues.append({'row':i,'field':field,'reason':'invalid; original retained only in restricted raw zone'})
        district = text(r.get('district')).casefold()
        r['district'] = districts.get(district, '')
        if not r['district']: issues.append({'row':i,'field':'district','reason':'unrecognised; needs steward review'})
        for field in ('dob','updated_at'):
            old = text(r.get(field)); r[field] = parse_date(old,day_first)
            if old and not r[field]: issues.append({'row':i,'field':field,'reason':'invalid or ambiguous date'})
        g = text(r.get('gender')).casefold()
        r['gender'] = {'m':'male','male':'male','f':'female','female':'female','other':'other','prefer not to say':'not_stated'}.get(g,'not_stated')
        key = person_key(r)
        if key and key in seen:
            candidates.append({'row_a':seen[key], 'row_b':i, 'score':100, 'action':'review; no identity merge without verification'})
        elif key: seen[key]=i
        clean.append(r)
    # Only remove byte-equivalent normalized duplicate records with the same source ID.
    distinct = []; signatures = set()
    for r in clean:
        signature = tuple(sorted(r.items()))
        if not r.get('customer_id') or signature not in signatures: distinct.append(r)
        signatures.add(signature)
    return distinct, issues, candidates


def clean_products(rows, category_map):
    clean, issues, seen = [], [], {}
    units={'kgs':'kg','kilograms':'kg','kg':'kg','grams':'g','g':'g','litres':'l','liters':'l','l':'l','ml':'ml','pcs':'each','each':'each'}
    for i,row in enumerate(rows,2):
        r=dict(row); r['sku']=text(r.get('sku')).upper(); r['name']=text(r.get('name'))
        r['unit']=units.get(text(r.get('unit')).casefold(),'')
        r['category']=category_map.get(text(r.get('category')).casefold(),text(r.get('category')))
        if not r['sku'] or not r['unit']: issues.append({'row':i,'field':'sku/unit','reason':'missing or unknown; no inferred pack-size conversion'})
        if r['sku'] in seen:
            if r==seen[r['sku']]: continue
            issues.append({'row':i,'field':'sku','reason':'conflicting SKU; retain and quarantine from warehouse lookup'})
        seen[r['sku']]=r; clean.append(r)
    return clean,issues
