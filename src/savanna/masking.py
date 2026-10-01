"""Restricted analytics pseudonyms; this is NOT an anonymisation claim."""
import argparse,csv,hashlib,hmac,os
from pathlib import Path

def token(value,key):
    if len(key)<32: raise ValueError('HMAC key must contain at least 32 bytes')
    return hmac.new(key,str(value).encode(),hashlib.sha256).hexdigest()

def mask(row,key):
    return {'customer_token':token(row['customer_id'],key), 'district':row.get('district','')}

def main():
    p=argparse.ArgumentParser();p.add_argument('input',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    key=os.environ.get('SAVANNA_MASKING_KEY','').encode()
    if len(key)<32: p.error('Set SAVANNA_MASKING_KEY to a securely generated secret of at least 32 bytes')
    if a.input.resolve()==a.output.resolve():p.error('Input and output must differ')
    with a.input.open(newline='') as src,a.output.open('w',newline='') as dst:
        w=csv.DictWriter(dst,fieldnames=['customer_token','district']);w.writeheader()
        for row in csv.DictReader(src):w.writerow(mask(row,key))
    os.chmod(a.output,0o600)
if __name__=='__main__':main()
