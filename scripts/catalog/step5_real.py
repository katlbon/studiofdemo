"""Replace placeholder products with real Studio F products (names, refs, sizes, colors, images, prices)."""
import html, json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vtex import call
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sfdata')
ST = 'state.json'; st = json.load(open(ST))
def save(): json.dump(st, open(ST, 'w'), indent=1, ensure_ascii=False)
def ok(s, r, w):
    if s >= 300: raise SystemExit(f'{w} failed {s}: {str(r)[:400]}')
    return r
# (source file, exact productName, first color filter or None, target subcategory, brand, fit)
PICK = [
 ('ropa_camisas-y-blusas', 'Camiseta bordada con brillo', 'Blusas y camisas', 'Studio F', 'Regular'),
 ('ropa_camisas-y-blusas', 'Blusa halter top interno estampada', 'Blusas y camisas', 'Studio F', 'Regular'),
 ('ropa_camisas-y-blusas', 'Crop top con vivos en contraste', 'Blusas y camisas', 'Studio F', 'Ajustado'),
 ('ropa_camisas-y-blusas', 'Blusa manga corta boxy con cartera', 'Blusas y camisas', 'Studio F', 'Holgado'),
 ('ropa_buzos', 'Buzo tejido con bordado', 'Buzos', 'Studio F', 'Regular'),
 ('ropa_chalecos', 'Chaleco tejido bordado', 'Chalecos', 'Studio F', 'Regular'),
 ('ropa_vestidos', 'Vestido midi con insumo en manga', 'Vestidos', 'Studio F', 'Ajustado'),
 ('ropa_vestidos', 'Vestido strapless con cristales', 'Vestidos', 'Studio F', 'Ajustado'),
 ('ropa_vestidos', 'Vestido corto de tiras con cristales', 'Vestidos', 'Studio F', 'Ajustado'),
 ('ropa_pantalones-y-leggings', 'Pantalon con pinzas', 'Pantalones', 'Studio F', 'Holgado'),
 ('ropa_faldas', 'Falda corta con hot fix', 'Faldas', 'Studio F', 'Ajustado'),
 ('ropa_chaquetas', 'Chaqueta manga larga tipo biker', 'Chaquetas', 'Studio F', 'Regular'),
 ('jeans_bota-campana', 'Jean campan atiro alto,pretina ancha', 'Bota campana', 'Studio F', 'Ajustado'),
 ('jeans_bota-recta', 'Jeans recto con hotfix', 'Bota recta', 'Studio F', 'Regular'),
 ('zapatos_sandalias', 'Sandalia tacon tiras', 'Sandalias', 'Studio F', 'Unico'),
 ('zapatos_tenis', 'Tenis metalizados', 'Tenis', 'Studio F', 'Unico'),
 ('accesorios_bolsos-y-carteras', 'Bolso manos libre acolchado charol', 'Bolsos y carteras', 'Studio F', 'Unico'),
 ('accesorios_bisuteria', 'Anillos variados set x4', 'Bisuteria', 'Studio F', 'Unico'),
 ('hombre_camisas', 'Camisa para hombre slim fit m/l', 'Camisas', 'Studio F Man', 'Ajustado'),
 ('hombre_pantalones', 'Pantalon chino para hombre', 'Pantalones hombre', 'Studio F Man', 'Ajustado'),
]
SIZE_MAP = {'UNIC': 'Única'}
def color_name(c): return {'CAFE': 'Café'}.get(c, c.capitalize())
def material_of(desc):
    m = re.search(r'Composici[oó]n:\s*([A-ZÁÉÍÓÚÑ ]+?)\s*\d', desc or '')
    return m.group(1).strip().capitalize() if m else 'Mezcla textil'
def ensure_value(field, name):
    if name in st['values'][field]: return st['values'][field][name]
    s, r = call('POST', '/api/catalog/pvt/specificationvalue', {'FieldId': st['fields'][field], 'Name': name, 'IsActive': True, 'Position': len(st['values'][field]) + 1})
    st['values'][field][name] = ok(s, r, f'value {field}:{name}')['FieldValueId']; save()
    return st['values'][field][name]
def ensure_cat(name, parent):
    if name not in st['cats']:
        s, r = call('POST', '/api/catalog/pvt/category', {'Name': name, 'FatherCategoryId': st['cats'][parent], 'Title': f'{name} | Studio F', 'Description': name,
            'Keywords': name, 'IsActive': True, 'ShowInStoreFront': True, 'ShowBrandFilter': True, 'ActiveStoreFrontLink': True, 'StockKeepingUnitSelectionMode': 'SPECIFICATION'})
        st['cats'][name] = ok(s, r, 'cat ' + name)['Id']; save()
