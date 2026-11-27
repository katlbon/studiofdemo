"""Associate Studio F products only with trade policy 2 (Secondary) and move promotions there."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vtex import call
st = json.load(open('state.json'))
TP = 2
ids = [p['id'] for p in st['real'].values()] + [p['id'] for p in st['products'].values()]
for pid in ids:
    s, cur = call('GET', f'/api/catalog/pvt/product/{pid}/salespolicy')
    have = {int(x.get('StoreId') or x.get('SalesChannelId') or x.get('Id') or 0) for x in (cur or [])} if isinstance(cur, list) else set()
    if TP not in have:
        s, r = call('POST', f'/api/catalog/pvt/product/{pid}/salespolicy/{TP}')
        if s >= 300: raise SystemExit(f'assoc {pid} {s} {r}')
    for other in have - {TP}:
        call('DELETE', f'/api/catalog/pvt/product/{pid}/salespolicy/{other}')
s, cur = call('GET', f"/api/catalog/pvt/product/{ids[0]}/salespolicy"); print('example association', cur)
for key in ('promo', 'promo_ship'):
    s, p = call('GET', f"/api/rnb/pvt/calculatorconfiguration/{st[key]}")
    p['idsSalesChannel'] = [str(TP)]; p['areSalesChannelIdsExclusive'] = False
    s, r = call('POST', '/api/rnb/pvt/calculatorconfiguration', p); print(key, p['name'], s)
st['trade_policy'] = TP; json.dump(st, open('state.json', 'w'), indent=1, ensure_ascii=False)
