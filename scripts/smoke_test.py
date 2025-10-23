import requests

BASE = 'http://127.0.0.1:8000'

endpoints = [
    '/api/products/',
    '/api/services/',
    '/api/gallery/',
    '/api/process/',
]

for ep in endpoints:
    url = BASE + ep
    try:
        r = requests.get(url, timeout=3)
        print(ep, r.status_code)
    except Exception as e:
        print(ep, 'ERROR', e)

# check admin login form reachable
try:
    r = requests.get(BASE + '/admin/login/', timeout=3)
    print('/admin/login/', r.status_code)
except Exception as e:
    print('/admin/login/ ERROR', e)
