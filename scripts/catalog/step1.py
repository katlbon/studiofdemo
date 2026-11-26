import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vtex import call
import data
ST = 'state.json'
st = json.load(open(ST)) if os.path.exists(ST) else {}
def save(): json.dump(st, open(ST, 'w'), indent=1, ensure_ascii=False)
def ok(s, r, what):
    if s >= 300: raise SystemExit(f'{what} failed {s}: {r}')
    return r
def cat(name, father, title):
    s, r = call('POST', '/api/catalog/pvt/category', {'Name': name, 'FatherCategoryId': father, 'Title': title,
        'Description': title, 'Keywords': name, 'IsActive': True, 'ShowInStoreFront': True, 'ShowBrandFilter': True,
        'ActiveStoreFrontLink': True, 'StockKeepingUnitSelectionMode': 'SPECIFICATION', 'Score': None})
    return ok(s, r, 'category ' + name)['Id']
st.setdefault('cats', {})
if 'root' not in st['cats']:
    st['cats']['root'] = cat('studiofcatalog', None, 'Studio F | Catalogo'); save()
root = st['cats']['root']
for dep, subs in data.TREE.items():
    if dep not in st['cats']:
        st['cats'][dep] = cat(dep, root, f'{dep} | Studio F'); save()
    for sub in subs:
        if sub not in st['cats']:
            st['cats'][sub] = cat(sub, st['cats'][dep], f'{sub} | Studio F'); save()
st.setdefault('brands', {})
for b in data.BRANDS:
    if b not in st['brands']:
        s, r = call('POST', '/api/catalog/pvt/brand', {'Name': b, 'Active': True, 'Title': b, 'MetaTagDescription': b})
        st['brands'][b] = ok(s, r, 'brand')['Id']; save()
# spec groups + fields on root category (inherited by children)
st.setdefault('groups', {})
for g in ['Variaciones', 'Caracteristicas']:
    if g not in st['groups']:
        s, r = call('POST', '/api/catalog/pvt/specificationgroup', {'CategoryId': root, 'Name': g})
        st['groups'][g] = ok(s, r, 'group')['Id']; save()
st.setdefault('fields', {}); st.setdefault('values', {})
FIELDS = [('Color', True, list(data.COLORS)), ('Talla', True, data.SIZES), ('Material', False, data.MATERIALS), ('Ajuste', False, data.FITS)]
for name, sku, vals in FIELDS:
    if name not in st['fields']:
        s, r = call('POST', '/api/catalog/pvt/specification', {'FieldTypeId': 6 if sku else 5, 'CategoryId': root,
            'FieldGroupId': st['groups']['Variaciones' if sku else 'Caracteristicas'], 'Name': name,
            'IsFilter': True, 'IsRequired': False, 'IsOnProductDetails': not sku, 'IsStockKeepingUnit': sku,
            'IsActive': True, 'IsTopMenuLinkActive': False, 'IsSideMenuLinkActive': True, 'Position': 1})
        st['fields'][name] = ok(s, r, 'field ' + name)['Id']; save()
    st['values'].setdefault(name, {})
    for i, v in enumerate(vals):
        if v not in st['values'][name]:
            s, r = call('POST', '/api/catalog/pvt/specificationvalue', {'FieldId': st['fields'][name], 'Name': v, 'IsActive': True, 'Position': i + 1})
            st['values'][name][v] = ok(s, r, 'value ' + v)['FieldValueId']; save()
print(json.dumps({k: st[k] for k in ['cats', 'brands', 'fields']}, ensure_ascii=False))
