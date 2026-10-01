import unittest,tempfile
from datetime import date
from pathlib import Path
from savanna.quality import *
from savanna.pipeline import run
from savanna.etl import load_sales,amount
from savanna.masking import mask,token

class QualityTests(unittest.TestCase):
    def test_phone_variants_and_invalid(self):
        self.assertEqual(phone('0772 000001'),'+256772000001')
        self.assertEqual(phone('00256772000001'),'+256772000001')
        self.assertEqual(phone('123'),'')
    def test_ambiguous_date_requires_contract(self):
        self.assertEqual(parse_date('03/04/2026'),'')
        self.assertEqual(parse_date('03/04/2026',True),'2026-04-03')
        self.assertEqual(parse_date('2026-02-30'),'')
    def test_shared_phone_not_identity(self):
        a={'name':'A','phone':'0772000001','email':'a@example.invalid'}
        b={**a,'name':'B','email':'b@example.invalid'}
        self.assertNotEqual(person_key(a),person_key(b))
        self.assertLess(match_score(a,b),70)
    def test_synthetic_pipeline(self):
        with tempfile.TemporaryDirectory() as t:
            m=run(Path('data/synthetic'),Path(t),Path('data/reference'),date(2026,9,29))
            self.assertEqual(m['customers']['before']['rows'],6)
            self.assertEqual(m['customers']['after']['rows'],5)
            self.assertIsNone(m['customers']['after']['accuracy_pct'])
            self.assertEqual(m['products']['after']['rows'],4)
            self.assertTrue(m['provenance']['synthetic'])
    def test_masking_removes_direct_identifiers(self):
        k=b'x'*32; r=mask({'customer_id':'A','name':'Private','phone':'0772000001','email':'private@example.invalid','district':'Gulu'},k)
        self.assertEqual(set(r),{'customer_token','district'})
        self.assertNotEqual(token('A',k),token('A',b'y'*32))
        with self.assertRaises(ValueError):token('A',b'short')
    def test_empty_profile_no_fake_zero(self):
        self.assertIsNone(profile([],'customers',{},date.today())['uniqueness_pct'])

class SalesTests(unittest.TestCase):
    def setUp(self):
        self.db={}
        self.row={'source':'pos','order_id':'O1','line_no':'1','order_date':'2026-09-01','customer_id':'C1','sku':'P1','store_id':'S1','quantity':'-2','unit_price':'UGX 1,000','currency':'UGX','payment_ref':''}
    def load(self,rows):return load_sales(rows,self.db,{'P1'},{'C1'})
    def test_return_and_replay(self):
        self.assertEqual(self.load([self.row])['loaded'],1)
        self.assertEqual(next(iter(self.db.values()))[10],'-2000')
        self.assertEqual(self.load([self.row])['replayed'],1)
    def test_conflicting_replay_quarantined(self):
        self.load([self.row]);self.assertEqual(self.load([{**self.row,'quantity':'-3'}])['quarantined'],1)
    def test_orphans_and_bad_currency(self):
        for changes in ({'sku':'UNKNOWN'},{'customer_id':'UNKNOWN'},{'unit_price':'KES 10'},{'quantity':'NaN'},{'order_date':'04/03/2026'}):
            self.assertEqual(self.load([{**self.row,**changes}])['quarantined'],1)
    def test_cash_null_payment_reference_is_retained(self):
        self.assertEqual(self.load([self.row])['loaded'],1)
if __name__=='__main__':unittest.main()
