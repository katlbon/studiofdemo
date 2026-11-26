"""Re-price catalog in COP and move shipping/free-shipping to Colombia (trade policy 1 is COP/COL)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vtex import call
import data
st = json.load(open('state.json'))
def ok(s, r, w):
    if s >= 300: raise SystemExit(f'{w} {s} {r}')
    return r
def cop(usd): return int(round(usd * 4)) * 1000 - 100  # 99.9 -> 399.900
for name, *_rest in data.PRODUCTS:
    usd = _rest[6]; price = cop(usd)
    for sk in st['products'][name]['skus'].values():
        s, r = call('PUT', f"/demofskb/pricing/prices/{sk['id']}", {'basePrice': price, 'listPrice': price, 'costPrice': int(price * .4)}, host='https://api.vtex.com')
        ok(s, r, 'price')
    print(name, price, flush=True)
# shipping rates for Colombia (6-digit postal codes)
s, r = call('POST', f"/api/logistics/pvt/configuration/freights/{st['policy']}/values/update", [{
    'zipCodeStart': '000000', 'zipCodeEnd': '999999', 'weightStart': 0, 'weightEnd': 100000, 'absoluteMoneyCost': '15900',
    'pricePercent': 0, 'pricePercentByWeight': 0, 'maxVolume': 1000000000, 'timeCost': '3.00:00:00', 'country': 'COL',
    'operationType': 1, 'polygon': '', 'minimumValueInsurance': 0, 'restrictedFreights': []}])
ok(s, r, 'rates COL')
s, p = call('GET', f"/api/rnb/pvt/calculatorconfiguration/{st['promo_ship']}"); ok(s, p, 'getpromo')
p.update({'totalValueFloor': 250000, 'name': 'Envio gratis compras > $250.000'})
s, r = call('POST', '/api/rnb/pvt/calculatorconfiguration', p); ok(s, r, 'promo ship update')
print('shipping ok')
