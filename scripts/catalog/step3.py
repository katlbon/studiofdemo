import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vtex import call
ST = 'state.json'; st = json.load(open(ST))
def save(): json.dump(st, open(ST, 'w'), indent=1, ensure_ascii=False)
def ok(s, r, what):
    if s >= 300: raise SystemExit(f'{what} failed {s}: {r}')
    return r
SEASON = ['Vestido largo strapless globo', 'Vestido midi con insumo en manga', 'Vestido corto de lentejuelas', 'Blusa halter estampada',
          'Camiseta bordada con brillo', 'Crop top con vivos en contraste', 'Falda midi plisada', 'Chaqueta de cuero sintetico',
          'Sandalia de tacon metalizada', 'Bolso de hombro acolchado', 'Aretes argolla dorados', 'Jean campana tiro alto']
# 1. seasonal collection
if 'collection' not in st:
    s, r = call('POST', '/api/catalog/pvt/collection/', {'Name': 'Party Season 2026', 'Description': 'Coleccion de temporada Party Season / Black Sale',
        'Searchable': True, 'Highlight': True, 'DateFrom': '2026-11-01T00:00:00', 'DateTo': '2027-01-31T23:59:59'})
    st['collection'] = ok(s, r, 'collection')['Id']; save()
if 'subcollection' not in st:
    s, r = call('POST', '/api/catalog/pvt/subcollection', {'CollectionId': st['collection'], 'Name': 'Party Season 2026 - SKUs', 'Type': 'Inclusive', 'PreSale': False, 'Release': True})
    st['subcollection'] = ok(s, r, 'subcollection')['Id']; save()
if not st.get('collection_skus'):
    for n in SEASON:
        for sk in st['products'][n]['skus'].values():
            s, r = call('POST', f"/api/catalog/pvt/subcollection/{st['subcollection']}/stockkeepingunit", {'SkuId': sk['id']})
            if s >= 300 and 'already' not in str(r).lower(): ok(s, r, 'colsku')
    st['collection_skus'] = True; save()
# 2. promotion: 35% off the collection
if 'promo' not in st:
    s, r = call('POST', '/api/rnb/pvt/calculatorconfiguration', {'name': 'Black Sale - Party Season 35% OFF', 'description': '35% off coleccion Party Season 2026',
        'beginDateUtc': '2026-11-01T05:00:00Z', 'endDateUtc': '2027-01-31T05:00:00Z', 'isActive': True, 'type': 'regular',
        'percentualDiscountValue': 35, 'nominalDiscountValue': 0, 'maximumUnitPriceDiscount': 0, 'discountType': 'percentual',
        'collections': [{'id': str(st['collection']), 'name': 'Party Season 2026'}], 'collectionsIsInclusive': True, 'collections1BuyTogether': [], 'idsSalesChannel': ['1'],
        'areSalesChannelIdsExclusive': False, 'cumulative': False, 'isFeatured': True, 'origin': 'Marketplace', 'accumulateWithManualPrice': False})
    st['promo'] = ok(s, r, 'promo')['idCalculatorConfiguration']; save()
# free shipping over $60 (Studio F: envio gratis > $250.000 COP)
if 'promo_ship' not in st:
    s, r = call('POST', '/api/rnb/pvt/calculatorconfiguration', {'name': 'Envio gratis compras > $60', 'beginDateUtc': '2026-11-01T05:00:00Z',
        'isActive': True, 'type': 'regular', 'discountType': 'shipping', 'percentualShippingDiscountValue': 100, 'percentualDiscountValue': 0,
        'totalValueFloor': 60, 'idsSalesChannel': ['1'], 'cumulative': True, 'isFeatured': False, 'origin': 'Marketplace'})
    st['promo_ship'] = ok(s, r, 'promo ship')['idCalculatorConfiguration']; save()
# 3. home-delivery shipping policy
if 'policy' not in st:
    s, base = call('GET', '/api/logistics/pvt/shipping-policies/1'); ok(s, base, 'getpol')
    for k in ('processingStatus', 'lastIndexedAt'): base.pop(k, None)
    base.update({'id': 'envio-domicilio', 'name': 'Envio a domicilio', 'shippingMethod': 'Envio a domicilio', 'deliveryChannel': 'delivery', 'isActive': True})
    s, r = call('POST', '/api/logistics/pvt/shipping-policies', base); ok(s, r, 'policy')
    st['policy'] = 'envio-domicilio'; save()
if not st.get('rates'):
    s, r = call('POST', f"/api/logistics/pvt/configuration/freights/{st['policy']}/values/update", [{
        'zipCodeStart': '00000', 'zipCodeEnd': '99999', 'weightStart': 0, 'weightEnd': 100000, 'absoluteMoneyCost': '7.90',
        'pricePercent': 0, 'pricePercentByWeight': 0, 'maxVolume': 1000000000, 'timeCost': '3.00:00:00', 'country': 'USA',
        'operationType': 1, 'polygon': '', 'minimumValueInsurance': 0, 'restrictedFreights': []}])
    ok(s, r, 'rates'); st['rates'] = True; save()
if not st.get('dock_linked'):
    s, d = call('GET', '/api/logistics/pvt/configuration/docks/1'); ok(s, d, 'dock')
    if st['policy'] not in d['freightTableIds']: d['freightTableIds'].append(st['policy'])
    s, r = call('POST', '/api/logistics/pvt/configuration/docks', d); ok(s, r, 'dock update')
    st['dock_linked'] = True; save()
print({k: st[k] for k in ('collection', 'promo', 'promo_ship', 'policy')})
