import json, os, sys, urllib.request, urllib.error
TOKEN = json.load(open(os.path.expanduser('~/.vtex/session/session.json')))['token']
ACC = 'demofskb'
def call(method, path, body=None, host=None):
    url = (host or f'https://{ACC}.vtexcommercestable.com.br') + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        'VtexIdclientAutCookie': TOKEN, 'Content-Type': 'application/json', 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            t = r.read().decode()
            return r.status, (json.loads(t) if t.strip() else None)
    except urllib.error.HTTPError as e:
        t = e.read().decode()
        try: return e.code, json.loads(t)
        except Exception: return e.code, t
if __name__ == '__main__':
    m, p = sys.argv[1], sys.argv[2]
    b = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
    s, r = call(m, p, b)
    print(s); print(json.dumps(r, ensure_ascii=False, indent=1)[:6000])