ensure_cat('Buzos', 'Ropa'); ensure_cat('Chalecos', 'Ropa')
st.setdefault('real', {})
for f, pname, sub, brand, fit in PICK:
    src = next(p for p in json.load(open(os.path.join(SRC, f + '.json'))) if p['productName'] == pname)
    rp = st['real'].setdefault(pname, {'skus': {}})
    if 'id' not in rp:
        clean = lambda t: re.sub(r'\s*&\s*', ' y ', html.unescape(t or ''))
        desc = clean(src['description']); src['metaTagDescription'] = clean(src.get('metaTagDescription')); src['productTitle'] = clean(src.get('productTitle'))
        s, r = call('POST', '/api/catalog/pvt/product', {'Name': pname, 'CategoryId': st['cats'][sub], 'BrandId': st['brands'][brand],
            'LinkId': src['linkText'], 'RefId': src['productReference'], 'IsVisible': True, 'Description': desc,
            'DescriptionShort': re.sub('<[^>]+>', ' ', desc).strip()[:250], 'ReleaseDate': src['releaseDate'][:19], 'KeyWords': f'{sub}, {brand}',
            'Title': src.get('productTitle') or pname, 'IsActive': True, 'ShowWithoutStock': False, 'MetaTagDescription': src.get('metaTagDescription', '')[:250]})
        rp['id'] = ok(s, r, 'product ' + pname)['Id']; save()
        for fld, v in (('Material', material_of(desc)), ('Ajuste', fit)):
            s, r = call('POST', f"/api/catalog/pvt/product/{rp['id']}/specification", {'FieldId': st['fields'][fld], 'FieldValueId': ensure_value(fld, v)})
            ok(s, r, 'prodspec')
    for it in src['items']:
        key = it['itemId']
        sk = rp['skus'].setdefault(key, {})
        if sk.get('done'): continue
        color = color_name(it['Color'][0]); size = SIZE_MAP.get(it['Talla'][0], it['Talla'][0])
        o = it['sellers'][0]['commertialOffer']
        if 'id' not in sk:
            ref = next((x['Value'] for x in it.get('referenceId', []) if x.get('Value')), key)
            s, r = call('POST', '/api/catalog/pvt/stockkeepingunit', {'ProductId': rp['id'], 'IsActive': False, 'Name': f'{pname} - {color} - {size}',
                'RefId': f'SF-{ref}', 'PackagedHeight': 5, 'PackagedLength': 30, 'PackagedWidth': 25, 'PackagedWeightKg': 0.5,
                'MeasurementUnit': 'un', 'UnitMultiplier': 1})
            sk['id'] = ok(s, r, 'sku')['Id']; sk.update({'color': color, 'size': size, 'price': o['Price'], 'list': o['ListPrice']}); save()
        sid = sk['id']
        for fld, v in (('Color', color), ('Talla', size)):
            s, r = call('POST', f'/api/catalog/pvt/stockkeepingunit/{sid}/specification', {'FieldId': st['fields'][fld], 'FieldValueId': ensure_value(fld, v)})
            if s >= 300 and 'already' not in str(r).lower(): ok(s, r, 'skuspec')
        for n, im in enumerate(it['images']):
            url = im['imageUrl'].split('?')[0]
            s, r = call('POST', f'/api/catalog/pvt/stockkeepingunit/{sid}/file', {'IsMain': n == 0, 'Label': color, 'Name': f"{rp['id']}-{key}-{n}", 'Text': pname, 'Url': url})
            ok(s, r, 'image')
        s, b = call('GET', f'/api/catalog/pvt/stockkeepingunit/{sid}'); b = ok(s, b, 'getsku'); b['IsActive'] = True
        ok(*call('PUT', f'/api/catalog/pvt/stockkeepingunit/{sid}', b), 'activate')
        lst = int(o['ListPrice']) or int(o['Price']); pr = int(o['Price']) or lst
        in_promo = abs(pr / lst - 0.65) < 0.005
        sk['promo35'] = in_promo
        base = lst if in_promo else pr   # 35% comes from the collection promotion; other discounts are list vs base price
        ok(*call('PUT', f'/demofskb/pricing/prices/{sid}', {'basePrice': base, 'listPrice': lst, 'costPrice': int(lst * .35)}, host='https://api.vtex.com'), 'price')
        ok(*call('PUT', f'/api/logistics/pvt/inventory/skus/{sid}/warehouses/{st["warehouse"]}', {'unlimitedQuantity': False, 'quantity': 50}), 'stock')
        if in_promo:
            s, r = call('POST', f"/api/catalog/pvt/subcollection/{st['subcollection']}/stockkeepingunit", {'SkuId': sid})
            if s >= 300 and 'already' not in str(r).lower(): ok(s, r, 'colsku')
        sk['done'] = True; save()
    print('ok', rp['id'], pname, len(rp['skus']), flush=True)
# deactivate placeholder products
if not st.get('placeholders_off'):
    for name, p in st['products'].items():
        s, b = call('GET', f"/api/catalog/pvt/product/{p['id']}"); b = ok(s, b, 'getprod')
        b.update({'IsActive': False, 'IsVisible': False}); ok(*call('PUT', f"/api/catalog/pvt/product/{p['id']}", b), 'deactivate')
    st['placeholders_off'] = True; save(); print('placeholders deactivated')
