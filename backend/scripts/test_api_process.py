import os
import sys
import json

# Ensure backend package is on path and Django settings are set
sys.path.insert(0, r"e:\powerotfarm\backend")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'powerotfarm.settings')

import django
django.setup()

from django.test import Client

c = Client()
resp = c.get('/api/process/')
print('status', resp.status_code)
try:
    data = json.loads(resp.content)
    print('items:', len(data))
    for i, item in enumerate(data, 1):
        print(i, item.get('title'))
except Exception as e:
    print('error parsing response:', e)
    print('raw content:', resp.content)
