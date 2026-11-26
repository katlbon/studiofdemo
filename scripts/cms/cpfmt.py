import itertools, time
_ids = itertools.count(int(time.time() * 1000))
def is_switch(v): return isinstance(v, dict) and v.get('$fnType') == 'switch'
def is_array(v): return isinstance(v, dict) and v.get('$fnType') == 'array'
def decode(v):
    if is_switch(v): return v.get('defaultCase')
    if is_array(v):
        items = sorted(v.get('values', {}).values(), key=lambda x: x.get('$position', 0))
        out = []
        for it in items:
            if set(it.keys()) - {'id', '$position'} == {'value'}: out.append(decode(it['value']))
            else: out.append({k: decode(x) for k, x in it.items() if k not in ('id', '$position')})
        return out
    if isinstance(v, dict): return {k: decode(x) for k, x in v.items()}
    return v
def sw(x): return {'cases': None, '$fnType': 'switch', 'varyByKeys': ['locale'], 'defaultCase': x, 'configurationSourceType': 'contexts'}
META = ('$componentKey', '$componentTitle')
def encode(v, key=None):
    if isinstance(v, list):
        vals = {}
        for i, it in enumerate(v):
            n = next(_ids)
            if isinstance(it, dict): e = {k: (x if k in META else encode(x, k)) for k, x in it.items()}
            else: e = {'value': encode(it)}
            e.update({'id': n, '$position': i}); vals[str(n)] = e
        return {'values': vals, '$fnType': 'array'}
    if isinstance(v, dict): return {k: (x if k in META else encode(x, k)) for k, x in v.items()}
    return sw(v)
