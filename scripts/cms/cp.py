import json,os,sys,urllib.request,urllib.error
T=json.load(open(os.path.expanduser('~/.vtex/session/session.json')))['token']
BASE='https://api.vtexcommercestable.com.br/api/content-platform/manage/demofskb'
def cp(method, path, body=None):
    r=urllib.request.Request(BASE+path, data=json.dumps(body).encode() if body is not None else None, method=method,
        headers={'Authorization':'Bearer '+T,'Content-Type':'application/json','Accept':'application/json'})
    try:
        with urllib.request.urlopen(r, timeout=60) as x:
            t=x.read().decode(); return x.status, (json.loads(t) if t.strip() else None)
    except urllib.error.HTTPError as e:
        t=e.read().decode()
        try: return e.code, json.loads(t)
        except Exception: return e.code, t[:300]
if __name__=='__main__':
    s,r=cp(sys.argv[1], sys.argv[2], json.loads(sys.argv[3]) if len(sys.argv)>3 else None)
    print(s); print(json.dumps(r,indent=1,ensure_ascii=False)[:3000])
