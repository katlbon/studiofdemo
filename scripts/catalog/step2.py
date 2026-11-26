import json, os, sys, re, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vtex import call
import data
ST = 'state.json'; st = json.load(open(ST))
def save(): json.dump(st, open(ST, 'w'), indent=1, ensure_ascii=False)
def ok(s, r, what):
    if s >= 300: raise SystemExit(f'{what} failed {s}: {r}')
    return r
def slug(s): return re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()).strip('-')
IMG = "https://raw.githubusercontent.com/katlbon/studiofdemo/main/public/catalog/"
WH = 'bodega-central'
if not st.get('warehouse'):
    s, r = call('POST', '/api/logistics/pvt/configuration/warehouses', {'id': WH, 'name': 'Bodega Central',
        'warehouseDocks': [{'dockId': '1', 'time': '1.00:00:00', 'cost': 0.0}], 'pickupPointIds': [], 'priority': 0, 'isActive': True})
    ok(s, r, 'warehouse'); st['warehouse'] = WH; save()
st.setdefault('products', {})
for i, (name, sub, brand, mat, fit, colors, sizes, price, shape, desc) in enumerate(data.PRODUCTS, 1):
    pst = st['products'].setdefault(name, {'skus': {}})
    if 'id' not in pst:
        s, r = call('POST', '/api/catalog/pvt/product', {'Name': name, 'CategoryId': st['cats'][sub], 'BrandId': st['brands'][brand],
            'LinkId': slug(name), 'RefId': f'SF{i:03d}', 'IsVisible': True, 'Description': desc, 'DescriptionShort': desc,
            'ReleaseDate': '2026-11-01T00:00:00', 'KeyWords': f'{sub}, {brand}, studio f', 'Title': f'{name} | Studio F',
            'IsActive': True, 'ShowWithoutStock': False, 'MetaTagDescription': desc})
        pst['id'] = ok(s, r, 'product ' + name)['Id']; save()
    if not pst.get('specs'):
        for f, v in (('Material', mat), ('Ajuste', fit)):
            s, r = call('POST', f"/api/catalog/pvt/product/{pst['id']}/specification", {'FieldId': st['fields'][f], 'FieldValueId': st['values'][f][v]})
            ok(s, r, 'prodspec')
        pst['specs'] = True; save()
    for c in colors:
        for z in sizes:
            key = f'{c}|{z}'
            if key in pst['skus'] and pst['skus'][key].get('done'): continue
            sk = pst['skus'].setdefault(key, {})
            if 'id' not in sk:
                s, r = call('POST', '/api/catalog/pvt/stockkeepingunit', {'ProductId': pst['id'], 'IsActive': False,
                    'Name': f'{name} - {c} - {z}', 'RefId': f'SF{i:03d}-{slug(c)}-{slug(z)}'.upper(),
                    'PackagedHeight': 5, 'PackagedLength': 30, 'PackagedWidth': 25, 'PackagedWeightKg': 0.5,
                    'MeasurementUnit': 'un', 'UnitMultiplier': 1, 'ActivateIfPossible': True})
                sk['id'] = ok(s, r, 'sku')['Id']; save()
            sid = sk['id']
            for f, v in (('Color', c), ('Talla', z)):
                s, r = call('POST', f'/api/catalog/pvt/stockkeepingunit/{sid}/specification', {'FieldId': st['fields'][f], 'FieldValueId': st['values'][f][v]})
                if s >= 300 and 'already' not in str(r).lower(): ok(s, r, 'skuspec')
            for n in (1, 2):
                fn = f'{slug(name)}-{slug(c)}-{n}'
                s, r = call('POST', f'/api/catalog/pvt/stockkeepingunit/{sid}/file', {'IsMain': n == 1, 'Label': c, 'Name': fn, 'Text': f'{name} {c}', 'Url': IMG + fn + '.jpg'})
                ok(s, r, 'image')
            s, r = call('GET', f'/api/catalog/pvt/stockkeepingunit/{sid}'); body = ok(s, r, 'getsku'); body['IsActive'] = True
            s, r = call('PUT', f'/api/catalog/pvt/stockkeepingunit/{sid}', body); ok(s, r, 'activate')
            s, r = call('PUT', f'/demofskb/pricing/prices/{sid}', {'basePrice': price, 'listPrice': price, 'costPrice': round(price * .4, 2)}, host='https://api.vtex.com')
            ok(s, r, 'price')
            s, r = call('PUT', f'/api/logistics/pvt/inventory/skus/{sid}/warehouses/{WH}', {'unlimitedQuantity': False, 'quantity': 50})
            ok(s, r, 'stock')
            sk['done'] = True; save()
    print('ok', pst['id'], name, len(pst['skus']), flush=True)
